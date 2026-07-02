from dbconfig import get_db_connection
import datetime

class AcademicCalendarModel:

    def _conn(self):
        c = get_db_connection()
        return c, c.cursor(dictionary=True)

    def _rows(self, cur):
        rows = cur.fetchall()
        return [{k:(str(v) if hasattr(v,'isoformat') else v) for k,v in r.items()} for r in rows]

    def get_all(self):
        conn, cur = self._conn()
        try:
            cur.execute("SELECT * FROM academic_calendar ORDER BY date")
            return self._rows(cur)
        finally:
            cur.close(); conn.close()

    def get_by_dept(self, dept_id):
        conn, cur = self._conn()
        try:
            cur.execute(
                "SELECT * FROM academic_calendar WHERE department_id IS NULL OR department_id=%s ORDER BY date",
                (dept_id,)
            )
            return self._rows(cur)
        finally:
            cur.close(); conn.close()

    def insert(self, data):
        conn, cur = self._conn()
        try:
            cur.execute(
                "INSERT INTO academic_calendar (title,date,type,description,department_id) VALUES (%s,%s,%s,%s,%s)",
                (data['title'], data['date'], data['type'],
                 data.get('description',''), data.get('department_id') or None)
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
            cur.execute("DELETE FROM academic_calendar WHERE id=%s", (id,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close(); conn.close()
