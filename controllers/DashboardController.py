from flask import render_template, session, redirect, request, jsonify
from models.DashboardModel import DashboardModel
from models.StudentModel import StudentModel
from models.TeacherModel import TeacherModel
from models.HodModel import HodModel
from models.DepartmentModel import DepartmentModel
from models.SubjectModel import SubjectModel
from models.ClassModel import ClassModel
from models.TimetableModel import TimetableModel
from models.AttendanceModel import AttendanceModel
from models.AcademicCalendarModel import AcademicCalendarModel
import datetime

class DashboardController:

    def index(self):
        if 'role' not in session:
            return redirect('/role-select')
        role = session['role']
        name = session.get('name')
        model = DashboardModel()

        if role == 'principal':
            stats    = model.get_principal_stats()
            depts    = DepartmentModel().get_all()
            subjects = SubjectModel().get_all()
            return render_template('dashboard/principal.html',
                                   stats=stats, departments=depts, name=name, subjects=subjects)

        elif role == 'hod':
            dept_id  = session.get('dept_id')
            stats    = model.get_hod_stats(dept_id)
            dept     = DepartmentModel().get_by_id(dept_id)
            events   = AcademicCalendarModel().get_by_dept(dept_id)
            classes  = ClassModel().get_by_dept(dept_id)
            subjects = SubjectModel().get_by_dept(dept_id)
            return render_template('dashboard/hod.html',
                                   stats=stats, dept=dept, events=events,
                                   classes=classes, subjects=subjects, name=name)

        elif role == 'teacher':
            teacher_id      = session.get('user_id')
            dept_id         = session.get('dept_id')
            stats           = model.get_teacher_stats(teacher_id)
            dept            = DepartmentModel().get_by_id(dept_id) if dept_id else {}
            subjects        = SubjectModel().get_by_dept(dept_id) if dept_id else []
            classes         = ClassModel().get_by_dept(dept_id)   if dept_id else []
            is_class_teacher = (session.get('is_class_teacher') == 'yes')
            return render_template('dashboard/teacher.html',
                                   stats=stats, dept=dept,
                                   subjects=subjects, classes=classes,
                                   name=name, is_class_teacher=is_class_teacher)

        elif role == 'student':
            student_id = session.get('user_id')
            stats      = model.get_student_stats(student_id)
            student    = StudentModel().get_by_id(student_id)
            dept       = DepartmentModel().get_by_id(student.get('department_id')) if student else {}
            return render_template('dashboard/student.html',
                                   stats=stats, student=student, dept=dept, name=name)

        return redirect('/role-select')

    # ── Principal APIs ────────────────────────────────────
    def api_all_students(self):
        if session.get('role') != 'principal':
            return jsonify({'error':'Unauthorized'}), 403
        return jsonify(StudentModel().get_all_with_dept())

    def api_all_teachers(self):
        if session.get('role') != 'principal':
            return jsonify({'error':'Unauthorized'}), 403
        return jsonify(TeacherModel().get_all_with_dept())

    def api_all_hods(self):
        if session.get('role') != 'principal':
            return jsonify({'error':'Unauthorized'}), 403
        return jsonify(HodModel().get_all_with_dept())

    def api_department_dashboard(self, dept_id):
        if session.get('role') != 'principal':
            return jsonify({'error':'Unauthorized'}), 403
        return jsonify(DashboardModel().get_dept_full_dashboard(dept_id))

    def api_attendance_report(self):
        if session.get('role') not in ['principal','hod','teacher']:
            return jsonify({'error':'Unauthorized'}), 403
        date       = request.args.get('date', str(datetime.date.today()))
        dept_id    = request.args.get('dept_id','')
        teacher_id = request.args.get('teacher_id','')
        subject_id = request.args.get('subject_id','')
        class_name = request.args.get('class_name','')
        return jsonify(AttendanceModel().get_filtered_report(
            date, dept_id, teacher_id, subject_id, class_name))

    # ── HOD APIs ──────────────────────────────────────────
    def api_hod_class_students(self, cls):
        dept_id = session.get('dept_id')
        return jsonify(StudentModel().get_by_class_dept(cls, dept_id))

    def api_hod_teachers(self):
        dept_id = session.get('dept_id')
        return jsonify(TeacherModel().get_by_dept(dept_id))

    def api_hod_attendance(self):
        dept_id    = session.get('dept_id')
        date       = request.args.get('date', str(datetime.date.today()))
        teacher_id = request.args.get('teacher_id','')
        class_name = request.args.get('class_name','')
        subject_id = request.args.get('subject_id','')
        return jsonify(AttendanceModel().get_filtered_report(
            date, dept_id, teacher_id, subject_id, class_name))

    def api_hod_timetable(self, cls):
        dept_id = session.get('dept_id')
        return jsonify(TimetableModel().get_by_class_dept(cls, dept_id))

    def api_student_detail(self, student_id):
        if session.get('role') not in ['principal','hod']:
            return jsonify({'error':'Unauthorized'}), 403
        student = StudentModel().get_by_id(student_id)
        if not student:
            return jsonify({'error':'Not found'}), 404
        att = AttendanceModel().get_student_attendance(student_id)
        student['attendance'] = att
        return jsonify(student)

    # ── Teacher APIs ──────────────────────────────────────
    def api_teacher_attendance(self):
        teacher_id = session.get('user_id')
        date       = request.args.get('date', str(datetime.date.today()))
        class_name = request.args.get('class_name','')
        subject_id = request.args.get('subject_id','')
        return jsonify(AttendanceModel().get_teacher_filtered(
            teacher_id, date, class_name, subject_id))

    def api_teacher_subjects(self):
        dept_id = session.get('dept_id')
        return jsonify(SubjectModel().get_by_dept(dept_id))

    def api_teacher_classes(self):
        dept_id = session.get('dept_id')
        return jsonify(ClassModel().get_by_dept(dept_id))

    # ── Student API ───────────────────────────────────────
    def api_student_attendance(self):
        student_id = session.get('user_id')
        return jsonify(AttendanceModel().get_student_attendance(student_id))
