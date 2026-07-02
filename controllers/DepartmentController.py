from flask import render_template, request, redirect, session
from models.DepartmentModel import DepartmentModel

class DepartmentController:
    def __init__(self):
        self.model = DepartmentModel()

    def index(self):
        if session.get('role') != 'principal':
            return redirect('/dashboard')
        depts = self.model.get_all()
        return render_template('admin/department_list.html', depts=depts)

    def create(self):
        if session.get('role') != 'principal':
            return redirect('/dashboard')
        return render_template('admin/department_form.html')

    def store(self):
        if session.get('role') != 'principal':
            return redirect('/dashboard')
        data = request.form.to_dict()
        self.model.insert(data)
        return redirect('/departments')
