from flask import render_template, request, redirect, session
from models.AuthModel import AuthModel

class AuthController:

    def role_select(self):
        return render_template('auth/role_select.html')

    def login(self, role):
        return render_template('auth/login.html', role=role)

    def login_auth(self):
        role     = request.form.get('role', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not role or not username or not password:
            return render_template('auth/login.html', role=role,
                                   error='Please fill all fields.')

        try:
            # Fresh model per request — avoids stale connection issues
            auth_model = AuthModel()
            user = auth_model.check_login(role, username, password)
        except Exception as e:
            return render_template('auth/login.html', role=role,
                                   error=f'Database error: {e}')

        if user:
            session.clear()
            session['user_id']  = user['id']
            session['name']     = user.get('name', 'User')
            session['role']     = role
            session['dept_id']  = user.get('department_id')
            # For teachers, store class teacher status in session
            if role == 'teacher':
                session['is_class_teacher'] = user.get('is_class_teacher', 'no')
            return redirect('/dashboard')

        return render_template('auth/login.html', role=role,
                               error='Invalid username or password. Please check credentials.')

    def logout(self):
        session.clear()
        return redirect('/role-select')
