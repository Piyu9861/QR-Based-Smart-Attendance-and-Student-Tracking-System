from flask import render_template, request, redirect, session
from models.AcademicCalendarModel import AcademicCalendarModel
from models.DepartmentModel import DepartmentModel

class AcademicCalendarController:
    def __init__(self):
        self.model = AcademicCalendarModel()

    def index(self):
        if 'role' not in session: return redirect('/role-select')
        role = session.get('role')
        dept_id = session.get('dept_id')
        if role == 'hod':
            events = self.model.get_by_dept(dept_id)
        else:
            events = self.model.get_all()
        return render_template('admin/calendar_list.html', events=events)

    def create(self):
        if 'role' not in session: return redirect('/role-select')
        depts = DepartmentModel().get_all()
        session_dept = session.get('dept_id')
        return render_template('admin/calendar_form.html', depts=depts, session_dept=session_dept)

    def store(self):
        if 'role' not in session: return redirect('/role-select')
        data = request.form.to_dict()
        # HOD can only add for their dept or all
        if session.get('role') == 'hod' and not data.get('department_id'):
            data['department_id'] = session.get('dept_id')
        self.model.insert(data)
        return redirect('/calendar')

    def delete(self):
        if 'role' not in session: return redirect('/role-select')
        self.model.delete(request.args.get('id'))
        return redirect('/calendar')
