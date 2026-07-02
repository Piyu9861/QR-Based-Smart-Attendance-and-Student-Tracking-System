from flask import render_template, request, redirect, url_for
from models.ClassModel import ClassModel
from models.DepartmentModel import DepartmentModel

class ClassController:

    def __init__(self):
        self.model = ClassModel()
        self.dept_model = DepartmentModel()

    # LIST
    def index(self):
        classes = self.model.get_all()
        return render_template("admin/class_list.html", classes=classes)

    # CREATE
    def create(self):
        departments = self.dept_model.get_all()
        return render_template("admin/class_form.html", departments=departments)

    # STORE
    def store(self):
        data = {
            'class_name': request.form['class_name'],
            'division': request.form['division'],
            'department_id': request.form['department_id']
        }

        self.model.insert(data)
        return redirect(url_for('class_list', status='success'))

    # EDIT
    def edit(self):
        id = request.args.get('id')
        class_data = self.model.get_by_id(id)
        departments = self.dept_model.get_all()

        return render_template("admin/class_edit.html", class_data=class_data, departments=departments)

    # UPDATE
    def update(self):
        data = {
            'id': request.form['id'],
            'class_name': request.form['class_name'],
            'division': request.form['division'],
            'department_id': request.form['department_id']
        }

        self.model.update(data)
        return redirect(url_for('class_list', status='updated'))

    # DELETE
    def delete(self):
        id = request.args.get('id')
        self.model.delete(id)
        return redirect(url_for('class_list', status='deleted'))