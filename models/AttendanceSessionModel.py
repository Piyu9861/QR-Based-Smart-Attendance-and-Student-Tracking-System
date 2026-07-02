from dbconfig import get_db_connection

class AttendanceSessionModel:

    def _conn(self):
        c = get_db_connection()
        return c, c.cursor(dictionary=True)

    def _rows(self, cur):
        rows = cur.fetchall()
        return [
            {k: (str(v) if hasattr(v, 'isoformat') else v) for k, v in r.items()}
            for r in rows
        ]

    # ── READ ──────────────────────────────────────────────────

    def get_all(self):
        conn, cur = self._conn()
        try:
            cur.execute("""
                SELECT ses.*, c.class_name, c.division, s.subject_name, t.name as teacher_name
                FROM attendance_sessions ses
                LEFT JOIN classes  c ON c.id=ses.class_id
                LEFT JOIN subjects s ON s.id=ses.subject_id
                LEFT JOIN teachers t ON t.id=ses.teacher_id
                ORDER BY ses.start_time DESC
            """)
            return self._rows(cur)
        finally:
            cur.close(); conn.close()

    def get_by_teacher(self, teacher_id):
        conn, cur = self._conn()
        try:
            cur.execute("""
                SELECT ses.*, c.class_name, c.division, s.subject_name
                FROM attendance_sessions ses
                LEFT JOIN classes  c ON c.id=ses.class_id
                LEFT JOIN subjects s ON s.id=ses.subject_id
                WHERE ses.teacher_id=%s ORDER BY ses.start_time DESC
            """, (teacher_id,))
            return self._rows(cur)
        finally:
            cur.close(); conn.close()

    def get_by_id(self, id):
        conn, cur = self._conn()
        try:
            cur.execute("SELECT * FROM attendance_sessions WHERE id=%s", (id,))
            r = cur.fetchone()
            cur.fetchall()  # consume any remaining results
            return {k: (str(v) if hasattr(v, 'isoformat') else v) for k, v in r.items()} if r else None
        finally:
            cur.close(); conn.close()

    def get_by_token(self, token):
        conn, cur = self._conn()
        try:
            cur.execute("SELECT * FROM attendance_sessions WHERE qr_token=%s", (token,))
            r = cur.fetchone()
            cur.fetchall()  # consume any remaining results
            return {k: (str(v) if hasattr(v, 'isoformat') else v) for k, v in r.items()} if r else None
        finally:
            cur.close(); conn.close()

    # ── WRITE ─────────────────────────────────────────────────

    def insert(self, data):
        conn, cur = self._conn()
        try:
            cur.execute("""
                INSERT INTO attendance_sessions
                (class_id,subject_id,teacher_id,date,start_time,end_time,
                 qr_token,status,qr_image)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (data['class_id'], data['subject_id'], data['teacher_id'],
                  data['date'], data['start_time'], data['end_time'],
                  data['qr_token'], data['status'], data['qr_image']))
            conn.commit()
            return cur.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close(); conn.close()
