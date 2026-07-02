from flask import render_template, request, redirect, session, jsonify
from models.AttendanceSessionModel import AttendanceSessionModel
from models.ClassModel import ClassModel
from models.SubjectModel import SubjectModel
from models.AttendanceModel import AttendanceModel
from models.TeacherModel import TeacherModel
from models.DepartmentModel import DepartmentModel
import uuid, datetime, os

class AttendanceController:
    def __init__(self):
        self.model = AttendanceSessionModel()
        self.class_model = ClassModel()
        self.subject_model = SubjectModel()
        self.attendance_model = AttendanceModel()

    def index(self):
        if 'role' not in session:
            return redirect('/role-select')
        teacher_id = session.get('user_id')
        sessions = self.model.get_by_teacher(teacher_id)
        return render_template('dashboard/teacher.html',
            sessions=sessions,
            name=session.get('name'),
            stats={'sessions': len(sessions), 'today_sessions': 0},
            dept={}
        )

    def session_attendance(self):
        session_id = request.args.get('id')
        records = self.attendance_model.get_session_attendance(session_id)
        return jsonify(records)

    def create(self):
        if 'role' not in session:
            return redirect('/role-select')
        role = session.get('role')
        if role == 'teacher':
            dept_id = session.get('dept_id')
            classes = self.class_model.get_by_dept(dept_id) if dept_id else self.class_model.get_all()
            subjects = self.subject_model.get_by_dept(dept_id) if dept_id else self.subject_model.get_all()
        else:
            classes = self.class_model.get_all()
            subjects = self.subject_model.get_all()
        return render_template('admin/attendance_form.html',
            classes=classes, subjects=subjects)

    def generate_qr(self):
        if 'role' not in session:
            return jsonify({'error': 'Not logged in'}), 401

        class_id = request.form.get('class_id')
        subject_id = request.form.get('subject_id')
        duration = int(request.form.get('duration', 15))
        teacher_id = session.get('user_id', 1)

        if not class_id or not subject_id:
            return jsonify({'error': 'Class and subject are required'}), 400

        now = datetime.datetime.now()
        end_time = now + datetime.timedelta(minutes=duration)
        qr_token = str(uuid.uuid4())

        # Get the server's actual IP for QR URL
        host = request.host  # e.g., 192.168.1.5:5000
        qr_url = f"http://{host}/scan?token={qr_token}"

        try:
            import qrcode
            img = qrcode.make(qr_url)
            filename = f"{qr_token}.png"
            os.makedirs("static/qr", exist_ok=True)
            img.save(os.path.join("static/qr", filename))
        except Exception as e:
            print(f"QR generation error: {e}")
            filename = f"{qr_token}.png"

        data = {
            'class_id': class_id, 'subject_id': subject_id, 'teacher_id': teacher_id,
            'date': now.date(), 'start_time': now, 'end_time': end_time,
            'qr_token': qr_token, 'status': 'active', 'qr_image': filename
        }
        session_id = self.model.insert(data)
        return jsonify({
            'session_id': session_id, 'qr_token': qr_token,
            'qr_url': qr_url, 'qr_image': f'/static/qr/{filename}',
            'end_time': str(end_time), 'duration': duration,
            'expires_in': duration * 60
        })
