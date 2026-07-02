from dbconfig import get_db_connection

class ClassModel:

    def _conn(self):
        c = get_db_connection()
        return c, c.cursor(dictionary=True)

    def get_all(self):
        conn, cur = self._conn()
        try:
            cur.execute("""
                SELECT c.*, d.department_name, d.short_name,
                       CONCAT(c.class_name,' Div ',c.division) as display_name
                FROM classes c LEFT JOIN departments d ON d.id=c.department_id
                ORDER BY d.id,
                  FIELD(c.class_name,'1st Year','2nd Year','3rd Year'),
                  c.division
            """)
            return cur.fetchall()
        finally:
            cur.close(); conn.close()

    def get_by_dept(self, dept_id):
        conn, cur = self._conn()
        try:
            cur.execute("""
                SELECT c.*, d.department_name,
                       CONCAT(c.class_name,' Div ',c.division) as display_name
                FROM classes c
                LEFT JOIN departments d ON d.id=c.department_id
                WHERE c.department_id=%s
                ORDER BY FIELD(c.class_name,'1st Year','2nd Year','3rd Year'), c.division
            """, (dept_id,))
            return cur.fetchall()
        finally:
            cur.close(); conn.close()

    def get_by_class_dept(self, cls, dept_id):
        conn, cur = self._conn()
        try:
            cur.execute(
                "SELECT * FROM classes WHERE class_name=%s AND department_id=%s",
                (cls, dept_id)
            )
            return cur.fetchall()
        finally:
            cur.close(); conn.close()
