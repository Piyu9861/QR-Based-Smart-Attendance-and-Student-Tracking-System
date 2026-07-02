from flask import session, redirect, Response, request, render_template, jsonify
from models.AttendanceModel import AttendanceModel
from models.StudentModel import StudentModel
import io, csv, datetime, os

class ExportController:

    def export_attendance_csv(self):
        if session.get('role') not in ['principal','hod','teacher']:
            return redirect('/dashboard')
        date       = request.args.get('date', str(datetime.date.today()))
        dept_id    = request.args.get('dept_id','')
        class_name = request.args.get('class_name','')
        rows = AttendanceModel().get_all_for_export(date, dept_id, class_name)

        out = io.StringIO()
        w   = csv.writer(out)
        w.writerow(['Roll No','Student Name','Year','Department','Subject',
                    'Teacher','Date','Time','Status','Location Verified'])
        for r in rows:
            w.writerow([
                r.get('roll_no',''), r.get('student_name',''),
                r.get('student_class',''), r.get('department_name',''),
                r.get('subject_name',''), r.get('teacher_name',''),
                r.get('date',''), r.get('time',''),
                r.get('status','present'),
                'Yes' if r.get('location_verified') else 'No'
            ])
        out.seek(0)
        fname = f"KPPatil_Attendance_{date or 'all'}.csv"
        return Response(out.getvalue(), mimetype='text/csv',
                        headers={'Content-Disposition': f'attachment; filename={fname}'})

    def export_attendance_html_print(self):
        if session.get('role') not in ['principal','hod','teacher']:
            return redirect('/dashboard')
        date       = request.args.get('date', str(datetime.date.today()))
        dept_id    = request.args.get('dept_id','')
        class_name = request.args.get('class_name','')
        rows = AttendanceModel().get_all_for_export(date, dept_id, class_name)
        return render_template('admin/attendance_print.html',
            rows=rows, date=date, dept_id=dept_id, class_name=class_name,
            generated_at=datetime.datetime.now().strftime('%d %b %Y, %I:%M %p'))

    # ── PDF / Excel Import → Database ───────────────────
    def import_page(self):
        """Show PDF/Excel import page"""
        if session.get('role') not in ['principal','hod']:
            return redirect('/dashboard')
        return render_template('admin/import_data.html')

    def import_students_csv(self):
        """
        Import students from uploaded CSV/Excel file into database.
        Expected CSV columns: roll_no, enrollment_no, name, email, class,
        mobile, parent_mobile, category, gender, mark_10th, mark_sem1..6
        """
        if session.get('role') not in ['principal','hod']:
            return redirect('/dashboard')

        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        f = request.files['file']
        if not f.filename:
            return jsonify({'error': 'No file selected'}), 400

        dept_id = session.get('dept_id') or request.form.get('dept_id')

        try:
            content = f.read().decode('utf-8-sig')  # handles BOM
            reader  = csv.DictReader(io.StringIO(content))
            model   = StudentModel()
            success, errors = 0, []

            for i, row in enumerate(reader, 2):  # row 2 = first data row
                try:
                    # Normalize column names (case-insensitive)
                    data = {k.strip().lower().replace(' ','_'): v.strip() for k,v in row.items()}

                    # Map common column names
                    student_data = {
                        'roll_no':       data.get('roll_no') or data.get('roll no') or '',
                        'enrollment_no': data.get('enrollment_no') or data.get('enroll no') or data.get('enrollment no') or '',
                        'name':          data.get('name') or data.get('student name') or data.get('student_name') or '',
                        'email':         data.get('email') or '',
                        'class':         data.get('class') or data.get('year') or data.get('semester') or '1st Year',
                        'department_id': data.get('department_id') or dept_id or 1,
                        'gender':        data.get('gender') or 'Male',
                        'category':      data.get('category') or 'OPEN',
                        'seat_type':     data.get('seat_type') or data.get('seat type') or 'Regular',
                        'mobile':        data.get('mobile') or data.get('mobile no') or '',
                        'parent_mobile': data.get('parent_mobile') or data.get('parent mobile') or '',
                        'address':       data.get('address') or '',
                        'blood_group':   data.get('blood_group') or data.get('blood group') or '',
                        'password':      data.get('password') or 'Stud123',
                        'mark_10th':     data.get('mark_10th') or data.get('10th') or data.get('10th marks') or '',
                        'mark_sem1':     data.get('mark_sem1') or data.get('sem1') or data.get('sem 1') or '',
                        'mark_sem2':     data.get('mark_sem2') or data.get('sem2') or data.get('sem 2') or '',
                        'mark_sem3':     data.get('mark_sem3') or data.get('sem3') or data.get('sem 3') or '',
                        'mark_sem4':     data.get('mark_sem4') or data.get('sem4') or data.get('sem 4') or '',
                        'mark_sem5':     data.get('mark_sem5') or data.get('sem5') or data.get('sem 5') or '',
                        'mark_sem6':     data.get('mark_sem6') or data.get('sem6') or data.get('sem 6') or '',
                    }

                    if not student_data['name'] or not student_data['mobile']:
                        errors.append(f"Row {i}: Name or Mobile missing — skipped")
                        continue

                    # Normalize class name
                    cls = student_data['class'].strip()
                    cls_map = {
                        'fy':'1st Year','sy':'2nd Year','ty':'3rd Year',
                        'first year':'1st Year','second year':'2nd Year','third year':'3rd Year',
                        'sem1':'1st Year','sem2':'1st Year','sem3':'2nd Year',
                        'sem4':'2nd Year','sem5':'3rd Year','sem6':'3rd Year',
                        '1':'1st Year','2':'2nd Year','3':'3rd Year',
                    }
                    student_data['class'] = cls_map.get(cls.lower(), cls)

                    model.insert(student_data)
                    success += 1
                except Exception as e:
                    errors.append(f"Row {i}: {str(e)}")

            return jsonify({
                'success': success,
                'errors':  errors,
                'message': f'{success} students imported successfully. {len(errors)} errors.'
            })

        except Exception as e:
            return jsonify({'error': f'File processing error: {str(e)}'}), 500
