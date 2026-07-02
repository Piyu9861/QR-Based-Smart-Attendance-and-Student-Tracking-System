from dbconfig import get_db_connection

class HodModel:

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
            cur.execute("SELECT * FROM hods ORDER BY department_id")
            return self._rows(cur)   # was returning raw fetchall() — datetime crash fixed
        finally:
            cur.close(); conn.close()

    def get_all_with_dept(self):
        conn, cur = self._conn()
        try:
            cur.execute("""
                SELECT h.*, d.department_name, d.short_name
                FROM hods h LEFT JOIN departments d ON d.id=h.department_id
                ORDER BY d.id
            """)
            return self._rows(cur)   # datetime serialization fixed
        finally:
            cur.close(); conn.close()

    def get_by_id(self, id):
        conn, cur = self._conn()
        try:
            cur.execute("SELECT * FROM hods WHERE id=%s", (id,))
            r = cur.fetchone()
            return {k: (str(v) if hasattr(v, 'isoformat') else v) for k, v in r.items()} if r else None
        finally:
            cur.close(); conn.close()

    def get_by_dept_id(self, dept_id):
        conn, cur = self._conn()
        try:
            cur.execute("SELECT * FROM hods WHERE department_id=%s", (dept_id,))
            r = cur.fetchone()
            return {k: (str(v) if hasattr(v, 'isoformat') else v) for k, v in r.items()} if r else None
        finally:
            cur.close(); conn.close()

    # ── WRITE — always rollback on exception ──────────────────

    def insert(self, data):
        conn, cur = self._conn()
        try:
            cur.execute(
                "INSERT INTO hods (name,email,mobile,department_id,username,password) "
                "VALUES (%s,%s,%s,%s,%s,%s)",
                (data['name'], data.get('email',''), data.get('mobile',''),
                 data['department_id'], data['username'], data.get('password','hod123'))
            )
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
            cur.execute(
                "UPDATE hods SET name=%s,email=%s,mobile=%s,department_id=%s,username=%s "
                "WHERE id=%s",
                (data['name'], data.get('email',''), data.get('mobile',''),
                 data['department_id'], data['username'], id)
            )
            pwd = data.get('password','').strip()
            if pwd:
                cur.execute("UPDATE hods SET password=%s WHERE id=%s", (pwd, id))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close(); conn.close()

    def delete(self, id):
        conn, cur = self._conn()
        try:
            cur.execute("DELETE FROM hods WHERE id=%s", (id,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close(); conn.close()
