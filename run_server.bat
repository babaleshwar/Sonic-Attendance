@echo off
title SonicAttend Ultrasonic Attendance Platform - VSMSRKITE Nipani
echo ======================================================================
echo  SONICATTEND BACKEND ENGINE - VSMSRKITE NIPANI
echo  Proxy-Proof Inaudible Acoustic Attendance Platform
echo ======================================================================
echo.
echo Starting Flask Server on http://127.0.0.1:5000 ...
echo.
echo Open in your browser:
echo  - Home Hub:         http://127.0.0.1:5000/
echo  - Lecturer Portal:  http://127.0.0.1:5000/lecturer_login.html
echo  - Student Portal:   http://127.0.0.1:5000/login.html
echo  - Live Attendance:  http://127.0.0.1:5000/student_attendance.html
echo ======================================================================
echo.
python app.py
pause

