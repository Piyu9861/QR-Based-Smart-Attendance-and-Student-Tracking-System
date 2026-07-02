from dbconfig import get_db_connection

class AttendanceModel:

    def _conn(self):
        c = get_db_connection()
        return c, c.cursor(dictionary=True)

    def _rows(self, cur):
        rows = cur.fetchall()
        return [
            {k: (str(v) if hasattr(v, 'isoformat') else v) for k, v in r.items()}
            for r in rows
        ]

    # ── WRITE ─────────────────────────────────────────────────

    def mark_attendance(self, data):
        conn, cur = self._conn()
        try:
            cur.execute(
                "INSERT INTO attendance "
                "(session_id,student_id,marked_at,latitude,longitude,location_verified) "
                "VALUES (%s,%s,%s,%s,%s,%s)",
                (data['session_id'], data['student_id'], data['marked_at'],
                 data.get('latitude',''), data.get('longitude',''),
                 data.get('location_verified', 0))
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close(); conn.close()

    # ── READ ──────────────────────────────────────────────────

    def already_marked(self, session_id, student_id):
        conn, cur = self._conn()
        try:
            cur.execute(
                "SELECT * FROM attendance WHERE session_id=%s AND student_id=%s",
                (session_id, student_id)
            )
            r = cur.fetchone()
            cur.fetchall()  # consume remaining results to avoid sync errors
            return r
        finally:
            cur.close(); conn.close()

    def get_session_attendance(self, session_id):
        conn, cur = self._conn()
        try:
            cur.execute("""
                SELECT st.id, st.name, st.roll_no, st.mobile, a.marked_at,
                       a.location_verified,
                       CASE WHEN a.id IS NOT NULL THEN 1 ELSE 0 END AS is_present
                FROM students st
                LEFT JOIN attendance a
                  ON st.id=a.student_id AND a.session_id=%s
                ORDER BY st.roll_no
            """, (session_id,))
            return self._rows(cur)
        finally:
            cur.close(); conn.close()

    def get_student_attendance(self, student_id):
        conn, cur = self._conn()
        try:
            cur.execute("""
                SELECT a.*, s.subject_name, ses.date,
                       COALESCE(DATE(a.marked_at),'') as att_date
                FROM attendance a
                LEFT JOIN attendance_sessions ses ON ses.id=a.session_id
                LEFT JOIN subjects s ON s.id=ses.subject_id
                WHERE a.student_id=%s ORDER BY ses.date DESC
            """, (student_id,))
            return self._rows(cur)
        finally:
            cur.close(); conn.close()

    def get_filtered_report(self, date, dept_id='', teacher_id='', subject_id='', class_name=''):
        conn, cur = self._conn()
        try:
            where  = ["DATE(a.marked_at)=%s"]
            params = [date]
            if dept_id:    where.append("st.department_id=%s"); params.append(dept_id)
            if teacher_id: where.append("ses.teacher_id=%s");  params.append(teacher_id)
            if subject_id: where.append("ses.subject_id=%s");  params.append(subject_id)
            if class_name: where.append("st.class=%s");        params.append(class_name)
            cur.execute(f"""
                SELECT a.id, st.name as student_name, st.roll_no,
                       st.class as student_class, st.mobile,
                       d.department_name, sub.subject_name,
                       t.name as teacher_name, a.marked_at, a.status, a.location_verified
                FROM attendance a
                LEFT JOIN students st           ON st.id=a.student_id
                LEFT JOIN departments d         ON d.id=st.department_id
                LEFT JOIN attendance_sessions ses ON ses.id=a.session_id
                LEFT JOIN subjects sub          ON sub.id=ses.subject_id
                LEFT JOIN teachers t            ON t.id=ses.teacher_id
                WHERE {' AND '.join(where)}
                ORDER BY a.marked_at DESC
            """, params)
            return self._rows(cur)
        finally:
            cur.close(); conn.close()

    def get_teacher_filtered(self, teacher_id, date, class_name='', subject_id=''):
        conn, cur = self._conn()
        try:
            where  = ["ses.teacher_id=%s", "DATE(a.marked_at)=%s"]
            params = [teacher_id, date]
            if class_name: where.append("st.class=%s");       params.append(class_name)
            if subject_id: where.append("ses.subject_id=%s"); params.append(subject_id)
            cur.execute(f"""
                SELECT a.id, st.name as student_name, st.roll_no,
                       st.class as student_class,
                       sub.subject_name, a.marked_at, a.status, a.location_verified
                FROM attendance a
                LEFT JOIN students st             ON st.id=a.student_id
                LEFT JOIN attendance_sessions ses ON ses.id=a.session_id
                LEFT JOIN subjects sub            ON sub.id=ses.subject_id
                WHERE {' AND '.join(where)}
                ORDER BY a.marked_at DESC
            """, params)
            return self._rows(cur)
        finally:
            cur.close(); conn.close()

    def get_all_for_export(self, date='', dept_id='', class_name=''):
        conn, cur = self._conn()
        try:
            where  = ["1=1"]
            params = []
            if date:       where.append("DATE(a.marked_at)=%s"); params.append(date)
            if dept_id:    where.append("st.department_id=%s");  params.append(dept_id)
            if class_name: where.append("st.class=%s");          params.append(class_name)
            cur.execute(f"""
                SELECT st.roll_no, st.name as student_name, st.class as student_class,
                       d.department_name, sub.subject_name, t.name as teacher_name,
                       DATE(a.marked_at) as date, TIME(a.marked_at) as time,
                       a.status, a.location_verified
                FROM attendance a
                LEFT JOIN students st             ON st.id=a.student_id
                LEFT JOIN departments d           ON d.id=st.department_id
                LEFT JOIN attendance_sessions ses ON ses.id=a.session_id
                LEFT JOIN subjects sub            ON sub.id=ses.subject_id
                LEFT JOIN teachers t              ON t.id=ses.teacher_id
                WHERE {' AND '.join(where)}
                ORDER BY d.id, st.class, st.roll_no, a.marked_at
            """, params)
            return self._rows(cur)
        finally:
            cur.close(); conn.close()
