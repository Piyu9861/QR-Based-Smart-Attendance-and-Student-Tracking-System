from dbconfig import get_db_connection

class AuthModel:

    def check_login(self, role, username, password):
        """
        Returns user dict on success, None on failure.
        Creates a fresh DB connection per call.
        """
        tables = {
            'principal': 'principal',
            'hod':       'hods',
            'teacher':   'teachers',
            'student':   'students'
        }
        table = tables.get(role)
        if not table:
            return None

        conn   = None
        cursor = None
        try:
            conn   = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            username = str(username).strip()
            password = str(password).strip()

            if role == 'teacher':
                # Login: email address OR teacher username (TCH001 etc.)
                cursor.execute(
                    "SELECT * FROM teachers "
                    "WHERE (email=%s OR username=%s) AND password=%s AND status='active'",
                    (username, username, password)
                )
            elif role == 'student':
                # Login: mobile number OR enrollment number
                cursor.execute(
                    "SELECT * FROM students "
                    "WHERE (mobile=%s OR enrollment_no=%s) AND password=%s",
                    (username, username, password)
                )
            elif role == 'hod':
                # Login: username field in hods table
                cursor.execute(
                    "SELECT * FROM hods WHERE username=%s AND password=%s",
                    (username, password)
                )
            elif role == 'principal':
                # Login: username field in principal table
                cursor.execute(
                    "SELECT * FROM principal WHERE username=%s AND password=%s",
                    (username, password)
                )
            else:
                return None

            row = cursor.fetchone()
            return row   # None if no match

        except Exception as e:
            print(f"[AuthModel] login error for role={role}: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conn:   conn.close()
