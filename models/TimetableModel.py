from dbconfig import get_db_connection

class TimetableModel:

    def _conn(self):
        c = get_db_connection()
        return c, c.cursor(dictionary=True)

    def get_all(self):
        conn, cur = self._conn()
        try:
            cur.execute("""
                SELECT tt.*, c.class_name, c.division, d.department_name,
                       s.subject_name, t.name as teacher_name
                FROM timetable tt
                LEFT JOIN classes c ON c.id=tt.class_id
                LEFT JOIN departments d ON d.id=c.department_id
                LEFT JOIN subjects s ON s.id=tt.subject_id
                LEFT JOIN teachers t ON t.id=tt.teacher_id
                ORDER BY d.id, c.class_name, tt.day
            """)
            rows = cur.fetchall()
            return [{k:(str(v) if hasattr(v,'isoformat') else v) for k,v in r.items()} for r in rows]
        finally:
            cur.close(); conn.close()

    def get_by_class_dept(self, cls, dept_id):
        conn, cur = self._conn()
        try:
            cur.execute("""
                SELECT tt.*, c.class_name, c.division, s.subject_name, t.name as teacher_name
                FROM timetable tt
                LEFT JOIN classes c ON c.id=tt.class_id
                LEFT JOIN subjects s ON s.id=tt.subject_id
                LEFT JOIN teachers t ON t.id=tt.teacher_id
                WHERE c.department_id=%s AND c.class_name=%s
                ORDER BY FIELD(tt.day,'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), tt.time_slot
            """, (dept_id, cls))
            rows = cur.fetchall()
            return [{k:(str(v) if hasattr(v,'isoformat') else v) for k,v in r.items()} for r in rows]
        finally:
            cur.close(); conn.close()

    def insert(self, data):
        conn, cur = self._conn()
        try:
            cur.execute(
                "INSERT INTO timetable (class_id,subject_id,teacher_id,day,time_slot,room_no) VALUES (%s,%s,%s,%s,%s,%s)",
                (data['class_id'], data['subject_id'], data['teacher_id'],
                 data['day'], data['time_slot'], data.get('room_no',''))
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
            cur.execute("DELETE FROM timetable WHERE id=%s", (id,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close(); conn.close()
