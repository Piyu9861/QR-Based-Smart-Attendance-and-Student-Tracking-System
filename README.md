# K.P. Patil Institute — QR Smart Attendance System
## FINAL VERSION — 5 Departments

---

## 🚀 QUICK SETUP

### Step 1 — Install MySQL and create database
```
mysql -u root -p < qr_attendance_db_FINAL.sql
```

### Step 2 — Install Python dependencies
```
pip install -r requirements.txt
```

### Step 3 — Configure database password (if needed)
Edit `dbconfig.py` → change `password=''` to your MySQL password.

### Step 4 — Run the app
```
python app.py
```
Open browser: **http://localhost:5000**

---

## 🏛️ DEPARTMENTS (5)
| # | Department | Short Name |
|---|-----------|-----------|
| 1 | Artificial Intelligence & Machine Learning | AIML |
| 2 | Computer Engineering | COMP |
| 3 | Civil Engineering | CIVIL |
| 4 | Mechanical Engineering | MECH |
| 5 | Electrical Engineering | ELEC |

---

## 🔑 LOGIN CREDENTIALS

| Role | Username / Mobile | Password |
|------|------------------|----------|
| **Principal** | `snaik11` | `snaik11` |
| **HOD AIML** | `rohits6066` | `rohits6066` |
| **HOD COMP** | `anandp` | `anandp123` |
| **HOD CIVIL** | `sanjayk` | `sanjayk123` |
| **HOD MECH** | `rajeshs` | `rajeshs123` |
| **HOD ELEC** | `meerak` | `meerak123` |
| **Teacher (AIML)** | `priya@kppatil.edu` | `teacher123` |
| **Teacher (COMP)** | `vijay@kppatil.edu` | `teacher123` |
| **Teacher (CIVIL)** | `nana@kppatil.edu` | `teacher123` |
| **Teacher (MECH)** | `sunil@kppatil.edu` | `teacher123` |
| **Teacher (ELEC)** | `kavita@kppatil.edu` | `teacher123` |
| **Student (AIML)** | `9988770001` | `Stud123` |
| **Student (COMP)** | `9988770008` | `Stud123` |
 Principal:  spmore , spmore123
 AIML HOD: avadhut_aiml / avadhut123
COMP HOD: hod_comp / hodcomp123
CIVIL HOD: hod_civil / hodcivil123
MECH HOD: hod_mech / hodmech123
ELEC HOD: hod_elec / hodelec123
teacher: Email: digusuryawanshi@gmail.com
Password: teacher123  (all teachers)
Email:akshayhuddar108@gmail.com
student Mobile: 9988770089 ·  Password: Piyu_1234

---

## 📱 QR ATTENDANCE — HOW IT WORKS

1. **Teacher logs in** → clicks "Generate QR"
2. **Select class + subject + duration** → click Generate
3. **QR Code appears** with countdown timer
4. **Students scan** the QR with their phone
5. **Students login** on the scan page (mobile + Stud123)
6. **Attendance marked** automatically — can't scan twice!

---

## 🐛 BUGS FIXED IN THIS VERSION

1. ✅ Teacher login fixed (email OR username, not email OR mobile)
2. ✅ Student login fixed (mobile OR enrollment_no)
3. ✅ QR URL now auto-detects server IP (no hardcoded IP)
4. ✅ QR scan login page has proper POST handler (/scan-login)
5. ✅ Principal dashboard — all 5 dept cards working
6. ✅ Department model has short_name column
7. ✅ Student model has email column
8. ✅ DashboardModel fixed (no double-counting present/absent)
9. ✅ All templates present — no missing page errors

---

## 📁 PROJECT STRUCTURE
```
kppatil_system/
├── app.py                    # Main Flask app + all routes
├── dbconfig.py               # MySQL connection config
├── requirements.txt
├── qr_attendance_db_FINAL.sql  # Complete database with 5 depts
├── models/
│   ├── AuthModel.py
│   ├── DashboardModel.py
│   ├── StudentModel.py
│   ├── TeacherModel.py
│   ├── HodModel.py
│   ├── DepartmentModel.py
│   ├── SubjectModel.py
│   ├── ClassModel.py
│   ├── TimetableModel.py
│   ├── AttendanceModel.py
│   ├── AttendanceSessionModel.py
│   └── AcademicCalendarModel.py
├── controllers/
│   ├── AuthController.py
│   ├── DashboardController.py
│   ├── StudentController.py
│   ├── TeacherController.py
│   ├── HodController.py
│   ├── DepartmentController.py
│   ├── SubjectController.py
│   ├── TimetableController.py
│   ├── AttendanceController.py
│   ├── AcademicCalendarController.py
│   └── ScanController.py
├── templates/
│   ├── base.html             # Sidebar + topbar layout
│   ├── auth/
│   │   ├── role_select.html  # Landing page — choose role
│   │   └── login.html        # Login form (all roles)
│   ├── dashboard/
│   │   ├── principal.html    # Full college dashboard
│   │   ├── hod.html          # Department dashboard
│   │   ├── teacher.html      # QR + attendance teacher view
│   │   └── student.html      # Student attendance tracker
│   ├── admin/
│   │   ├── student_list.html / student_form.html
│   │   ├── teacher_list.html / teacher_form.html
│   │   ├── hod_list.html / hod_form.html
│   │   ├── department_list.html / department_form.html
│   │   ├── subject_list.html / subject_form.html
│   │   ├── timetable_list.html / timetable_form.html
│   │   ├── calendar_list.html / calendar_form.html
│   │   └── attendance_form.html
│   └── scan/
│       ├── login.html         # Student login via QR scan
│       ├── success.html       # Attendance marked OK
│       ├── already.html       # Already marked warning
│       └── error.html         # QR error / expired
└── static/
    └── qr/                    # Generated QR images stored here
```
