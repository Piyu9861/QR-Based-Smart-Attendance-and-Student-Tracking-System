from dbconfig import get_db_connection

class SubjectModel:

    def _conn(self):
        c = get_db_connection()
        return c, c.cursor(dictionary=True)

    def get_all(self):
        conn, cur = self._conn()
        try:
            cur.execute("SELECT * FROM subjects ORDER BY department_id, semester, subject_name")
            rows = cur.fetchall()
            return [{k:(str(v) if hasattr(v,'isoformat') else v) for k,v in r.items()} for r in rows]
        finally:
            cur.close(); conn.close()

    def get_by_dept(self, dept_id):
        conn, cur = self._conn()
        try:
            cur.execute("SELECT * FROM subjects WHERE department_id=%s ORDER BY semester, subject_name", (dept_id,))
            rows = cur.fetchall()
            return [{k:(str(v) if hasattr(v,'isoformat') else v) for k,v in r.items()} for r in rows]
        finally:
            cur.close(); conn.close()

    def get_by_id(self, id):
        conn, cur = self._conn()
        try:
            cur.execute("SELECT * FROM subjects WHERE id=%s", (id,))
            return cur.fetchone()
        finally:
            cur.close(); conn.close()

    def insert(self, data):
        conn, cur = self._conn()
        try:
            cur.execute(
                "INSERT INTO subjects (subject_name,subject_code,department_id,semester,class) VALUES (%s,%s,%s,%s,%s)",
                (data['subject_name'], data.get('subject_code',''),
                 data['department_id'], data.get('semester',''), data.get('class',''))
            )
            conn.commit()
            return cur.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close(); conn.close()

    def delete(self, id):
        conn, cur = self._conn()
        try:
            cur.execute("DELETE FROM subjects WHERE id=%s", (id,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close(); conn.close()
