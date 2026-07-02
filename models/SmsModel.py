from dbconfig import get_db_connection
import datetime

class SmsModel:

    def _conn(self):
        c = get_db_connection()
        return c, c.cursor(dictionary=True)

    def send_attendance_sms(self, student, subject_name, marked_at):
        parent = student.get('parent_mobile') or student.get('parent_whatsapp','')
        if not parent: return False
        msg = (
            f"[KP Patil Institute]\n"
            f"Dear Parent, your ward *{student.get('name','')}* "
            f"(Roll:{student.get('roll_no','')}) attended *{subject_name}* on "
            f"{marked_at.strftime('%d-%b-%Y at %I:%M %p')}. -Principal Mr. S.P. More"
        )
        self._log(student['id'], parent, msg, 'attendance', 'whatsapp')
        self._whatsapp(parent, msg)
        return True

    def send_absent_alert(self, student, subject_name, date_str):
        parent = student.get('parent_mobile') or student.get('parent_whatsapp','')
        if not parent: return False
        msg = (
            f"[KP Patil Institute]\n"
            f"Dear Parent, *{student.get('name','')}* (Roll:{student.get('roll_no','')}) "
            f"was *ABSENT* for *{subject_name}* on {date_str}. "
            f"Min attendance required: 75%. -Principal Mr. S.P. More"
        )
        self._log(student['id'], parent, msg, 'absent_alert', 'whatsapp')
        self._whatsapp(parent, msg)
        return True

    def _log(self, student_id, mobile, message, sms_type, channel='sms'):
        conn, cur = self._conn()
        try:
            cur.execute(
                "INSERT INTO sms_log (student_id,parent_mobile,message,sent_at,status,type,channel) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (student_id, mobile, message, datetime.datetime.now(), 'sent', sms_type, channel)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"SMS log error: {e}")
        finally:
            cur.close(); conn.close()

    def _whatsapp(self, mobile, message):
        """
        DEMO: prints to console.
        For real WhatsApp (UltraMsg - easiest for India):
            import requests
            requests.post("https://api.ultramsg.com/YOUR_INSTANCE/messages/chat",
                data={"token":"YOUR_TOKEN","to":f"+91{mobile}","body":message})

        For Fast2SMS (real SMS):
            import requests
            requests.post("https://www.fast2sms.com/dev/bulkV2",
                headers={"authorization":"YOUR_API_KEY"},
                data={"route":"q","message":message[:160],"numbers":mobile})
        """
        print(f"\n📱 [WhatsApp → +91{mobile}]\n{message}\n{'─'*50}")

    def get_recent_logs(self, limit=100):
        conn, cur = self._conn()
        try:
            cur.execute("""
                SELECT sl.*, st.name as student_name, st.roll_no
                FROM sms_log sl LEFT JOIN students st ON st.id=sl.student_id
                ORDER BY sl.sent_at DESC LIMIT %s
            """, (limit,))
            rows = cur.fetchall()
            return [{k:(str(v) if hasattr(v,'isoformat') else v) for k,v in r.items()} for r in rows]
        finally:
            cur.close(); conn.close()
