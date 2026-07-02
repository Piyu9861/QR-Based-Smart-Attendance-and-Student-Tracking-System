from dbconfig import get_db_connection

class DepartmentModel:

    def _conn(self):
        c = get_db_connection()
        return c, c.cursor(dictionary=True)

    def get_all(self):
        conn, cur = self._conn()
        try:
            cur.execute("SELECT * FROM departments ORDER BY id")
            rows = cur.fetchall()
            return [{k:(str(v) if hasattr(v,'isoformat') else v) for k,v in r.items()} for r in rows]
        finally:
            cur.close(); conn.close()

    def get_by_id(self, id):
        conn, cur = self._conn()
        try:
            cur.execute("SELECT * FROM departments WHERE id=%s", (id,))
            return cur.fetchone()
        finally:
            cur.close(); conn.close()

    def insert(self, data):
        conn, cur = self._conn()
        try:
            cur.execute(
                "INSERT INTO departments (department_name, short_name) VALUES (%s,%s)",
                (data['department_name'], data.get('short_name',''))
            )
            conn.commit()
            return cur.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close(); conn.close()
