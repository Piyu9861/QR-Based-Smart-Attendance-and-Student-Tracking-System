from dbconfig import get_db_connection
import datetime

class DashboardModel:

    def _conn(self):
        c = get_db_connection()
        return c, c.cursor(dictionary=True)

    def get_principal_stats(self):
        conn, cur = self._conn()
        try:
            stats = {}
            for key, sql in [
                ('departments', "SELECT COUNT(*) as c FROM departments"),
                ('hods',        "SELECT COUNT(*) as c FROM hods"),
                ('teachers',    "SELECT COUNT(*) as c FROM teachers WHERE status='active'"),
                ('students',    "SELECT COUNT(*) as c FROM students")
            ]:
                cur.execute(sql); stats[key] = cur.fetchone()['c']

            today = str(datetime.date.today())
            cur.execute("SELECT COUNT(DISTINCT student_id) as c FROM attendance WHERE DATE(marked_at)=%s", (today,))
            present = cur.fetchone()['c']
            stats['present']  = present
            stats['absent']   = max(0, stats['students'] - present)
            stats['present_percent'] = round((present/stats['students'])*100,1) if stats['students'] else 0

            cur.execute("""
                SELECT d.id, d.department_name, d.short_name,
                       COUNT(DISTINCT st.id) as total_students,
                       COUNT(DISTINCT t.id)  as total_teachers,
                       COUNT(DISTINCT a.student_id) as present
                FROM departments d
                LEFT JOIN students  st ON st.department_id=d.id
                LEFT JOIN teachers  t  ON t.department_id=d.id AND t.status='active'
                LEFT JOIN attendance a ON st.id=a.student_id AND DATE(a.marked_at)=%s
                GROUP BY d.id ORDER BY d.id
            """, (today,))
            rows = cur.fetchall()
            for r in rows: r['absent'] = max(0, r['total_students'] - r['present'])
            stats['dept_breakdown'] = rows
            return stats
        finally:
            cur.close(); conn.close()

    def get_hod_stats(self, dept_id):
        conn, cur = self._conn()
        try:
            stats = {}
            for sem in ['1st Year','2nd Year','3rd Year']:
                cur.execute("SELECT COUNT(*) as c FROM students WHERE department_id=%s AND class=%s", (dept_id,sem))
                stats[sem.replace(' ','_').lower()+'_students'] = cur.fetchone()['c']
            cur.execute("SELECT COUNT(*) as c FROM students WHERE department_id=%s", (dept_id,))
            stats['total_students'] = cur.fetchone()['c']
            cur.execute("SELECT COUNT(*) as c FROM teachers WHERE department_id=%s AND status='active'", (dept_id,))
            stats['teachers'] = cur.fetchone()['c']
            today = str(datetime.date.today())
            cur.execute("""
                SELECT COUNT(DISTINCT a.student_id) as c
                FROM students st LEFT JOIN attendance a ON st.id=a.student_id AND DATE(a.marked_at)=%s
                WHERE st.department_id=%s
            """, (today, dept_id))
            present = cur.fetchone()['c']
            stats['present']  = present
            stats['absent']   = max(0, stats['total_students'] - present)
            stats['present_percent'] = round((present/stats['total_students'])*100,1) if stats['total_students'] else 0
            return stats
        finally:
            cur.close(); conn.close()

    def get_teacher_stats(self, teacher_id):
        conn, cur = self._conn()
        try:
            stats = {}
            cur.execute("SELECT COUNT(*) as c FROM attendance_sessions WHERE teacher_id=%s", (teacher_id,))
            stats['sessions'] = cur.fetchone()['c']
            today = str(datetime.date.today())
            cur.execute("SELECT COUNT(*) as c FROM attendance_sessions WHERE teacher_id=%s AND DATE(start_time)=%s", (teacher_id,today))
            stats['today_sessions'] = cur.fetchone()['c']
            cur.execute("""
                SELECT ses.id, ses.date, c.class_name, c.division, s.subject_name,
                       COUNT(a.id) as attendance_count, ses.start_time
                FROM attendance_sessions ses
                LEFT JOIN classes c ON c.id=ses.class_id
                LEFT JOIN subjects s ON s.id=ses.subject_id
                LEFT JOIN attendance a ON a.session_id=ses.id
                WHERE ses.teacher_id=%s GROUP BY ses.id ORDER BY ses.start_time DESC LIMIT 10
            """, (teacher_id,))
            rows = cur.fetchall()
            stats['recent_sessions'] = [{k:(str(v) if hasattr(v,'isoformat') else v) for k,v in r.items()} for r in rows]
            return stats
        finally:
            cur.close(); conn.close()

    def get_student_stats(self, student_id):
        conn, cur = self._conn()
        try:
            cur.execute("SELECT * FROM students WHERE id=%s", (student_id,))
            student = cur.fetchone()
            if not student:
                return {'present':0,'total_sessions':0,'percentage':0,'recent':[],'by_subject':[],'absent':0}
            dept_id, cls = student.get('department_id'), student.get('class')

            cur.execute("""
                SELECT COUNT(*) as c FROM attendance_sessions ses
                LEFT JOIN classes c ON c.id=ses.class_id
                WHERE c.department_id=%s AND c.class_name=%s
            """, (dept_id, cls))
            total = cur.fetchone()['c']

            cur.execute("SELECT COUNT(*) as c FROM attendance WHERE student_id=%s", (student_id,))
            present = cur.fetchone()['c']

            cur.execute("""
                SELECT s.subject_name, COUNT(DISTINCT ses.id) as total,
                       COUNT(DISTINCT a.id) as present
                FROM subjects s
                LEFT JOIN attendance_sessions ses ON ses.subject_id=s.id
                LEFT JOIN classes c ON c.id=ses.class_id
                LEFT JOIN attendance a ON a.session_id=ses.id AND a.student_id=%s
                WHERE c.department_id=%s AND c.class_name=%s
                GROUP BY s.id, s.subject_name
            """, (student_id, dept_id, cls))
            subj_rows = cur.fetchall()
            for r in subj_rows: r['pct'] = round((r['present']/r['total'])*100,1) if r['total'] else 0

            cur.execute("""
                SELECT s.subject_name, DATE(a.marked_at) as date, TIME(a.marked_at) as time
                FROM attendance a
                LEFT JOIN attendance_sessions ses ON ses.id=a.session_id
                LEFT JOIN subjects s ON s.id=ses.subject_id
                WHERE a.student_id=%s ORDER BY a.marked_at DESC LIMIT 10
            """, (student_id,))
            rec_rows = cur.fetchall()

            # Day-wise attendance — last 30 days
            cur.execute("""
                SELECT DATE(a.marked_at) as att_date, COUNT(*) as sessions_present,
                       GROUP_CONCAT(DISTINCT s.subject_name ORDER BY s.subject_name SEPARATOR ', ') as subjects
                FROM attendance a
                LEFT JOIN attendance_sessions ses ON ses.id=a.session_id
                LEFT JOIN subjects s ON s.id=ses.subject_id
                WHERE a.student_id=%s AND a.marked_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
                GROUP BY DATE(a.marked_at) ORDER BY att_date DESC
            """, (student_id,))
            day_rows = cur.fetchall()

            return {
                'present': present, 'total_sessions': total,
                'absent':  max(0, total - present),
                'percentage': round((present/total)*100,1) if total else 0,
                'by_subject': subj_rows,
                'recent': [{k:(str(v) if hasattr(v,'isoformat') else v) for k,v in r.items()} for r in rec_rows],
                'by_day': [{k:(str(v) if hasattr(v,'isoformat') else v) for k,v in r.items()} for r in day_rows]
            }
        finally:
            cur.close(); conn.close()

    def get_dept_full_dashboard(self, dept_id):
        conn, cur = self._conn()
        try:
            data = {}
            cur.execute("SELECT * FROM departments WHERE id=%s", (dept_id,))
            data['dept'] = cur.fetchone()
            cur.execute("SELECT name,email,mobile FROM hods WHERE department_id=%s", (dept_id,))
            data['hod'] = cur.fetchone()
            for sem in ['1st Year','2nd Year','3rd Year']:
                cur.execute("SELECT COUNT(*) as c FROM students WHERE department_id=%s AND class=%s", (dept_id,sem))
                data[sem.replace(' ','_').lower()+'_count'] = cur.fetchone()['c']
            cur.execute("SELECT COUNT(*) as c FROM teachers WHERE department_id=%s AND status='active'", (dept_id,))
            data['teacher_count'] = cur.fetchone()['c']
            today = str(datetime.date.today())
            cur.execute("""
                SELECT COUNT(*) as total, COUNT(DISTINCT a.student_id) as present
                FROM students st
                LEFT JOIN attendance a ON st.id=a.student_id AND DATE(a.marked_at)=%s
                WHERE st.department_id=%s
            """, (today, dept_id))
            att = cur.fetchone()
            data.update({
                'present': att['present'], 'total_students': att['total'],
                'absent':  max(0, att['total']-att['present']),
                'percent': round((att['present']/att['total'])*100,1) if att['total'] else 0
            })
            cur.execute("""
                SELECT s.*,d.department_name FROM students s
                LEFT JOIN departments d ON d.id=s.department_id
                WHERE s.department_id=%s ORDER BY s.class,s.roll_no
            """, (dept_id,))
            rows = cur.fetchall()
            data['students'] = [{k:(str(v) if hasattr(v,'isoformat') else v) for k,v in r.items()} for r in rows]
            cur.execute("""
                SELECT t.*,d.department_name FROM teachers t
                LEFT JOIN departments d ON d.id=t.department_id
                WHERE t.department_id=%s ORDER BY t.name
            """, (dept_id,))
            rows2 = cur.fetchall()
            data['teachers'] = [{k:(str(v) if hasattr(v,'isoformat') else v) for k,v in r.items()} for r in rows2]
            return data
        finally:
            cur.close(); conn.close()
