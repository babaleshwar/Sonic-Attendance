# SonicAttend 🔊🛡️
> **Proxy-Proof Inaudible Acoustic Ultrasonic Attendance Platform**  
> *Developed for VSM's S. R. Kittoor Institute of Technology (VSMSRKITE), Nipani*  
> *Department of Computer Science & Engineering • Affiliated to VTU Belagavi*

---

## 📌 Overview

**SonicAttend** is an air-gapped, zero-hardware classroom attendance system that eliminates proxy attendance using high-frequency inaudible acoustic waves (18.5 kHz – 19.8 kHz) and cryptographic device binding.

Unlike traditional methods:
* **No Paper Roll Calls**: Zero time wasted calling names; attendance is recorded within 2 seconds.
* **No Static QR Code Forwarding**: Tokens rotate every 15 seconds via HMAC-SHA256. Messaging apps (WhatsApp, Telegram) compress and cut audio frequencies above 16 kHz, making remote proxy sharing physically impossible.
* **No Bluetooth Bleed**: Bluetooth signals penetrate brick walls (30–50 m range), allowing proxies from canteens or adjacent corridors. Ultrasonic acoustic waves **cannot penetrate concrete walls**, strictly confining attendance to students physically present inside the lecture hall.
* **Anti-Proxy Device Binding**: Each student's account is permanently bound to their registered smartphone's hardware signature (1 Phone = 1 USN).

---

## ⚡ Key Features

### 👨‍🏫 Lecturer Command Console (`lecturer_console.html`)
* **Inaudible Acoustic Transmitter**: Built on HTML5 Web Audio API, synthesizing frequency-shift keyed (FSK) pilot and carrier tones (18.5 kHz – 19.8 kHz) through laptop speakers.
* **Real-time Canvas FFT Visualizer**: Live 512-point spectral frequency curve and sub-channel activity meters.
* **Rotating TOTP Dial**: Dynamic 15-second countdown displaying real-time cryptographic tokens (`#8FF1`, `#7FCE`).
* **Live Attendance Roster Table**: Instant attendee sync with search filters (`All`, `Verified`, `Pending`).
* **1-Click Attendance Simulation**: Evaluator & classroom viva demo button to simulate ultrasonic check-in for registered students in 1 click without needing multiple physical phones.
* **Emergency Optical Fallback QR**: Dynamic popup modal encoding the rotating token and cryptographic HMAC for legacy student devices with mic limitations.
* **Official VTU Printable Attendance Sheet**: Generates official print-ready university format with college letterhead, attendance quorum %, and dual signature blocks for Course Coordinator and HOD.

### 🎓 Student Mobile PWA (`student_attendance.html`)
* **Acoustic Receiver Engine**: Uses Web Audio API `MediaStreamAudioSourceNode` to decode the classroom acoustic token locally in under 2 seconds.
* **Class Schedule / Timetable Tab**: Day-by-day timetable view (Mon–Sat) displaying period slots, room numbers, and active lecture indicators.
* **Roster & VTU Analytics Tab**: Comprehensive scorecard showing overall attendance percentage, VTU 75% compliance status, subject-wise breakdown bars, and recent verification audit logs.
* **Device Account & Audit Tab**: Displays registered device hardware fingerprint (`#DEV-XXXX`) and provides an official HOD Device Re-binding Ticket submission workflow.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend Runtime** | Python 3.10+ |
| **Web Framework** | Flask 3.0+ |
| **Database** | SQLite3 (`sonicattend.db`) |
| **Cryptography** | HMAC-SHA256 (TOTP rotating tokens), SHA-256 (Device signatures) |
| **Frontend UI** | HTML5, Tailwind CSS, Google Material Symbols Outlined |
| **Audio Synthesis & FFT** | HTML5 Web Audio API (`OscillatorNode`, `AnalyserNode`, `GainNode`) |
| **Deployment Targets** | Windows Localhost, Hostinger cPanel (Passenger WSGI), Linux VPS (Nginx + Gunicorn) |

---

## 📁 Repository Structure

```
Sonnic_Attendance/
├── app.py                      # Core Flask backend server and REST API endpoints
├── index.html                  # Main University Portal Landing Hub
├── lecturer_console.html       # Lecturer Command Console (Transmitter & Live Roster)
├── lecturer_login.html         # Faculty Login and Registration Portal
├── student_attendance.html     # Student Mobile PWA (Check-in, Schedule, Analytics)
├── login.html                  # Student Login Portal
├── student_register.html       # Student Registration & Hardware Device Binding
├── run_server.bat              # 1-Click Windows execution script
├── logo.png                    # College & system emblem
├── sonicattend.db              # Active SQLite Database
├── sonicattend_backup.db       # Safe backup of database state
├── PROJECT_PRD.md              # Detailed Product Requirements Document & Changelog
├── SONICATTEND_MASTER_PROMPT.xml # Master XML specification prompt for AI builders / Horizon
└── README.md                   # This project overview documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
* Python 3.10 or higher installed ([Download Python](https://www.python.org/downloads/))
* Google Chrome, Microsoft Edge, or Safari browser

### 2. Installation
Clone or navigate to the project directory:
```powershell
cd "c:\Users\hp\OneDrive\Desktop\Sonnic_Attendance"
```

Install the required dependencies:
```powershell
pip install flask
```

### 3. Running the Server

#### Method A: 1-Click Batch File (Windows)
Double-click **`run_server.bat`** in the project folder.

#### Method B: Terminal / Command Line
```powershell
python app.py
```

The server will launch at:
👉 **`http://127.0.0.1:5000`**

---

## 🌐 Portal Navigation Links

| Portal | URL | Description |
| :--- | :--- | :--- |
| 🏠 **Home Hub** | [http://127.0.0.1:5000/](http://127.0.0.1:5000/) | Main portal directory |
| 👨‍🏫 **Lecturer Console** | [http://127.0.0.1:5000/lecturer_console.html](http://127.0.0.1:5000/lecturer_console.html) | Acoustic transmitter, live roster & reports |
| 🎓 **Student Attendance** | [http://127.0.0.1:5000/student_attendance.html](http://127.0.0.1:5000/student_attendance.html) | Acoustic receiver, timetable & scorecard |
| 📝 **Student Register** | [http://127.0.0.1:5000/student_register.html](http://127.0.0.1:5000/student_register.html) | Student registration & hardware lock |
| 🔑 **Lecturer Login** | [http://127.0.0.1:5000/lecturer_login.html](http://127.0.0.1:5000/lecturer_login.html) | Faculty authentication |

---

## 📊 Database Schema Summary

The embedded SQLite database (`sonicattend.db`) contains 7 core tables:
1. **`students`**: USN, name, department, semester, mobile, hashed password, and bound hardware ID (`DEV-XXXX`).
2. **`faculty`**: Faculty ID, name, designation, department, mobile, and assigned subject.
3. **`class_sessions`**: Active lecture session, room number, frequency, and secret seed.
4. **`attendance_records`**: Verified timestamps, USNs, acoustic tokens, and hardware verification status.
5. **`courses`**: Course catalog (code, title, faculty, room, credits).
6. **`timetable`**: Weekly timetable slots (Day, Period, Course, Time, Room, Lab flag).
7. **`device_rebinding_tickets`**: Student phone replacement audit tickets with HOD approval status.

---

## 🔒 Acoustic Protocol Frequencies

| Tone Channel | Frequency | Protocol Function |
| :--- | :--- | :--- |
| **Shift 0** | 18,500 Hz | FSK Binary Data Modulation |
| **Shift 1** | 18,800 Hz | FSK Binary Data Modulation |
| **Shift 2** | 19,000 Hz | Synchronization Pilot Wave |
| **Primary** | **19,250 Hz** | **Main Acoustic Carrier & Amplitude Reference** |
| **Shift 3** | 19,500 Hz | Frame Boundary Marker |
| **Shift 4** | 19,800 Hz | High-band Parity & Integrity Check |

---

## 📄 License & Institutional Notice
Developed as an academic final-year project at **VSMSRKITE Nipani**, Department of Computer Science & Engineering, affiliated to **Visvesvaraya Technological University (VTU), Belagavi**.  
Academic and demonstration use permitted.
