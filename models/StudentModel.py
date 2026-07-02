from dbconfig import get_db_connection

class StudentModel:

    def _conn(self):
        c = get_db_connection()
        return c, c.cursor(dictionary=True)

    def _rows(self, cur):
        rows = cur.fetchall()
        return [
            {k: (str(v) if hasattr(v, 'isoformat') else v) for k, v in r.items()}
            for r in rows
        ]

    def _null(self, v):
        if v is None or str(v).strip() == '':
            return None
        try:
            return float(v)
        except (ValueError, TypeError):
            return None

    # ── READ ──────────────────────────────────────────────────

    def get_all(self):
        conn, cur = self._conn()
        try:
            cur.execute("""
                SELECT s.*, d.department_name, d.short_name
                FROM students s LEFT JOIN departments d ON d.id=s.department_id
                ORDER BY d.id, s.class, s.roll_no
            """)
            return self._rows(cur)
        finally:
            cur.close(); conn.close()

    def get_all_with_dept(self):
        return self.get_all()

    def get_by_id(self, id):
        conn, cur = self._conn()
        try:
            cur.execute("SELECT * FROM students WHERE id=%s", (id,))
            r = cur.fetchone()
            return {k: (str(v) if hasattr(v, 'isoformat') else v) for k, v in r.items()} if r else None
        finally:
            cur.close(); conn.close()

    def get_by_dept(self, dept_id):
        conn, cur = self._conn()
        try:
            cur.execute("""
                SELECT s.*, d.department_name FROM students s
                LEFT JOIN departments d ON d.id=s.department_id
                WHERE s.department_id=%s ORDER BY s.class, s.roll_no
            """, (dept_id,))
            return self._rows(cur)
        finally:
            cur.close(); conn.close()

    def get_by_class_dept(self, cls, dept_id):
        conn, cur = self._conn()
        try:
            cur.execute("""
                SELECT s.*, d.department_name FROM students s
                LEFT JOIN departments d ON d.id=s.department_id
                WHERE s.class=%s AND s.department_id=%s ORDER BY s.roll_no
            """, (cls, dept_id))
            return self._rows(cur)
        finally:
            cur.close(); conn.close()

    # ── WRITE — always rollback on exception ──────────────────

    def insert(self, data):
        conn, cur = self._conn()
        try:
            cur.execute("""
                INSERT INTO students
                (roll_no,enrollment_no,name,email,class,department_id,gender,
                 category,seat_type,mobile,parent_mobile,parent_whatsapp,
                 address,blood_group,password,
                 mark_10th,mark_sem1,mark_sem2,mark_sem3,mark_sem4,mark_sem5,mark_sem6)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                data.get('roll_no'), data.get('enrollment_no'), data.get('name'),
                data.get('email',''), data.get('class'), data.get('department_id'),
                data.get('gender'), data.get('category'), data.get('seat_type'),
                data.get('mobile'), data.get('parent_mobile',''),
                data.get('parent_mobile',''),
                data.get('address',''), data.get('blood_group',''),
                data.get('password','Stud123'),
                self._null(data.get('mark_10th')), self._null(data.get('mark_sem1')),
                self._null(data.get('mark_sem2')), self._null(data.get('mark_sem3')),
                self._null(data.get('mark_sem4')), self._null(data.get('mark_sem5')),
                self._null(data.get('mark_sem6')),
            ))
            conn.commit()
            return cur.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close(); conn.close()

    def update(self, id, data):
        conn, cur = self._conn()
        try:
            cur.execute("""
                UPDATE students SET
                roll_no=%s,enrollment_no=%s,name=%s,email=%s,class=%s,
                department_id=%s,gender=%s,category=%s,seat_type=%s,
                mobile=%s,parent_mobile=%s,parent_whatsapp=%s,
                address=%s,blood_group=%s,
                mark_10th=%s,mark_sem1=%s,mark_sem2=%s,mark_sem3=%s,
                mark_sem4=%s,mark_sem5=%s,mark_sem6=%s
                WHERE id=%s
            """, (
                data.get('roll_no'), data.get('enrollment_no'), data.get('name'),
                data.get('email',''), data.get('class'), data.get('department_id'),
                data.get('gender'), data.get('category'), data.get('seat_type'),
                data.get('mobile'), data.get('parent_mobile',''),
                data.get('parent_mobile',''),
                data.get('address',''), data.get('blood_group',''),
                self._null(data.get('mark_10th')), self._null(data.get('mark_sem1')),
                self._null(data.get('mark_sem2')), self._null(data.get('mark_sem3')),
                self._null(data.get('mark_sem4')), self._null(data.get('mark_sem5')),
                self._null(data.get('mark_sem6')), id,
            ))
            pwd = data.get('password','').strip()
            if pwd:
                cur.execute("UPDATE students SET password=%s WHERE id=%s", (pwd, id))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close(); conn.close()

    def delete(self, id):
        """
        Delete in safe order:
          1. sms_log  (references student_id)
          2. attendance (references student_id)
          3. students (main record)
        All inside one transaction — rollback if anything fails.
        """
        conn, cur = self._conn()
        try:
            cur.execute("DELETE FROM sms_log   WHERE student_id=%s", (id,))
            cur.execute("DELETE FROM attendance WHERE student_id=%s", (id,))
            cur.execute("DELETE FROM students   WHERE id=%s",         (id,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close(); conn.close()
