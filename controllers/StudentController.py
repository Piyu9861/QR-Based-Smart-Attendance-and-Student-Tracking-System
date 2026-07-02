from flask import render_template, request, redirect, session
from models.StudentModel import StudentModel
from models.DepartmentModel import DepartmentModel
from models.TeacherModel import TeacherModel

class StudentController:
    def __init__(self):
        self.model = StudentModel()
        self.dept_model = DepartmentModel()
        self.teacher_model = TeacherModel()

    def _is_class_teacher(self):
        """Return True if the logged-in teacher is a class teacher."""
        if session.get('role') != 'teacher':
            return False
        t = self.teacher_model.get_by_id(session.get('user_id'))
        return t and t.get('is_class_teacher') == 'yes'

    def _check(self):
        if 'role' not in session:
            return redirect('/role-select')
        role = session['role']
        if role in ['principal', 'hod']:
            return None
        if role == 'teacher' and self._is_class_teacher():
            return None
        return redirect('/dashboard')

    def _check_view_only(self):
        """For list/view pages: principal, hod, and class teachers allowed."""
        if 'role' not in session:
            return redirect('/role-select')
        role = session['role']
        if role in ['principal', 'hod']:
            return None
        if role == 'teacher' and self._is_class_teacher():
            return None
        return redirect('/dashboard')

    def index(self):
        r = self._check_view_only()
        if r: return r
        role = session.get('role')
        if role == 'hod':
            students = self.model.get_by_dept(session.get('dept_id'))
        elif role == 'teacher':
            # Class teacher sees students of their dept
            t = self.teacher_model.get_by_id(session.get('user_id'))
            students = self.model.get_by_dept(t.get('department_id')) if t else []
        else:
            students = self.model.get_all()
        depts = self.dept_model.get_all()
        return render_template('admin/student_list.html',
                               students=students, depts=depts, role=role)

    def create(self):
        r = self._check()
        if r: return r
        depts = self.dept_model.get_all()
        # Pre-select HOD's or class teacher's dept
        role = session.get('role')
        if role == 'hod':
            preselect_dept = session.get('dept_id')
        elif role == 'teacher':
            t = self.teacher_model.get_by_id(session.get('user_id'))
            preselect_dept = t.get('department_id') if t else None
        else:
            preselect_dept = None
        return render_template('admin/student_form.html',
                               depts=depts, student=None,
                               action='add', preselect_dept=preselect_dept)

    def store(self):
        r = self._check()
        if r: return r
        data = request.form.to_dict()
        try:
            self.model.insert(data)
        except Exception as e:
            depts = self.dept_model.get_all()
            return render_template('admin/student_form.html',
                                   depts=depts, student=None,
                                   action='add', error=str(e))
        return redirect('/students')

    def edit(self):
        r = self._check()
        if r: return r
        student = self.model.get_by_id(request.args.get('id'))
        depts = self.dept_model.get_all()
        return render_template('admin/student_form.html',
                               student=student, depts=depts, action='edit')

    def update(self):
        r = self._check()
        if r: return r
        id = request.form.get('id')
        data = request.form.to_dict()
        try:
            self.model.update(id, data)
        except Exception as e:
            student = self.model.get_by_id(id)
            depts = self.dept_model.get_all()
            return render_template('admin/student_form.html',
                                   student=student, depts=depts,
                                   action='edit', error=str(e))
        return redirect('/students')

    def delete(self):
        r = self._check()
        if r: return r
        self.model.delete(request.args.get('id'))
        return redirect('/students')
