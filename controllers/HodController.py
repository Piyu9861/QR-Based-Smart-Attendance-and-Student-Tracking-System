from flask import render_template, request, redirect, session
from models.HodModel import HodModel
from models.DepartmentModel import DepartmentModel

class HodController:
    def __init__(self):
        self.model = HodModel()
        self.dept_model = DepartmentModel()

    def _check(self):
        if session.get('role') != 'principal':
            return redirect('/dashboard')
        return None

    def index(self):
        r = self._check()
        if r: return r
        hods = self.model.get_all_with_dept()
        return render_template('admin/hod_list.html', hods=hods)

    def create(self):
        r = self._check()
        if r: return r
        depts = self.dept_model.get_all()
        return render_template('admin/hod_form.html', depts=depts, hod=None, action='add')

    def store(self):
        r = self._check()
        if r: return r
        try:
            self.model.insert(request.form.to_dict())
        except Exception as e:
            depts = self.dept_model.get_all()
            return render_template('admin/hod_form.html', depts=depts, hod=None,
                                   action='add', error=str(e))
        return redirect('/hods')

    def edit(self):
        r = self._check()
        if r: return r
        id = request.args.get('id')
        hod = self.model.get_by_id(id)
        depts = self.dept_model.get_all()
        return render_template('admin/hod_form.html', hod=hod, depts=depts, action='edit')

    def update(self):
        r = self._check()
        if r: return r
        id = request.form.get('id')
        try:
            self.model.update(id, request.form.to_dict())
        except Exception as e:
            hod = self.model.get_by_id(id)
            depts = self.dept_model.get_all()
            return render_template('admin/hod_form.html', hod=hod, depts=depts,
                                   action='edit', error=str(e))
        return redirect('/hods')

    def delete(self):
        r = self._check()
        if r: return r
        self.model.delete(request.args.get('id'))
        return redirect('/hods')
