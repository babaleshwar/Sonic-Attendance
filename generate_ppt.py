import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    C_NAVY_DARK = RGBColor(10, 15, 30)       # #0a0f1e
    C_CARD_BG = RGBColor(19, 28, 52)         # #131c34
    C_CARD_BORDER = RGBColor(37, 56, 92)     # #25385c
    C_WHITE = RGBColor(255, 255, 255)
    C_CYAN = RGBColor(6, 182, 212)           # #06b6d4
    C_EMERALD = RGBColor(16, 185, 129)       # #10b981
    C_GOLD = RGBColor(245, 158, 11)          # #f59e0b
    C_SLATE_LIGHT = RGBColor(203, 213, 225)  # #cbd5e1
    C_SLATE_MUTED = RGBColor(148, 163, 184)  # #94a3b8

    def add_header(slide, section_num, title):
        # Top banner background
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = RGBColor(13, 20, 38)
        top_bar.line.color.rgb = RGBColor(30, 45, 75)
        top_bar.line.width = Pt(1)

        # Section Pill
        if section_num:
            pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.25), Inches(0.9), Inches(0.55))
            pill.fill.solid()
            pill.fill.fore_color.rgb = C_CYAN
            pill.line.fill.background()
            tf_pill = pill.text_frame
            tf_pill.text = section_num
            p = tf_pill.paragraphs[0]
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = C_NAVY_DARK
            p.alignment = PP_ALIGN.CENTER

        # Title text
        tx = slide.shapes.add_textbox(Inches(1.85 if section_num else 0.8), Inches(0.18), Inches(7.5), Inches(0.75))
        tf = tx.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = title.upper()
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

        # College / Dept right tag
        tx_right = slide.shapes.add_textbox(Inches(8.5), Inches(0.18), Inches(4.2), Inches(0.75))
        tf_r = tx_right.text_frame
        tf_r.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_r = tf_r.paragraphs[0]
        p_r.text = "VSMSRKITE Nipani • Dept of CSE\nAffiliated to VTU Belagavi"
        p_r.font.size = Pt(10)
        p_r.font.bold = True
        p_r.font.color.rgb = C_SLATE_MUTED
        p_r.alignment = PP_ALIGN.RIGHT

    def add_footer(slide, current_slide, total_slides=15):
        bot_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(6.9), Inches(13.333), Inches(0.6))
        bot_bar.fill.solid()
        bot_bar.fill.fore_color.rgb = RGBColor(10, 15, 28)
        bot_bar.line.color.rgb = RGBColor(25, 36, 60)
        bot_bar.line.width = Pt(1)

        tx_bot = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(5.0), Inches(0.5))
        tf_b = tx_bot.text_frame
        p = tf_b.paragraphs[0]
        p.text = "SonicAttend • Proxy-Proof Acoustic Ultrasonic Attendance"
        p.font.size = Pt(10)
        p.font.color.rgb = C_SLATE_MUTED

        tx_cen = slide.shapes.add_textbox(Inches(5.0), Inches(6.95), Inches(5.0), Inches(0.5))
        tf_c = tx_cen.text_frame
        p_c = tf_c.paragraphs[0]
        p_c.text = "Pankaj M B • Laxmi S K • Laxmi L B"
        p_c.font.size = Pt(10)
        p_c.font.color.rgb = C_CYAN
        p_c.alignment = PP_ALIGN.CENTER

        tx_num = slide.shapes.add_textbox(Inches(11.0), Inches(6.95), Inches(1.5), Inches(0.5))
        tf_n = tx_num.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.text = f"Slide {current_slide} / {total_slides}"
        p_n.font.size = Pt(10)
        p_n.font.bold = True
        p_n.font.color.rgb = C_SLATE_MUTED
        p_n.alignment = PP_ALIGN.RIGHT

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_NAVY_DARK
        bg.line.fill.background()

    def add_card(slide, left, top, width, height, title="", border_color=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        if title:
            tx = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.5))
            tf = tx.text_frame
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = C_CYAN
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Accent decorative gradient line
    dec = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.9), Inches(11.733), Inches(0.06))
    dec.fill.solid()
    dec.fill.fore_color.rgb = C_CYAN
    dec.line.fill.background()

    # Logo if available
    if os.path.exists('logo.png'):
        try:
            s1.shapes.add_picture('logo.png', Inches(0.8), Inches(1.2), Inches(1.2), Inches(1.2))
        except Exception:
            pass

    # Institution
    tx_inst = s1.shapes.add_textbox(Inches(2.2), Inches(1.2), Inches(10.3), Inches(1.1))
    tf_i = tx_inst.text_frame
    p1 = tf_i.paragraphs[0]
    p1.text = "VSM'S S. R. KITTOOR INSTITUTE OF TECHNOLOGY, NIPANI"
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    p2 = tf_i.add_paragraph()
    p2.text = "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING\nAffiliated to Visvesvaraya Technological University (VTU), Belagavi"
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = C_SLATE_MUTED

    # Project Banner Box
    p_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.6), Inches(11.733), Inches(2.1))
    p_box.fill.solid()
    p_box.fill.fore_color.rgb = C_CARD_BG
    p_box.line.color.rgb = C_CYAN
    p_box.line.width = Pt(2)

    tx_proj = s1.shapes.add_textbox(Inches(1.1), Inches(2.75), Inches(11.1), Inches(1.8))
    tf_p = tx_proj.text_frame
    p_tag = tf_p.paragraphs[0]
    p_tag.text = "MINI PROJECT PRESENTATION • 5TH SEMESTER B.E. (BATCH 2026-27)"
    p_tag.font.size = Pt(12)
    p_tag.font.bold = True
    p_tag.font.color.rgb = C_EMERALD

    p_title = tf_p.add_paragraph()
    p_title.text = "SonicAttend: Proxy-Proof Inaudible Acoustic Ultrasonic FSK Attendance System"
    p_title.font.size = Pt(25)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WHITE

    p_sub = tf_p.add_paragraph()
    p_sub.text = "Zero-Hardware Classroom Presence Verification using Near-Ultrasound (18.2 - 19.8 kHz) & Rotating Cryptographic TOTP"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = C_CYAN

    # Team & Guide Cards
    add_card(s1, Inches(0.8), Inches(4.9), Inches(7.6), Inches(1.8), "PROJECT TEAM MEMBERS")
    tx_team = s1.shapes.add_textbox(Inches(1.0), Inches(5.4), Inches(7.2), Inches(1.2))
    tf_t = tx_team.text_frame
    members = [
        "1. Pankaj M Babaleshwar   (USN: 2VS24CS050)",
        "2. Laxmi S Koladur        (USN: 2VS24CS040)",
        "3. Laxmi L Biradar        (USN: 2VS24CS038)"
    ]
    for idx, m in enumerate(members):
        p = tf_t.paragraphs[0] if idx == 0 else tf_t.add_paragraph()
        p.text = m
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    add_card(s1, Inches(8.7), Inches(4.9), Inches(3.833), Inches(1.8), "PROJECT GUIDE")
    tx_guide = s1.shapes.add_textbox(Inches(8.9), Inches(5.4), Inches(3.4), Inches(1.2))
    tf_g = tx_guide.text_frame
    p_g1 = tf_g.paragraphs[0]
    p_g1.text = "Dept of Computer Science & Engg."
    p_g1.font.size = Pt(13)
    p_g1.font.bold = True
    p_g1.font.color.rgb = C_WHITE
    p_g2 = tf_g.add_paragraph()
    p_g2.text = "VSM's S. R. Kittoor Institute of Tech.\nNipani, Karnataka"
    p_g2.font.size = Pt(11)
    p_g2.font.color.rgb = C_SLATE_MUTED

    add_footer(s1, 1)

    # =========================================================================
    # SLIDE 2: AGENDA / TABLE OF CONTENTS
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "00", "Table of Contents & Presentation Outline")

    agenda_items = [
        ("01", "Introduction & Academic Context"),
        ("02", "Problem Statement & Vulnerabilities"),
        ("03", "Project Objectives & Scope"),
        ("04", "Literature Survey & Comparison Matrix"),
        ("05", "System Architecture & Security Protocols"),
        ("06", "Use Case Diagram & Actor Flow"),
        ("07", "Tools & Technologies Used"),
        ("08", "Software & Hardware Requirements"),
        ("09", "Step-by-Step Workflow & Data Flow"),
        ("10", "Expected Outcomes & Working Prototype"),
        ("11", "References & Conclusion")
    ]

    col1 = agenda_items[:6]
    col2 = agenda_items[6:]

    def build_agenda_col(items, left):
        for idx, (num, label) in enumerate(items):
            top = Inches(1.4 + idx * 0.88)
            card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(0.72))
            card.fill.solid()
            card.fill.fore_color.rgb = C_CARD_BG
            card.line.color.rgb = C_CARD_BORDER
            card.line.width = Pt(1)

            tx_n = s2.shapes.add_textbox(left + Inches(0.15), top + Inches(0.08), Inches(0.6), Inches(0.5))
            tf_n = tx_n.text_frame
            p_n = tf_n.paragraphs[0]
            p_n.text = num
            p_n.font.size = Pt(14)
            p_n.font.bold = True
            p_n.font.color.rgb = C_CYAN

            tx_l = s2.shapes.add_textbox(left + Inches(0.8), top + Inches(0.08), Inches(4.6), Inches(0.5))
            tf_l = tx_l.text_frame
            p_l = tf_l.paragraphs[0]
            p_l.text = label
            p_l.font.size = Pt(13)
            p_l.font.bold = True
            p_l.font.color.rgb = C_WHITE

    build_agenda_col(col1, Inches(0.8))
    build_agenda_col(col2, Inches(6.8))

    add_footer(s2, 2)

    # =========================================================================
    # SLIDE 3: 1. INTRODUCTION
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "01", "Introduction & Academic Background")

    add_card(s3, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.2), "THE ACADEMIC CONTEXT")
    tx_c1 = s3.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf_c1 = tx_c1.text_frame
    bullets_intro = [
        "Mandatory 75% VTU Attendance Rule: Visvesvaraya Technological University mandates minimum 75% attendance to qualify for semester examinations.",
        "Crucial Classroom Asset: Attendance reflects academic engagement and directly correlates with student pass percentages and accreditation norms.",
        "Inefficiency of Manual Roll Call: Traditional paper registers consume 10 to 15 minutes of every 60-minute lecture session.",
        "High Susceptibility to Proxies: Friends frequently answer for absentees, subverting official academic integrity."
    ]
    for idx, b in enumerate(bullets_intro):
        p = tf_c1.paragraphs[0] if idx == 0 else tf_c1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = C_SLATE_LIGHT
        p.space_after = Pt(12)

    add_card(s3, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.2), "THE SONICATTEND PARADIGM")
    tx_c2 = s3.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf_c2 = tx_c2.text_frame
    bullets_sonic = [
        "Inaudible Ultrasonic Audio: Operates between 18,200 Hz and 19,800 Hz—above human hearing thresholds but fully captured by standard mobile microphones.",
        "Physical Room Boundary Confinement: High-frequency sound waves cannot penetrate concrete classroom walls or glass windows, guaranteeing physical proximity.",
        "Zero Additional Hardware: Uses the teacher's existing laptop speakers and student smartphones without buying RFID readers, biometric scanners, or beacons.",
        "Web Audio API & Browser-Native: Runs directly in web browsers (Chrome, Edge, Safari)—zero mobile app installation required from app stores."
    ]
    for idx, b in enumerate(bullets_sonic):
        p = tf_c2.paragraphs[0] if idx == 0 else tf_c2.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = C_SLATE_LIGHT
        p.space_after = Pt(12)

    add_footer(s3, 3)

    # =========================================================================
    # SLIDE 4: 2. PROBLEM STATEMENT
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "02", "Problem Statement & Vulnerabilities")

    probs = [
        ("Paper Roll Call Vulnerability", "Takes 10–15 min per class. Widespread 'proxy attendance' by peer collusion. Paper registers suffer physical tearing and data loss.", C_GOLD),
        ("RFID Card Swapping Flaw", "Students carry multiple ID cards and tap for absent roommates. Hardware readers cost ₹5,000–₹15,000 per room and suffer card wear & tear.", C_GOLD),
        ("Biometric Bottlenecks & Delays", "Fingerprint / Face scanners create massive physical queues (60+ students). Unhygienic touch surfaces and high rejection rates on sweaty fingers.", C_GOLD),
        ("QR Code & GPS Spoofing Flaws", "Static/Dynamic QR codes are screenshotted and shared on WhatsApp to students in hostels. GPS apps spoof coordinates easily with fake mock locations.", C_GOLD)
    ]

    for idx, (title, desc, col) in enumerate(probs):
        r = idx // 2
        c = idx % 2
        left = Inches(0.8 + c * 6.0)
        top = Inches(1.4 + r * 2.65)
        add_card(s4, left, top, Inches(5.7), Inches(2.4), title, border_color=col)
        tx = s4.shapes.add_textbox(left + Inches(0.2), top + Inches(0.65), Inches(5.3), Inches(1.6))
        tf = tx.text_frame
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(13)
        p.font.color.rgb = C_SLATE_LIGHT
        p.space_after = Pt(8)

    add_footer(s4, 4)

    # =========================================================================
    # SLIDE 5: 3. OBJECTIVES
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "03", "Objectives of the Project")

    objs = [
        ("1. Zero Additional Hardware Cost", "Eliminate all external hardware expenditures by utilizing built-in laptop speakers for transmission and student smartphone microphones for reception."),
        ("2. Absolute Physical Room Verification", "Exploit physical acoustic attenuation—ultrasonic 19 kHz waves attenuate through concrete walls and doors, mathematically barring proxy from outside the hall."),
        ("3. Dynamic Cryptographic Token Rotation (TOTP)", "Implement 15-second rotating HMAC-SHA256 tokens over acoustic FSK, neutralizing replay attacks and recorded audio playback."),
        ("4. Strict 1-Device-to-1-USN Hardware Binding", "Generate persistent hardware device fingerprints upon registration; reject multi-account student logins on a single smartphone device."),
        ("5. Automated VTU Compliance & Audit Reporting", "Instantly generate official Visvesvaraya Technological University format attendance sheets with cryptographic verification signatures and quorum ratios.")
    ]

    for idx, (head, text) in enumerate(objs):
        top = Inches(1.35 + idx * 1.05)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.733), Inches(0.92))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_CYAN
        card.line.width = Pt(1.5)

        tx = s5.shapes.add_textbox(Inches(1.0), top + Inches(0.08), Inches(11.3), Inches(0.75))
        tf = tx.text_frame
        p1 = tf.paragraphs[0]
        p1.text = head
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = C_CYAN

        p2 = tf.add_paragraph()
        p2.text = text
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_SLATE_LIGHT

    add_footer(s5, 5)

    # =========================================================================
    # SLIDE 6: 4. LITERATURE SURVEY
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "04", "Literature Survey & Comparison Matrix")

    rows = 6
    cols = 6
    table_shape = s6.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.0))
    table = table_shape.table

    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(1.8)
    table.columns[2].width = Inches(1.8)
    table.columns[3].width = Inches(2.0)
    table.columns[4].width = Inches(1.9)
    table.columns[5].width = Inches(2.033)

    headers = ["Attendance System", "Extra Hardware", "Proxy Defense", "Processing Speed", "Queue Delay", "Spoof Immunity"]
    data = [
        ["Manual Paper Register", "None (Paper)", "Zero (Extreme Proxy)", "10 - 15 Minutes", "None (Disruptive)", "None (Fake Signatures)"],
        ["RFID Card Swapping", "RFID Reader + Cards", "Poor (Friend Tapping)", "2 - 3 Sec / Card", "Severe Entry Queue", "Low (Card Clones)"],
        ["Biometric Fingerprint", "Biometric Terminal", "Moderate (Late entry)", "3 - 5 Sec / Finger", "Critical Gate Jam", "Medium (Spoof molds)"],
        ["Static / Dynamic QR", "Printed / Screen QR", "Poor (WhatsApp share)", "5 - 8 Sec / Scan", "Medium (Crowding)", "Low (Image forward)"],
        ["SonicAttend (Proposed)", "NONE ($0 Extra)", "100% (Acoustic Barrier)", "< 2 Seconds Batch", "ZERO (Parallel Mic)", "100% (TOTP+HW Lock)"]
    ]

    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 41, 59)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_CYAN
        p.alignment = PP_ALIGN.CENTER

    for r_idx, row_vals in enumerate(data, 1):
        is_sonic = (r_idx == len(data))
        for c_idx, val in enumerate(row_vals):
            cell = table.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(16, 26, 48) if not is_sonic else RGBColor(6, 44, 48)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.bold = is_sonic
            p.font.color.rgb = C_EMERALD if is_sonic else C_SLATE_LIGHT
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT

    add_footer(s6, 6)

    # =========================================================================
    # SLIDE 7: 5. SYSTEM ARCHITECTURE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "05", "System Architecture & Acoustic Layer")

    tiers = [
        ("TIER 1: ACOUSTIC TRANSMITTER (TEACHER)", [
            "Web Audio API Oscillator Node: Synthesizes continuous sine wave at 19.25 kHz carrier frequency.",
            "Acoustic FSK Modulation: Frequency Shift Keying (18.5k, 18.8k, 19.0k, 19.5k, 19.8k Hz) encodes TOTP data bits.",
            "Sound Output: Plays via standard laptop stereo speakers with gain clamped to 0.12 (safe & inaudible)."
        ]),
        ("TIER 2: ACOUSTIC RECEIVER (STUDENT PHONE)", [
            "HTML5 getUserMedia: Secure microphone stream capture in mobile browser.",
            "512-Point Fast Fourier Transform (FFT): Real-time AnalyserNode extracts frequency magnitude bins.",
            "Acoustic Token Decoding: Isolates high-energy ultrasonic spike and decodes 4-character rotating token."
        ]),
        ("TIER 3: CRYPTOGRAPHIC BACKEND ENGINE", [
            "TOTP Cryptographic Generator: Computes HMAC-SHA256(SessionSeed, Floor(Timestamp / 15)).",
            "Hardware Fingerprint Verification: Checks USN against bound Hardware Device Signature in SQLite database.",
            "Grace Window Tolerance: Allows ±1 step (30s) drift tolerance to accommodate client clock variations."
        ]),
        ("TIER 4: ACID DATASTORE & VTU COMPLIANCE", [
            "SQLite Relational Storage: Atomic attendance logging (record_id, usn, session_id, timestamp, acoustic_token).",
            "VTU Belagavi Official Sheet Generator: Generates printable audit sheet with cryptographic SHA256 digest.",
            "Database Explorer Portal: Real-time live status inspection at /database with 1-click DB download."
        ])
    ]

    for idx, (title, items) in enumerate(tiers):
        r = idx // 2
        c = idx % 2
        left = Inches(0.8 + c * 6.0)
        top = Inches(1.4 + r * 2.65)
        add_card(s7, left, top, Inches(5.7), Inches(2.4), title)
        tx = s7.shapes.add_textbox(left + Inches(0.2), top + Inches(0.6), Inches(5.3), Inches(1.7))
        tf = tx.text_frame
        for b_idx, item in enumerate(items):
            p = tf.paragraphs[0] if b_idx == 0 else tf.add_paragraph()
            p.text = "• " + item
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_SLATE_LIGHT
            p.space_after = Pt(4)

    add_footer(s7, 7)

    # =========================================================================
    # SLIDE 8: 5. USE CASE DIAGRAM & ACTOR FLOW
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "05", "Use Case Analysis & Actor Interactions")

    actors = [
        ("FACULTY / LECTURER", [
            "UC-01: Faculty Authentication (Secure password & ID verification)",
            "UC-02: Start Classroom Session (Select Subject Code & Room No)",
            "UC-03: Broadcast Ultrasonic Beacon (19.25 kHz FSK tone activation)",
            "UC-04: View Live Real-Time Roster (Track attending student count)",
            "UC-05: Export Official VTU Attendance Sheet (PDF Printout generation)"
        ], C_CYAN),
        ("STUDENT ACTOR", [
            "UC-06: Student One-Time Registration (USN + Mobile + Device Binding)",
            "UC-07: Daily Student Login (Simple USN & Password credential check)",
            "UC-08: Activate Acoustic Radar (Grant temporary mic access via browser)",
            "UC-09: Local Ultrasonic Token Capture (512-pt FFT frequency detection)",
            "UC-10: Submit Verified Check-in (Token + Bound Device Hardware ID)"
        ], C_EMERALD),
        ("HOD / ACADEMIC AUDITOR", [
            "UC-11: Live Database Inspection (/database real-time explorer)",
            "UC-12: Download SQLite Database File (/api/db/download for audit)",
            "UC-13: Device Rebinding Verification (Approve device change tickets)",
            "UC-14: Audit Quorum & Percentage Compliance (VTU eligibility audit)"
        ], C_GOLD)
    ]

    for idx, (name, cases, col) in enumerate(actors):
        left = Inches(0.8 + idx * 4.0)
        top = Inches(1.4)
        add_card(s8, left, top, Inches(3.733), Inches(5.2), name, border_color=col)
        tx = s8.shapes.add_textbox(left + Inches(0.15), top + Inches(0.65), Inches(3.4), Inches(4.3))
        tf = tx.text_frame
        for c_idx, c_text in enumerate(cases):
            p = tf.paragraphs[0] if c_idx == 0 else tf.add_paragraph()
            p.text = "✔ " + c_text
            p.font.size = Pt(11)
            p.font.color.rgb = C_SLATE_LIGHT
            p.space_after = Pt(10)

    add_footer(s8, 8)

    # =========================================================================
    # SLIDE 9: 6. TOOLS USED
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "06", "Tools & Technologies Used")

    tools = [
        ("Backend Framework: Python Flask 3.0", "Provides lightweight, robust microframework architecture with RESTful JSON API endpoints, routing, session security, and clean URLs without .html extensions."),
        ("Relational Database: SQLite3 (ACID)", "Serverless, embedded relational database engine ensuring atomic transaction commits (conn.commit()) with zero complex configuration."),
        ("Acoustic Signal Engine: Web Audio API", "Hardware-accelerated W3C browser standard for synthesizing high-frequency carrier waveforms (OscillatorNode) and real-time FFT spectrum analysis (AnalyserNode)."),
        ("Frontend Architecture: TailwindCSS + ES6", "Modern, responsive mobile-first UI components styled with TailwindCSS utility framework, dynamic toast notification system, and asynchronous fetch() communication."),
        ("Cryptographic Engine: HMAC-SHA256 & TOTP", "RFC 6238 compliant 15-second rotating time-step token generation algorithm using standard Python hashlib and cryptographic secrets."),
        ("Deployment & DevOps: Render + Gunicorn", "High-performance production deployment powered by Gunicorn WSGI HTTP server running inside Linux cloud containers with automated GitHub continuous deployment.")
    ]

    for idx, (title, desc) in enumerate(tools):
        r = idx // 2
        c = idx % 2
        left = Inches(0.8 + c * 6.0)
        top = Inches(1.4 + r * 1.75)
        add_card(s9, left, top, Inches(5.7), Inches(1.55), title)
        tx = s9.shapes.add_textbox(left + Inches(0.2), top + Inches(0.55), Inches(5.3), Inches(0.9))
        tf = tx.text_frame
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = C_SLATE_LIGHT

    add_footer(s9, 9)

    # =========================================================================
    # SLIDE 10: 7. HARDWARE & SOFTWARE REQUIREMENTS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "07", "Hardware & Software Requirements")

    add_card(s10, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.2), "SOFTWARE REQUIREMENTS")
    tx_sw = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf_sw = tx_sw.text_frame
    sw_reqs = [
        "Operating System (Server): Linux (Ubuntu 22.04 LTS / Alpine), Windows 10/11, macOS.",
        "Operating System (Client): Android 8.0+, iOS 14.0+, Windows 10/11, macOS, ChromeOS.",
        "Web Browsers Supported: Google Chrome 90+, Microsoft Edge 90+, Apple Safari 14+, Mozilla Firefox 88+.",
        "Development Stack: Python 3.8 to 3.12, Flask >= 2.0.0, Gunicorn >= 20.1.0.",
        "Browser APIs Required: Web Audio API (AudioContext), MediaDevices (getUserMedia), LocalStorage."
    ]
    for idx, s in enumerate(sw_reqs):
        p = tf_sw.paragraphs[0] if idx == 0 else tf_sw.add_paragraph()
        p.text = "• " + s
        p.font.size = Pt(12)
        p.font.color.rgb = C_SLATE_LIGHT
        p.space_after = Pt(12)

    add_card(s10, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.2), "HARDWARE REQUIREMENTS (ZERO EXTRA COST)")
    tx_hw = s10.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf_hw = tx_hw.text_frame
    hw_reqs = [
        "Transmitter (Lecturer Station): Any standard Laptop or Desktop with standard built-in or external speakers (Frequency response up to 20,000 Hz).",
        "Receiver (Student Station): Any standard smartphone with built-in microphone (Standard MEMS microphone present in 100% of modern phones).",
        "Dedicated Attendance Hardware: ₹0.00 (Zero specialized biometric sensors, zero RFID readers, zero BLE beacons).",
        "Network Bandwidth: Minimal (~5 KB per attendance record submitted over campus Wi-Fi or cellular network)."
    ]
    for idx, h in enumerate(hw_reqs):
        p = tf_hw.paragraphs[0] if idx == 0 else tf_hw.add_paragraph()
        p.text = "• " + h
        p.font.size = Pt(12)
        p.font.color.rgb = C_SLATE_LIGHT
        p.space_after = Pt(12)

    add_footer(s10, 10)

    # =========================================================================
    # SLIDE 11: 8. WORKFLOW & STEP-BY-STEP EXECUTION
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "08", "System Workflow & Execution Sequence")

    steps = [
        ("Step 1: Session Initiation", "Teacher logs in on /faculty/login and clicks 'Start Broadcast' on /faculty/console, choosing Course Code and Room."),
        ("Step 2: Seed & TOTP Rotation", "Server seeds a cryptographic key and rotates a 15-second HMAC-SHA256 token (#8FF1, #7FCE, etc.)."),
        ("Step 3: Ultrasonic Tone Broadcast", "Laptop speakers play an inaudible 19.25 kHz acoustic wave throughout the classroom air space."),
        ("Step 4: Smartphone Microphone Capture", "Students open /attendance; browser requests microphone permission and captures audio stream via getUserMedia."),
        ("Step 5: In-Browser FFT Token Extraction", "Student phone runs a 512-point FFT, detects high-amplitude carrier frequency, and decodes the active token."),
        ("Step 6: Check-In Payload Transmission", "Student browser transmits JSON payload {usn, token, hardware_device_id} to /api/attendance/checkin."),
        ("Step 7: Server Validation & DB Commit", "Backend confirms token freshness (±15s window) and verifies hardware binding in SQLite datastore."),
        ("Step 8: Instant Verification & Roster Sync", "Attendance record is committed; Student UI displays 'Verified Ultrasonic' and teacher console updates live.")
    ]

    for idx, (title, desc) in enumerate(steps):
        r = idx // 2
        c = idx % 2
        left = Inches(0.8 + c * 6.0)
        top = Inches(1.35 + r * 1.35)
        add_card(s11, left, top, Inches(5.7), Inches(1.22), title)
        tx = s11.shapes.add_textbox(left + Inches(0.15), top + Inches(0.45), Inches(5.3), Inches(0.7))
        tf = tx.text_frame
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_SLATE_LIGHT

    add_footer(s11, 11)

    # =========================================================================
    # SLIDE 12: 9. EXPECTED OUTCOMES
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "09", "Expected Outcomes & Key Deliverables")

    outcomes = [
        ("1. Fully Working Live Prototype", "Successfully built and deployed live on Render Cloud (https://sonic-attendance.onrender.com) and locally on Python Flask.", C_CYAN),
        ("2. Sub-2 Second Batch Verification", "Class of 60 students completes presence verification simultaneously within seconds—saving 10–15 minutes of lecture time every hour.", C_CYAN),
        ("3. 100% Anti-Proxy Acoustic Containment", "Near-ultrasound waves (19.25 kHz) cannot penetrate closed doors or walls. Remote students in hostels or canteens cannot mark attendance.", C_EMERALD),
        ("4. One-Click Official VTU Audit Sheet Export", "Generates compliant printable audit sheets formatted specifically for Visvesvaraya Technological University Belagavi regulations.", C_EMERALD),
        ("5. Live Transparent Database Explorer", "Publicly verifiable SQLite database viewer at /database with 1-click full database download for external examiner audits.", C_GOLD),
        ("6. Hardware Fingerprint Device Binding", "Prevents single-phone multi-account proxy by locking each student USN permanently to their smartphone hardware signature.", C_GOLD)
    ]

    for idx, (title, desc, col) in enumerate(outcomes):
        r = idx // 2
        c = idx % 2
        left = Inches(0.8 + c * 6.0)
        top = Inches(1.4 + r * 1.75)
        add_card(s12, left, top, Inches(5.7), Inches(1.55), title, border_color=col)
        tx = s12.shapes.add_textbox(left + Inches(0.2), top + Inches(0.55), Inches(5.3), Inches(0.9))
        tf = tx.text_frame
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = C_SLATE_LIGHT

    add_footer(s12, 12)

    # =========================================================================
    # SLIDE 13: 10. REFERENCES
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "10", "References & Literature Citations")

    refs = [
        ("[1] M'Raihi, D., Machani, S., Pei, M., & Rydell, J.", "TOTP: Time-Based One-Time Password Algorithm", "Internet Engineering Task Force (IETF) RFC 6238, May 2011."),
        ("[2] Krawczyk, H., Bellare, M., & Canetti, R.", "HMAC: Keyed-Hashing for Message Authentication", "Internet Engineering Task Force (IETF) RFC 2104, February 1997."),
        ("[3] W3C Audio Working Group", "Web Audio API: W3C Recommendation", "World Wide Web Consortium (W3C), 2021. Available: https://www.w3.org/TR/webaudio/"),
        ("[4] Nandakumar, R., Chintalapudi, K. K., & Padmanabhan, V. N.", "Dhwani: Secure Peer-to-Peer Acoustic Communication", "ACM SIGCOMM Computer Communication Review, vol. 43, no. 4, pp. 63-74, 2013."),
        ("[5] Visvesvaraya Technological University (VTU)", "Regulations Governing the Degree of Bachelor of Engineering (B.E.) - Clause 18OB 6.1 (Attendance Requirements)", "VTU Belagavi Official Notification & Examination Guidelines, 2024.")
    ]

    for idx, (auth, title, src) in enumerate(refs):
        top = Inches(1.35 + idx * 1.05)
        card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.733), Inches(0.92))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_CARD_BORDER
        card.line.width = Pt(1)

        tx = s13.shapes.add_textbox(Inches(1.0), top + Inches(0.08), Inches(11.3), Inches(0.75))
        tf = tx.text_frame
        p1 = tf.paragraphs[0]
        p1.text = f"{auth} - \"{title}\""
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = C_CYAN

        p2 = tf.add_paragraph()
        p2.text = src
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_SLATE_LIGHT

    add_footer(s13, 13)

    # =========================================================================
    # SLIDE 14: 11. CONCLUSION & FUTURE ENHANCEMENTS
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "11", "Conclusion & Future Enhancements")

    add_card(s14, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.2), "PROJECT CONCLUSION")
    tx_co = s14.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf_co = tx_co.text_frame
    bullets_concl = [
        "Eradication of Proxy Attendance: Successfully demonstrated that near-ultrasound acoustic boundaries effectively eliminate peer proxy and buddy punching.",
        "Zero-Cost Implementation: Achieved automated attendance verification without procuring a single rupee of specialized biometric or RFID hardware.",
        "Significant Time Savings: Recovers 10–15 minutes of instructional lecture time every period across 60+ student batches.",
        "Academic & Regulatory Compliance: Fully integrated with official VTU format audit logs and cryptographic verification signatures."
    ]
    for idx, b in enumerate(bullets_concl):
        p = tf_co.paragraphs[0] if idx == 0 else tf_co.add_paragraph()
        p.text = "✔ " + b
        p.font.size = Pt(12)
        p.font.color.rgb = C_SLATE_LIGHT
        p.space_after = Pt(12)

    add_card(s14, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.2), "FUTURE ENHANCEMENTS")
    tx_fe = s14.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf_fe = tx_fe.text_frame
    bullets_future = [
        "VTU University Portal API Integration: Direct RESTful synchronization with VTU Belagavi centralized academic ERP servers.",
        "Multi-Frequency Spatial Beamforming: Implement MIMO acoustic array multiplexing for large tiered college auditoriums (200+ capacity).",
        "AI Noise Cancellation: On-device WebAssembly noise filtering to preserve decoding clarity in acoustically reverberant or noisy lab environments.",
        "Offline Cryptographic Sync: Enable offline presence recording using asymmetric public-key client certificates during internet outages."
    ]
    for idx, b in enumerate(bullets_future):
        p = tf_fe.paragraphs[0] if idx == 0 else tf_fe.add_paragraph()
        p.text = "★ " + b
        p.font.size = Pt(12)
        p.font.color.rgb = C_CYAN
        p.space_after = Pt(12)

    add_footer(s14, 14)

    # =========================================================================
    # SLIDE 15: THANK YOU / Q&A
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)

    add_card(s15, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1), "")
    tx_ty = s15.shapes.add_textbox(Inches(2.0), Inches(1.6), Inches(9.333), Inches(4.3))
    tf_ty = tx_ty.text_frame
    tf_ty.vertical_anchor = MSO_ANCHOR.MIDDLE

    p_t = tf_ty.paragraphs[0]
    p_t.text = "THANK YOU!"
    p_t.font.size = Pt(40)
    p_t.font.bold = True
    p_t.font.color.rgb = C_CYAN
    p_t.alignment = PP_ALIGN.CENTER

    p_q = tf_ty.add_paragraph()
    p_q.text = "Questions & Suggestions Are Welcome\n"
    p_q.font.size = Pt(20)
    p_q.font.color.rgb = C_WHITE
    p_q.alignment = PP_ALIGN.CENTER

    p_links = tf_ty.add_paragraph()
    p_links.text = "🌐 Live System URL: https://sonic-attendance.onrender.com\n💻 GitHub Repository: https://github.com/babaleshwar/Sonic-Attendance.git\n\nDepartment of Computer Science & Engineering\nVSM's S. R. Kittoor Institute of Technology, Nipani • VTU Belagavi"
    p_links.font.size = Pt(13)
    p_links.font.color.rgb = C_SLATE_LIGHT
    p_links.alignment = PP_ALIGN.CENTER

    add_footer(s15, 15)

    out_file = "SonicAttend_Mini_Project_Presentation.pptx"
    prs.save(out_file)
    print(f"Successfully generated PowerPoint presentation: {out_file}")

if __name__ == "__main__":
    create_presentation()
