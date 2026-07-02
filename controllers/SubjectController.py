from flask import render_template, request, redirect, session
from models.SubjectModel import SubjectModel
from models.DepartmentModel import DepartmentModel

class SubjectController:
    def __init__(self):
        self.model = SubjectModel()

    def index(self):
        if 'role' not in session:
            return redirect('/role-select')
        subjects = self.model.get_all()
        depts = DepartmentModel().get_all()
        return render_template('admin/subject_list.html', subjects=subjects, depts=depts)

    def create(self):
        if 'role' not in session:
            return redirect('/role-select')
        depts = DepartmentModel().get_all()
        return render_template('admin/subject_form.html', depts=depts)

    def store(self):
        if 'role' not in session:
            return redirect('/role-select')
        self.model.insert(request.form.to_dict())
        return redirect('/subjects')

    def delete(self):
        if 'role' not in session: return redirect('/role-select')
        self.model.delete(request.args.get('id'))
        return redirect('/subjects')
