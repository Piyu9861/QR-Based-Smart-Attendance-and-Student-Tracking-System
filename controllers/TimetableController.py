from flask import render_template, request, redirect, session
from models.TimetableModel import TimetableModel
from models.ClassModel import ClassModel
from models.SubjectModel import SubjectModel
from models.TeacherModel import TeacherModel

class TimetableController:
    def __init__(self):
        self.model = TimetableModel()

    def index(self):
        if 'role' not in session:
            return redirect('/role-select')
        timetable = self.model.get_all()
        return render_template('admin/timetable_list.html', timetable=timetable)

    def create(self):
        if 'role' not in session:
            return redirect('/role-select')
        classes = ClassModel().get_all()
        subjects = SubjectModel().get_all()
        teachers = TeacherModel().get_all()
        return render_template('admin/timetable_form.html', classes=classes, subjects=subjects, teachers=teachers)

    def store(self):
        if 'role' not in session:
            return redirect('/role-select')
        self.model.insert(request.form.to_dict())
        return redirect('/timetable')

    def delete(self):
        if 'role' not in session: return redirect('/role-select')
        id = request.args.get('id')
        self.model.delete(id)
        return redirect('/timetable')
