"""
K.P. Patil Institute of Technology (Polytechnic), Mudal
QR Smart Attendance System — Flask App
Principal: Mr. S.P. More | AIML HOD: Mr. Avadhut Patil
"""
from flask import Flask, session, redirect, jsonify

app = Flask(__name__)
app.secret_key = 'kppatil_mudal_2026_secure_key'

# ── Helper: import controller fresh per request ──────────────
def _auth():
    from controllers.AuthController import AuthController
    return AuthController()

def _dash():
    from controllers.DashboardController import DashboardController
    return DashboardController()

def _stud():
    from controllers.StudentController import StudentController
    return StudentController()

def _tch():
    from controllers.TeacherController import TeacherController
    return TeacherController()

def _hod():
    from controllers.HodController import HodController
    return HodController()

def _dept():
    from controllers.DepartmentController import DepartmentController
    return DepartmentController()

def _att():
    from controllers.AttendanceController import AttendanceController
    return AttendanceController()

def _tt():
    from controllers.TimetableController import TimetableController
    return TimetableController()

def _cal():
    from controllers.AcademicCalendarController import AcademicCalendarController
    return AcademicCalendarController()

def _subj():
    from controllers.SubjectController import SubjectController
    return SubjectController()

def _scan():
    from controllers.ScanController import ScanController
    return ScanController()

def _exp():
    from controllers.ExportController import ExportController
    return ExportController()

# ── AUTH ─────────────────────────────────────────────────────
@app.route('/')
def home(): return redirect('/role-select')

@app.route('/role-select')
def role_select(): return _auth().role_select()

@app.route('/login/<role>')
def login(role): return _auth().login(role)

@app.route('/login-auth', methods=['POST'])
def login_auth(): return _auth().login_auth()

@app.route('/logout')
def logout(): return _auth().logout()

# ── DASHBOARD ────────────────────────────────────────────────
@app.route('/dashboard')
def dashboard(): return _dash().index()

@app.route('/api/principal/students')
def api_principal_students(): return _dash().api_all_students()

@app.route('/api/principal/teachers')
def api_principal_teachers(): return _dash().api_all_teachers()

@app.route('/api/principal/hods')
def api_principal_hods(): return _dash().api_all_hods()

@app.route('/api/principal/department/<int:dept_id>')
def api_principal_dept(dept_id): return _dash().api_department_dashboard(dept_id)

@app.route('/api/principal/attendance')
def api_principal_att(): return _dash().api_attendance_report()

@app.route('/api/hod/students/<cls>')
def api_hod_students(cls): return _dash().api_hod_class_students(cls)

@app.route('/api/hod/teachers')
def api_hod_tch(): return _dash().api_hod_teachers()

@app.route('/api/hod/attendance')
def api_hod_att(): return _dash().api_hod_attendance()

@app.route('/api/hod/timetable/<cls>')
def api_hod_tt(cls): return _dash().api_hod_timetable(cls)

@app.route('/api/hod/student/<int:sid>')
def api_hod_stud(sid): return _dash().api_student_detail(sid)

@app.route('/api/teacher/attendance')
def api_tch_att(): return _dash().api_teacher_attendance()

@app.route('/api/teacher/subjects')
def api_tch_subj(): return _dash().api_teacher_subjects()

@app.route('/api/teacher/classes')
def api_tch_cls(): return _dash().api_teacher_classes()

@app.route('/api/student/attendance')
def api_stud_att(): return _dash().api_student_attendance()

# ── STUDENTS ─────────────────────────────────────────────────
@app.route('/students')
def student_list(): return _stud().index()

@app.route('/students/add')
def student_add(): return _stud().create()

@app.route('/students/store', methods=['POST'])
def student_store(): return _stud().store()

@app.route('/students/edit')
def student_edit(): return _stud().edit()

@app.route('/students/update', methods=['POST'])
def student_update(): return _stud().update()

@app.route('/students/delete')
def student_delete(): return _stud().delete()

# ── TEACHERS ─────────────────────────────────────────────────
@app.route('/teachers')
def teacher_list(): return _tch().index()

@app.route('/teachers/add')
def teacher_add(): return _tch().create()

@app.route('/teachers/store', methods=['POST'])
def teacher_store(): return _tch().store()

@app.route('/teachers/edit')
def teacher_edit(): return _tch().edit()

@app.route('/teachers/update', methods=['POST'])
def teacher_update(): return _tch().update()

@app.route('/teachers/delete')
def teacher_delete(): return _tch().delete()

# ── HODS ─────────────────────────────────────────────────────
@app.route('/hods')
def hod_list(): return _hod().index()

@app.route('/hods/add')
def hod_add(): return _hod().create()

@app.route('/hods/store', methods=['POST'])
def hod_store(): return _hod().store()

@app.route('/hods/edit')
def hod_edit(): return _hod().edit()

@app.route('/hods/update', methods=['POST'])
def hod_update(): return _hod().update()

@app.route('/hods/delete')
def hod_delete(): return _hod().delete()

# ── DEPARTMENTS ──────────────────────────────────────────────
@app.route('/departments')
def dept_list(): return _dept().index()

@app.route('/departments/add')
def dept_add(): return _dept().create()

@app.route('/departments/store', methods=['POST'])
def dept_store(): return _dept().store()

# ── ATTENDANCE ───────────────────────────────────────────────
@app.route('/attendance')
def att_list(): return _att().index()

@app.route('/attendance/create')
def att_create(): return _att().create()

@app.route('/attendance/generate-qr', methods=['POST'])
def att_gen_qr(): return _att().generate_qr()

@app.route('/attendance/session')
def att_session(): return _att().session_attendance()

# ── QR SCAN ──────────────────────────────────────────────────
@app.route('/scan')
def scan(): return _scan().scan()

@app.route('/scan-login', methods=['POST'])
def scan_login(): return _scan().scan_login()

# ── TIMETABLE ────────────────────────────────────────────────
@app.route('/timetable')
def tt_list(): return _tt().index()

@app.route('/timetable/add')
def tt_add(): return _tt().create()

@app.route('/timetable/store', methods=['POST'])
def tt_store(): return _tt().store()

@app.route('/timetable/delete')
def tt_delete(): return _tt().delete()

# ── CALENDAR ─────────────────────────────────────────────────
@app.route('/calendar')
def cal_list(): return _cal().index()

@app.route('/calendar/add')
def cal_add(): return _cal().create()

@app.route('/calendar/store', methods=['POST'])
def cal_store(): return _cal().store()

@app.route('/calendar/delete')
def cal_delete(): return _cal().delete()

# ── SUBJECTS ─────────────────────────────────────────────────
@app.route('/subjects')
def subj_list(): return _subj().index()

@app.route('/subjects/add')
def subj_add(): return _subj().create()

@app.route('/subjects/store', methods=['POST'])
def subj_store(): return _subj().store()

@app.route('/subjects/delete')
def subj_delete(): return _subj().delete()

# ── EXPORT ───────────────────────────────────────────────────
@app.route('/export/attendance-csv')
def exp_csv(): return _exp().export_attendance_csv()

@app.route('/export/attendance-print')
def exp_print(): return _exp().export_attendance_html_print()

# ── SMS LOG ──────────────────────────────────────────────────
@app.route('/sms-log')
def sms_log():
    if session.get('role') not in ['principal','hod','teacher']:
        return redirect('/dashboard')
    from models.SmsModel import SmsModel
    from flask import render_template
    return render_template('admin/sms_log.html',
                           logs=SmsModel().get_recent_logs(100))

# ── UTILS ─────────────────────────────────────────────────────
@app.route('/api/server-ip')
def server_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]; s.close()
    except:
        ip = "127.0.0.1"
    return jsonify({'ip': ip})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# ── IMPORT DATA ───────────────────────────────────────────────
@app.route('/import')
def import_page():
    if session.get('role') not in ['principal','hod']:
        return redirect('/dashboard')
    from models.DepartmentModel import DepartmentModel
    from flask import render_template
    depts = DepartmentModel().get_all()
    return render_template('admin/import_data.html', depts=depts)

@app.route('/import/students', methods=['POST'])
def import_students():
    return _exp().import_students_csv()

# ── ABSENT NOTIFICATION ───────────────────────────────────────
@app.route('/api/notify-absent', methods=['POST'])
def notify_absent():
    if session.get('role') not in ['teacher','hod','principal']:
        from flask import jsonify
        return jsonify({'error':'Unauthorized'}), 403
    from flask import jsonify, request as req
    from models.StudentModel import StudentModel
    from models.SmsModel import SmsModel
    import datetime

    student_id   = req.json.get('student_id')
    subject_name = req.json.get('subject_name', 'class')
    date_str     = req.json.get('date', str(datetime.date.today()))

    student = StudentModel().get_by_id(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    try:
        SmsModel().send_absent_alert(student, subject_name, date_str)
        return jsonify({
            'success': True,
            'message': f"Notification sent to parent of {student['name']} ({student.get('parent_mobile','—')})"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── BULK ABSENT NOTIFICATION ──────────────────────────────────
@app.route('/api/notify-all-absent', methods=['POST'])
def notify_all_absent():
    if session.get('role') not in ['teacher','hod','principal']:
        from flask import jsonify
        return jsonify({'error':'Unauthorized'}), 403
    from flask import jsonify, request as req
    from models.AttendanceModel import AttendanceModel
    from models.StudentModel import StudentModel
    from models.SmsModel import SmsModel
    import datetime

    session_id   = req.json.get('session_id')
    subject_name = req.json.get('subject_name', 'class')
    date_str     = req.json.get('date', str(datetime.date.today()))

    att_rows = AttendanceModel().get_session_attendance(session_id)
    absent   = [r for r in att_rows if not r.get('is_present')]

    sent, errors = 0, []
    sms = SmsModel()
    stud_model = StudentModel()
    for row in absent:
        try:
            student = stud_model.get_by_id(row['id'])
            if student and student.get('parent_mobile'):
                sms.send_absent_alert(student, subject_name, date_str)
                sent += 1
        except Exception as e:
            errors.append(str(e))

    return jsonify({
        'success': True,
        'sent':    sent,
        'absent':  len(absent),
        'message': f"Notified {sent} parents of absent students"
    })
