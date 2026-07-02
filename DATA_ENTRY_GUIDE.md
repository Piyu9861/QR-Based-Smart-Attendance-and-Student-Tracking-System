# 📊 K.P. Patil Institute — Database Data Entry Guide

---

## 🗂️ HOW TO FILL DATABASE DATA

### Method 1 — phpMyAdmin (Easiest for non-programmers)

1. Open browser → go to `http://localhost/phpmyadmin`
2. Select database: `qr_attendance_db`
3. Click any table → click **"Insert"** tab
4. Fill the fields → click **"Go"**

---

## 📋 TABLE-BY-TABLE GUIDE

---

### 1. `departments` — Add a Department
| Column | What to enter | Example |
|--------|--------------|---------|
| id | Leave blank (auto) | — |
| department_name | Full name | `Computer Engineering` |
| short_name | Short code | `COMP` |

**Via Web:** Login as Principal → click "Add Department"

---

### 2. `teachers` — Add a Teacher
| Column | What to enter | Example |
|--------|--------------|---------|
| name | Full name | `Priya Sharma` |
| email | Email (**used for login**) | `priya@kppatil.edu` |
| mobile | Mobile number | `8765432101` |
| department_id | Department number | `1` (AIML) |
| designation | Job title | `Professor` |
| joining_date | Date joined | `2018-06-01` |
| status | active / inactive | `active` |
| username | Login ID (optional) | `TCH001` |
| password | Login password | `teacher123` |
| subjects | Subjects taught | `Machine Learning,Python` |

**Via Web:** Login as Principal → Teachers → Add Teacher

---

### 3. `students` — Add a Student
| Column | What to enter | Example |
|--------|--------------|---------|
| roll_no | Class roll number | `01` |
| enrollment_no | University enroll no | `AIML301` |
| name | Full name | `Ankita Patil` |
| email | Student email | `ankita@gmail.com` |
| class | FY / SY / TY | `TY` |
| department_id | Department number | `1` |
| gender | Male/Female/Other | `Female` |
| category | OPEN/OBC/SC/ST | `OBC` |
| seat_type | Regular/DSY/Lateral | `Regular` |
| mobile | **Used for LOGIN** | `9988770001` |
| parent_mobile | Parent's mobile for SMS | `8898890001` |
| address | Home address | `Sangli` |
| blood_group | Blood group | `O+` |
| password | Login password | `Stud123` |
| mark_10th | 10th % marks | `88.50` |
| mark_sem1 | Sem 1 % | `79.00` |
| mark_sem2 | Sem 2 % | `82.00` |
| mark_sem3 | Sem 3 % | `77.00` |
| mark_sem4 | Sem 4 % | `80.00` |
| mark_sem5 | Sem 5 % | `75.00` |
| mark_sem6 | Sem 6 % | NULL (if not done yet) |

**Via Web:** Login as Principal/HOD → Students → Add Student

---

### 4. `hods` — Add a HOD
| Column | What to enter | Example |
|--------|--------------|---------|
| name | Full name | `Dr. Rohit Sarnaik` |
| email | Email | `rohit@kppatil.edu` |
| department_id | Department | `1` |
| username | **Used for login** | `rohits6066` |
| password | Password | `rohits6066` |

**Via Web:** Login as Principal → HODs → Add HOD

---

### 5. `classes` — Add a Class
| Column | What to enter | Example |
|--------|--------------|---------|
| class_name | FY / SY / TY | `TY` |
| division | Div A/B/C | `A` |
| department_id | Department | `1` |

**Note:** Classes are needed so teachers can select them in QR generation.

---

### 6. `subjects` — Add a Subject
| Column | What to enter | Example |
|--------|--------------|---------|
| subject_name | Subject name | `Machine Learning` |
| department_id | Department | `1` |
| semester | Sem number | `5` |
| class | FY/SY/TY | `TY` |

**Via Web:** Login as Principal → Subjects → Add Subject

---

## 📊 MARKS ENTRY (10th + Sem 1 to 6)

### Understanding marks fields:
```
mark_10th  → SSC / 10th board percentage (e.g. 88.50)
mark_sem1  → Semester 1 percentage (FY first semester)
mark_sem2  → Semester 2 percentage (FY second semester)
mark_sem3  → Semester 3 percentage (SY first semester)
mark_sem4  → Semester 4 percentage (SY second semester)
mark_sem5  → Semester 5 percentage (TY first semester)
mark_sem6  → Semester 6 percentage (TY second semester — final)
```

### Which class fills which sems:
| Student Class | Marks to fill |
|-------------|--------------|
| **FY** | mark_10th, mark_sem1 (sem2 after exams) |
| **SY** | mark_10th, mark_sem1, 2, 3 (sem4 after) |
| **TY** | mark_10th, mark_sem1 to 5 (sem6 after finals) |

### SQL to update marks:
```sql
UPDATE students SET
  mark_10th=88.50,
  mark_sem1=79.00,
  mark_sem2=82.00,
  mark_sem3=77.00,
  mark_sem4=80.00,
  mark_sem5=75.00
WHERE enrollment_no='AIML301';
```

---

## 📱 PARENT SMS — HOW IT WORKS

When a student scans QR and marks attendance:
1. System saves attendance to database
2. Automatically reads `parent_mobile` from student record
3. Sends SMS: *"Your ward Ankita attended Machine Learning on 27-Mar-2026 at 10:15 AM"*

### To enable REAL SMS (currently in demo/print mode):
Edit `models/SmsModel.py` → find `_send_sms()` method → uncomment one of:
- **Fast2SMS** (India, free tier): get API key from fast2sms.com
- **Twilio**: paid, international
- **MSG91**: Indian SMS gateway

---

## 🔑 DEFAULT LOGIN CREDENTIALS

| Role | Login ID | Password |
|------|---------|----------|
| Principal | `snaik11` | `snaik11` |
| HOD AIML | `rohits6066` | `rohits6066` |
| HOD COMP | `anandp` | `anandp123` |
| HOD CIVIL | `sanjayk` | `sanjayk123` |
| HOD MECH | `rajeshs` | `rajeshs123` |
| HOD ELEC | `meerak` | `meerak123` |
| Any Teacher | email (e.g. `priya@kppatil.edu`) | `teacher123` |
| Any Student | mobile (e.g. `9988770001`) | `Stud123` |

---

## 📡 QR ATTENDANCE — STEP BY STEP

### Teacher side:
1. Login as Teacher
2. Click **"Generate QR"** in top right or sidebar
3. Select **Class** + **Subject** + **Duration** (15 min default)
4. Click **"Generate QR Code"**
5. Show QR on projector or your phone screen

### Student side:
1. **Open camera** app on your Android/iPhone
2. **Point camera** at the QR code (no need to press anything)
3. A **link will pop up** at the top of the screen — **tap it**
4. Browser opens → login with your **mobile number + Stud123**
5. Attendance is **marked instantly** ✅
6. Parent gets **SMS notification**

### ⚠️ IMPORTANT:
- Teacher's laptop/PC and student phones must be on the **SAME Wi-Fi network** (college network)
- QR code expires after the selected duration (15 min default)
- A student can only scan **once** per session

---

## 🐛 TROUBLESHOOTING

| Problem | Solution |
|---------|---------|
| QR not scanning | Check both devices on same Wi-Fi |
| "Session not found" | QR expired, teacher must regenerate |
| Login failed (student) | Use mobile number, not email. Password = Stud123 |
| Login failed (teacher) | Use email address. Password = teacher123 |
| SMS not sending | Add API key in models/SmsModel.py |
| Database error | Check dbconfig.py MySQL password |
