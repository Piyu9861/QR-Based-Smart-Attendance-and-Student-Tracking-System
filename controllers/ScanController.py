from flask import request, render_template, session, redirect, jsonify
from models.AttendanceSessionModel import AttendanceSessionModel
from models.AttendanceModel import AttendanceModel
from models.StudentModel import StudentModel
from models.SubjectModel import SubjectModel
from models.AuthModel import AuthModel
from models.SmsModel import SmsModel
import datetime, math

# College location — K.P.Patil Institute, Mudal
COLLEGE_LAT  = 16.6913076
COLLEGE_LNG  = 74.2448662
COLLEGE_RADIUS_M = 500  # 500 metres radius

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2-lat1)
    dlam = math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

class ScanController:

    def scan(self):
        token = request.args.get('token')
        if not token:
            return render_template('scan/error.html',
                msg='Invalid QR code — no token found.',
                hint='Ask your teacher to generate a new QR code.')

        sess_model = AttendanceSessionModel()
        att_model  = AttendanceModel()
        qr_session = sess_model.get_by_token(token)

        if not qr_session:
            return render_template('scan/error.html',
                msg='QR session not found.',
                hint='This QR may have been deleted. Ask your teacher.')

        now = datetime.datetime.now()
        try:
            end_dt = qr_session['end_time']
            if isinstance(end_dt, str):
                end_dt = datetime.datetime.strptime(end_dt[:19], '%Y-%m-%d %H:%M:%S')
            if now > end_dt:
                return render_template('scan/error.html',
                    msg='QR code expired.',
                    hint=f'Expired at {end_dt.strftime("%I:%M %p")}. Ask teacher for new QR.')
        except:
            pass

        student_id = session.get('user_id')
        if not student_id or session.get('role') != 'student':
            return render_template('scan/login.html', token=token, error=None)

        already = att_model.already_marked(qr_session['id'], student_id)
        if already:
            student = StudentModel().get_by_id(student_id)
            return render_template('scan/already.html',
                student_name=session.get('name'), student=student,
                marked_at=str(already.get('marked_at','')))

        lat_str = request.args.get('lat', '')
        lng_str = request.args.get('lng', '')
        location_verified = 0
        location_msg = ''

        if lat_str and lng_str:
            try:
                lat, lng = float(lat_str), float(lng_str)
                dist = haversine(lat, lng, COLLEGE_LAT, COLLEGE_LNG)
                if dist <= COLLEGE_RADIUS_M:
                    location_verified = 1
                    location_msg = f'✅ Location verified ({int(dist)}m from college)'
                else:
                    location_msg = f'⚠️ Location outside college ({int(dist)}m away)'
            except:
                location_msg = 'Location check failed'

        data = {
            'session_id': qr_session['id'], 'student_id': student_id,
            'marked_at': now, 'latitude': lat_str, 'longitude': lng_str,
            'location_verified': location_verified
        }
        try:
            att_model.mark_attendance(data)
        except Exception as e:
            if 'Duplicate' in str(e):
                return render_template('scan/already.html',
                    student_name=session.get('name'), student=None, marked_at='')
            return render_template('scan/error.html', msg=f'Error: {e}', hint='Contact admin.')

        student     = StudentModel().get_by_id(student_id)
        subject_row = SubjectModel().get_by_id(qr_session.get('subject_id'))
        subject_name = subject_row['subject_name'] if subject_row else 'Class'

        try:
            SmsModel().send_attendance_sms(student, subject_name, now)
        except Exception as e:
            print(f'SMS/WhatsApp error: {e}')

        return render_template('scan/success.html',
            student=student, subject_name=subject_name,
            session_info=qr_session,
            marked_at=now.strftime('%d %b %Y, %I:%M %p'),
            location_msg=location_msg,
            location_verified=location_verified)

    def scan_login(self):
        token    = request.form.get('token')
        mobile   = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not mobile or not password:
            return render_template('scan/login.html', token=token,
                error='Please enter mobile number and password.')
        user = AuthModel().check_login('student', mobile, password)
        if user:
            session['user_id'] = user['id']
            session['name']    = user['name']
            session['role']    = 'student'
            session['dept_id'] = user.get('department_id')
            return redirect(f'/scan?token={token}')
        return render_template('scan/login.html', token=token,
            error='Invalid mobile or password. Default: Stud123')
