from flask import render_template, request, redirect, session
from models.TeacherModel import TeacherModel
from models.DepartmentModel import DepartmentModel

class TeacherController:
    def __init__(self):
        self.model = TeacherModel()
        self.dept_model = DepartmentModel()

    def _check(self):
        if 'role' not in session:
            return redirect('/role-select')
        if session['role'] not in ['principal', 'hod']:
            return redirect('/dashboard')
        return None

    def index(self):
        r = self._check()
        if r: return r
        role = session.get('role')
        if role == 'hod':
            teachers = self.model.get_by_dept(session.get('dept_id'))
        else:
            teachers = self.model.get_all()
        depts = self.dept_model.get_all()
        return render_template('admin/teacher_list.html',
                               teachers=teachers, depts=depts, role=role)

    def create(self):
        r = self._check()
        if r: return r
        depts = self.dept_model.get_all()
        preselect_dept = session.get('dept_id') if session.get('role') == 'hod' else None
        return render_template('admin/teacher_form.html',
                               teacher=None, depts=depts,
                               action='add', preselect_dept=preselect_dept)

    def store(self):
        r = self._check()
        if r: return r
        data = request.form.to_dict()
        try:
            self.model.insert(data)
        except Exception as e:
            depts = self.dept_model.get_all()
            return render_template('admin/teacher_form.html',
                                   teacher=None, depts=depts,
                                   action='add', error=str(e))
        return redirect('/teachers')

    def edit(self):
        r = self._check()
        if r: return r
        teacher = self.model.get_by_id(request.args.get('id'))
        depts = self.dept_model.get_all()
        return render_template('admin/teacher_form.html',
                               teacher=teacher, depts=depts, action='edit')

    def update(self):
        r = self._check()
        if r: return r
        id = request.form.get('id')
        data = request.form.to_dict()
        try:
            self.model.update(id, data)
        except Exception as e:
            teacher = self.model.get_by_id(id)
            depts = self.dept_model.get_all()
            return render_template('admin/teacher_form.html',
                                   teacher=teacher, depts=depts,
                                   action='edit', error=str(e))
        return redirect('/teachers')

    def delete(self):
        r = self._check()
        if r: return r
        self.model.delete(request.args.get('id'))
        return redirect('/teachers')
