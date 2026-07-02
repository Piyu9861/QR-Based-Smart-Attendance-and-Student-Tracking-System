from dbconfig import get_db_connection

class TeacherModel:

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
                SELECT t.*, d.department_name, d.short_name
                FROM teachers t LEFT JOIN departments d ON d.id=t.department_id
                ORDER BY d.id, t.name
            """)
            return self._rows(cur)
        finally:
            cur.close(); conn.close()

    def get_all_with_dept(self):
        return self.get_all()

    def get_by_id(self, id):
        conn, cur = self._conn()
        try:
            cur.execute("""
                SELECT t.*, d.department_name FROM teachers t
                LEFT JOIN departments d ON d.id=t.department_id WHERE t.id=%s
            """, (id,))
            r = cur.fetchone()
            return {k: (str(v) if hasattr(v, 'isoformat') else v) for k, v in r.items()} if r else None
        finally:
            cur.close(); conn.close()

    def get_by_dept(self, dept_id):
        conn, cur = self._conn()
        try:
            cur.execute("""
                SELECT t.*, d.department_name FROM teachers t
                LEFT JOIN departments d ON d.id=t.department_id
                WHERE t.department_id=%s AND t.status='active' ORDER BY t.name
            """, (dept_id,))
            return self._rows(cur)
        finally:
            cur.close(); conn.close()

    # ── WRITE — always rollback on exception ──────────────────

    def insert(self, data):
        conn, cur = self._conn()
        try:
            cur.execute("""
                INSERT INTO teachers
                (name,email,mobile,department_id,designation,joining_date,
                 status,is_class_teacher,subjects,username,password,whatsapp)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                data.get('name'), data.get('email'), data.get('mobile'),
                data.get('department_id'), data.get('designation','Lecturer'),
                data.get('joining_date') or None,
                data.get('status','active'), data.get('is_class_teacher','no'),
                data.get('subjects',''), data.get('username',''),
                data.get('password','teacher123'), data.get('mobile','')
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
                UPDATE teachers SET
                name=%s,email=%s,mobile=%s,department_id=%s,designation=%s,
                joining_date=%s,status=%s,is_class_teacher=%s,subjects=%s,
                username=%s,whatsapp=%s
                WHERE id=%s
            """, (
                data.get('name'), data.get('email'), data.get('mobile'),
                data.get('department_id'), data.get('designation','Lecturer'),
                data.get('joining_date') or None,
                data.get('status','active'), data.get('is_class_teacher','no'),
                data.get('subjects',''), data.get('username',''),
                data.get('mobile',''), id
            ))
            pwd = data.get('password','').strip()
            if pwd:
                cur.execute("UPDATE teachers SET password=%s WHERE id=%s", (pwd, id))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close(); conn.close()

    def delete(self, id):
        """
        Delete teacher safely:
          1. Nullify teacher_id in attendance_sessions (keep session records)
          2. Delete the teacher
        """
        conn, cur = self._conn()
        try:
            cur.execute(
                "UPDATE attendance_sessions SET teacher_id=NULL WHERE teacher_id=%s", (id,)
            )
            cur.execute("DELETE FROM teachers WHERE id=%s", (id,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close(); conn.close()
