# SonicAttend: Inaudible Acoustic Ultrasonic Attendance Platform
## Comprehensive Product Requirements Document (PRD), Architecture, Changelog & Roadmap Checklist

**Institution**: VSM's S. R. Kittoor Institute of Technology (VSMSRKITE), Nipani  
**Department**: Computer Science & Engineering  
**Affiliation**: Visvesvaraya Technological University (VTU), Belagavi  
**Version**: 2.0.0 (Production-Ready Prototype)  
**Last Updated**: November 24, 2026  

---

## Table of Contents
1. [Executive Summary & Problem Statement](#1-executive-summary--problem-statement)
2. [Core Technology & Security Protocols](#2-core-technology--security-protocols)
3. [System Architecture & Data Flow](#3-system-architecture--data-flow)
4. [Database Architecture & Schema (SQLite)](#4-database-architecture--schema-sqlite)
5. [Backend RESTful API Reference](#5-backend-restful-api-reference)
6. [Frontend UI/UX Specification & File Architecture](#6-frontend-uiux-specification--file-architecture)
7. [Comprehensive Changelog (Changes Made So Far)](#7-comprehensive-changelog-changes-made-so-far)
8. [Pending Features & Development Checklist](#8-pending-features--development-checklist)
9. [Operational Guide (How to Run & Test)](#9-operational-guide-how-to-run--test)

---

## 1. Executive Summary & Problem Statement

### 1.1 The Problem
Traditional college attendance systems suffer from severe vulnerabilities:
1. **Paper Roll Calls**: Consumes 10–15 minutes per lecture, prone to paper manipulation, proxy roll calls, and manual entry errors into university ERP portals.
2. **Static QR Codes**: Projected on screens or boards; students click photos and forward them instantly to absent peers in hostels via WhatsApp/Telegram.
3. **Biometric Scanners (Fingerprint/Face Kiosks)**: Create massive physical bottlenecks at classroom doors for 60+ students, prone to sensor smudging, hardware failures, and hygiene concerns.
4. **BLE (Bluetooth Low Energy) / Wi-Fi Beacons**: Bluetooth signals easily penetrate standard classroom brick/concrete walls (30–50 meter range), allowing students in corridors, canteens, or adjacent rooms to falsely register attendance.

### 1.2 The SonicAttend Solution
**SonicAttend** is a zero-hardware, zero-app-install attendance solution utilizing high-frequency inaudible acoustic waves (18.5 kHz – 19.8 kHz) combined with cryptographic rotating TOTP tokens and physical device binding:
* **Air-Gapped Physical Boundary**: High-frequency acoustic sound waves cannot penetrate solid brick walls or closed doors, guaranteeing physical classroom presence.
* **Zero Replay / WhatsApp Sharing**: Ultrasonic tokens rotate every 15 seconds using HMAC-SHA256. Audio codecs in messaging apps (Opus, AAC) filter out frequencies above 16 kHz, making remote transmission impossible.
* **Anti-Proxy Hardware Fingerprinting**: Each student's account is cryptographically bound to their registered smartphone's hardware signature (1 Phone = 1 USN).
* **Zero Extra Hardware**: Operates entirely within standard web browsers using the HTML5 Web Audio API on teacher laptops (transmitters) and student phones (receivers).

---

## 2. Core Technology & Security Protocols

### 2.1 Acoustic Frequency Modulation (FSK Carrier Set)
SonicAttend operates within the upper spectrum of human auditory cutoff (near-ultrasound: 18,000 Hz to 20,000 Hz), fully receivable by standard smartphone MEMS microphones and transmittable via standard laptop speakers:

| Frequency | Role in Protocol | Purpose |
| :--- | :--- | :--- |
| **18,500 Hz** | FSK Shift Tone 0 | Data Bit Modulation Channel |
| **18,800 Hz** | FSK Shift Tone 1 | Data Bit Modulation Channel |
| **19,000 Hz** | FSK Shift Tone 2 | Synchronization Pilot Wave |
| **19,250 Hz** | **Primary Carrier** | Main Beacon & Amplitude Reference |
| **19,500 Hz** | FSK Shift Tone 3 | Frame Boundary Marker |
| **19,800 Hz** | FSK Shift Tone 4 | High-band Parity Check |

* **Volume Safety**: Gain capped at 0.12 (inaudible to human ears, safe for standard speaker diaphragms).
* **Signal Analysis**: 512-point Fast Fourier Transform (FFT) with a smoothing time constant of 0.7.

### 2.2 Rotating Cryptographic Token Engine (TOTP)
* **Rotation Window**: 15 seconds.
* **Payload Generation**:
  $$\text{Digest} = \text{HMAC-SHA256}(\text{Secret Seed}, \lfloor \text{Epoch Time} / 15 \rfloor)$$
* **Token Output**: 4-character uppercase Hexadecimal (`#8FF1`, `#7FCE`, etc.).
* **Grace Period**: Verification allows $\pm 1$ time-step window (tolerance for network drift between client and server).

### 2.3 Anti-Proxy Defense Matrix

```
+-----------------------------------------------------------------------------------+
|                            ATTACK VECTOR VS DEFENSE                               |
+------------------------------------+----------------------------------------------+
| Attack Vector                      | SonicAttend Defense Layer                    |
+------------------------------------+----------------------------------------------+
| 1. Remote Proxy (Hostel/Canteen)   | Acoustic Inaudible Wave (Walls block sound;  |
|                                    | WhatsApp cuts audio above 16 kHz).           |
+------------------------------------+----------------------------------------------+
| 2. Multi-Account Login on 1 Phone  | Hardware Fingerprint Binding (1 Device =     |
|                                    | 1 USN). Unregistered hardware rejected.      |
+------------------------------------+----------------------------------------------+
| 3. Physical Phone Smuggling        | Acoustic Attenuation: 19 kHz waves are       |
|    (Friend brings phone to class)  | absorbed by denim/cloth pockets (Low SNR).   |
|                                    | Optional 1-second Camera Liveness check.     |
+------------------------------------+----------------------------------------------+
```

---

## 3. System Architecture & Data Flow

```
[ Teacher Laptop ]                               [ Student Phone ]
  (Chrome / Edge)                                  (Chrome / Safari)
        |                                                 |
  [ Web Audio API ]                                 [ Web Audio API ]
  OscillatorNode (19.25 kHz)                        AnalyserNode (FFT)
        |                                                 |
        | ~ ~ ~ Inaudible Acoustic Sound Wave ~ ~ ~ >     |
        |        (Rotating Token #8FF1)                   |
        |                                                 |
        |                                      Decodes Token Locally
        |                                                 |
        |                                           [ REST POST ]
        |                                        /api/attendance/mark
        |                                        { usn, token, dev_id }
        v                                                 v
  +-------------------------------------------------------------+
  |              SonicAttend Backend Engine (Flask)              |
  |  - Verifies Session Token against HMAC Seed                 |
  |  - Verifies Device Fingerprint against Registered Database  |
  |  - Records Present Timestamp & Emits Roster Telemetry       |
  +-------------------------------------------------------------+
        |                                                 |
  [ SSE / Poll Sync ]                               [ Visual Confirmation ]
  Live Table Updated (1s)                           Green Shield Verified
```

---

## 4. Database Architecture & Schema (SQLite)

The system uses an embedded SQLite database (`sonicattend.db`) designed for low latency, local academic compliance, and zero external dependency:

### 4.1 Schema Definition

```sql
-- 1. Registered Students with Hardware Binding
CREATE TABLE IF NOT EXISTS students (
    usn TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    branch TEXT DEFAULT 'Computer Science & Engineering',
    semester TEXT DEFAULT '5th Sem',
    mobile TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    bound_device_id TEXT NOT NULL,
    device_name TEXT DEFAULT 'Registered Smartphone',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Faculty Profiles
CREATE TABLE IF NOT EXISTS faculty (
    faculty_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    department TEXT DEFAULT 'Dept of Computer Science & Engineering',
    designation TEXT DEFAULT 'Assistant Professor',
    subject TEXT DEFAULT 'CS501 - Machine Learning',
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Live Classroom Sessions
CREATE TABLE IF NOT EXISTS class_sessions (
    session_id TEXT PRIMARY KEY,
    faculty_id TEXT NOT NULL,
    subject_code TEXT NOT NULL,
    subject_name TEXT NOT NULL,
    room_no TEXT NOT NULL,
    frequency_khz REAL DEFAULT 19.25,
    secret_seed TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Attendance Transaction Ledger
CREATE TABLE IF NOT EXISTS attendance_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    usn TEXT NOT NULL,
    student_name TEXT NOT NULL,
    subject_code TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    status TEXT NOT NULL,
    device_id TEXT NOT NULL,
    device_verified INTEGER DEFAULT 1,
    acoustic_token TEXT NOT NULL,
    FOREIGN KEY (usn) REFERENCES students(usn),
    FOREIGN KEY (session_id) REFERENCES class_sessions(session_id)
);

-- 5. Course Catalog
CREATE TABLE IF NOT EXISTS courses (
    course_code TEXT PRIMARY KEY,
    course_name TEXT NOT NULL,
    faculty_name TEXT NOT NULL,
    faculty_id TEXT NOT NULL,
    room_no TEXT NOT NULL,
    credits INTEGER DEFAULT 4
);

-- 6. Weekly Class Timetable
CREATE TABLE IF NOT EXISTS timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day_of_week TEXT NOT NULL,
    period_no INTEGER NOT NULL,
    course_code TEXT NOT NULL,
    course_name TEXT NOT NULL,
    faculty_name TEXT NOT NULL,
    room_no TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    is_lab INTEGER DEFAULT 0
);

-- 7. Device Re-binding Tickets (Audit Trail)
CREATE TABLE IF NOT EXISTS device_rebinding_tickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    usn TEXT NOT NULL,
    student_name TEXT NOT NULL,
    old_device_id TEXT NOT NULL,
    new_device_id TEXT NOT NULL,
    reason TEXT NOT NULL,
    status TEXT DEFAULT 'PENDING_HOD_APPROVAL',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usn) REFERENCES students(usn)
);
```

---

## 5. Backend RESTful API Reference

### 5.1 Student APIs

| Method | Endpoint | Description | Payload / Params |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/student/register` | Registers new student & locks device | `{ usn, name, branch, semester, mobile, password, device_id, device_name }` |
| `POST` | `/api/student/login` | Authenticates student & verifies hardware | `{ usn, password, device_id }` |
| `GET` | `/api/student/profile/<usn>` | Returns profile and bound hardware ID | URL parameter `usn` |
| `GET` | `/api/student/roster/<usn>` | Full scorecard, subject breakdown, logs | URL parameter `usn` |
| `POST` | `/api/student/rebind-ticket`| Submits official hardware swap request | `{ usn, reason, old_device_id, new_device_name }` |

### 5.2 Faculty & Session APIs

| Method | Endpoint | Description | Payload / Params |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/faculty/register` | Registers new professor profile | `{ faculty_id, name, mobile, designation, subject, password }` |
| `POST` | `/api/faculty/login` | Authenticates faculty | `{ identifier, password }` |
| `POST` | `/api/session/start` | Starts broadcast & seeds cryptographic HMAC | `{ faculty_id, subject_code, subject_name, room_no, frequency_khz }` |
| `POST` | `/api/session/stop` | Stops ultrasonic broadcast & freezes session | `{}` |
| `GET` | `/api/session/active` | Current active broadcast, token, countdown | None |
| `GET` | `/api/session/roster` | Real-time attendee list, quorum stats | None |
| `POST` | `/api/session/reset` | Clears present roster for clean demonstration | `{}` |
| `POST` | `/api/session/simulate-checkin` | 1-Click live simulation for viva demos | `{ count: 5 }` |

### 5.3 Academic Compliance & Exports

| Method | Endpoint | Output Format | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/export/vtu-report` | CSV (`text/csv`) | Complete VTU portal format report for university upload. |
| `GET` | `/api/export/vtu-sheet` | Printable HTML / PDF | Official letterhead format with signature blocks for HOD and faculty. |
| `GET` | `/api/courses` | JSON | List of all registered courses. |
| `GET` | `/api/timetable` | JSON | Weekly schedule filterable by day (`?day=Mon`). |

---

## 6. Frontend UI/UX Specification & File Architecture

```
Sonnic_Attendance/
├── app.py                      # Core Flask backend server and API endpoints
├── index.html                  # Main University Portal Landing Hub
├── lecturer_console.html       # Lecturer Command Center (Transmitter & Roster)
├── lecturer_login.html         # Faculty Login and Registration Portal
├── student_attendance.html     # Student Mobile PWA (Check-in, Schedule, Roster)
├── login.html                  # Student Login Portal
├── student_register.html       # Student Registration & Device Locking Portal
├── run_server.bat              # 1-Click Windows execution script
├── logo.png                    # Institutional badge & icon
├── sonicattend.db              # Active SQLite Database (Currently clean for timetable)
├── sonicattend_backup.db       # Full backup of prior test datasets
└── PROJECT_PRD.md              # Complete Project Documentation & PRD (This file)
```

---

## 7. Comprehensive Changelog (Changes Made So Far)

### 7.1 Visual & Layout Bug Fixes
* **Resolved Footer Overlap**:
  * Added fixed bottom layout (`fixed bottom-0 left-0 right-0 z-40`) with frosted glass blur.
  * Added `pb-44` on the main container so real-time FFT spectrum cards and table rows never hide beneath the action toolbar.
* **Top Navbar Alignment**:
  * Resolved left brand text clipping and right badge overflow on mobile/tablet viewports using responsive flex-wrap and adjusted spacing.

### 7.2 Database Sanitation & Overhaul
* **Purged Dummy & Corrupted Records**:
  * Removed duplicate faculty entries, test USNs (`2VS24CS048`, `2VS24CS099`), and legacy mock strings.
  * Formatted database tables into strict VTU structures (`students`, `faculty`, `courses`, `timetable`, `class_sessions`, `attendance_records`, `device_rebinding_tickets`).
  * Backed up initial testing state to `sonicattend_backup.db`.
  * Wiped all 7 active tables in `sonicattend.db` down to 0 rows upon user request, ready for fresh college timetable ingestion.

### 7.3 Backend Syntax & Compilation Fixes
* **Resolved Python f-string CSS Collisions**:
  * Fixed `SyntaxError: f-string: invalid syntax` caused by CSS braces inside multiline f-strings for the printable HTML sheet.
  * Replaced non-ASCII unicode symbols (`✓`) with standard HTML entities (`&#x2713;`).

### 7.4 Feature Completions
* **Emergency Fallback QR Modal**:
  * Replaced temporary browser `alert(...)` with a dark cyber-futuristic modal popup.
  * Displays dynamic QR code reflecting the active 15s rotating token, course ID, and security hash.
  * Auto-updates in real time as the TOTP token rotates.
* **1-Click Live Classroom Attendance Simulation (`/api/session/simulate-checkin`)**:
  * Added "Simulate Check-in" button on lecturer console.
  * Simulates acoustic reception for pending students in real time with animated toast notifications and automatic roster synchronization.
* **Official VTU Printable Attendance Sheet (`/api/export/vtu-sheet`)**:
  * Created print-ready template with VSMSRKITE letterhead, department headers, attendance quorum percentage, and dual signature blocks for Course Coordinator and HOD.
* **Hardware Re-binding Ticket Workflow (`/api/student/rebind-ticket`)**:
  * Connected student Account tab to re-binding ticket endpoint.
  * Generates tracking IDs (`TKT-VSM-XXXX`) and displays pending audit status in student profile.
* **Empty Database Auto-Provision Guard**:
  * Prevented phantom session creation when database has 0 registered faculty.

### 7.5 Codebase De-AI Polishing & Cleanliness
* **Purged 200+ AI-Style Banner & Comment Blocks**:
  * Removed all robotic mega divider bars (`// ====================`, `# ====================`, `<!-- ==================== -->`).
  * Removed AI dead-giveaways like `(For evaluator & viva demos)`, `(Clean, No Clipping)`, `Action Cluster`, `Atmospheric Glow Backdrop`, and numbered form field labels.
  * Replaced all backend and frontend comments with clean, natural, human-written developer notations.

---

## 8. Pending Features & Development Checklist

### Phase 1: Real College Timetable Ingestion (Awaiting User Timetable)
- [ ] Receive actual weekly timetable (Days, Periods, Timings, Rooms) from user.
- [ ] Populate `courses` table with authentic VTU course codes and course titles.
- [ ] Populate `faculty` table with real faculty profiles and assign courses.
- [ ] Populate `timetable` table with period slots (Monday through Saturday).
- [ ] Ingest authentic student batch list (USNs, Names, Phone numbers).

### Phase 2: Anti-Physical Smuggling Defenses
- [ ] **Acoustic SNR Threshold Rejection**:
  - Implement client-side audio check: if ultrasonic signal SNR $< 15\text{ dB}$ (indicating phone is inside a bag or pocket), reject with prompt *"Phone must be placed on desk facing lecturer"*.
- [ ] **1-Second Camera Liveness Verification**:
  - Upon decoding acoustic sound, prompt for 1-second front-camera selfie check to ensure the student physically holding the phone matches the enrolled student.

### Phase 3: Final Production Packaging
- [ ] Package desktop launcher or standalone PWA manifest for offline caching.
- [ ] Generate comprehensive final-year project report / PPT slides based on this PRD.

---

## 9. Operational Guide (How to Run & Test)

### 9.1 Starting the Server
**Option A: 1-Click Batch File (Recommended)**
Double-click `run_server.bat` in the project root.

**Option B: Terminal / PowerShell**
```powershell
cd "c:\Users\hp\OneDrive\Desktop\Sonnic_Attendance"
python app.py
```
The server will run on: `http://127.0.0.1:5000`

### 9.2 Access Links
* **Main Hub**: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
* **Lecturer Console**: [http://127.0.0.1:5000/lecturer_console.html](http://127.0.0.1:5000/lecturer_console.html)
* **Student Portal**: [http://127.0.0.1:5000/student_attendance.html](http://127.0.0.1:5000/student_attendance.html)
* **Student Registration**: [http://127.0.0.1:5000/student_register.html](http://127.0.0.1:5000/student_register.html)
* **Faculty Registration / Login**: [http://127.0.0.1:5000/lecturer_login.html](http://127.0.0.1:5000/lecturer_login.html)

---
*Developed for VSMSRKITE Nipani • Department of Computer Science & Engineering*
