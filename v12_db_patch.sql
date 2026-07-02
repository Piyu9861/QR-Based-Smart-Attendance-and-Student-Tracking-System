-- ============================================================
-- v12 DATABASE PATCH — Run this on existing databases
-- Fixes crash on update/delete by adding proper FK + ON DELETE
-- K.P. Patil Institute QR Attendance System
-- ============================================================

USE `qr_attendance_db`;

-- ── Step 1: Drop old FK if exists ────────────────────────────
SET FOREIGN_KEY_CHECKS = 0;

-- ── Step 2: Fix attendance table — add ON DELETE CASCADE ─────
-- If attendance record's session or student is deleted, auto-remove attendance row
ALTER TABLE `attendance`
  DROP FOREIGN KEY IF EXISTS `att_fk_session`,
  DROP FOREIGN KEY IF EXISTS `att_fk_student`;

ALTER TABLE `attendance`
  ADD CONSTRAINT `att_fk_session`
    FOREIGN KEY (`session_id`)
    REFERENCES `attendance_sessions`(`id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `att_fk_student`
    FOREIGN KEY (`student_id`)
    REFERENCES `students`(`id`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- ── Step 3: Fix sms_log — add ON DELETE SET NULL ──────────────
ALTER TABLE `sms_log`
  DROP FOREIGN KEY IF EXISTS `sms_fk_student`;

ALTER TABLE `sms_log`
  ADD CONSTRAINT `sms_fk_student`
    FOREIGN KEY (`student_id`)
    REFERENCES `students`(`id`)
    ON DELETE SET NULL ON UPDATE CASCADE;

-- ── Step 4: Fix attendance_sessions — ON DELETE SET NULL ──────
ALTER TABLE `attendance_sessions`
  DROP FOREIGN KEY IF EXISTS `sess_fk_teacher`,
  DROP FOREIGN KEY IF EXISTS `sess_fk_class`,
  DROP FOREIGN KEY IF EXISTS `sess_fk_subject`;

ALTER TABLE `attendance_sessions`
  ADD CONSTRAINT `sess_fk_teacher`
    FOREIGN KEY (`teacher_id`)
    REFERENCES `teachers`(`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `sess_fk_class`
    FOREIGN KEY (`class_id`)
    REFERENCES `classes`(`id`)
    ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `sess_fk_subject`
    FOREIGN KEY (`subject_id`)
    REFERENCES `subjects`(`id`)
    ON DELETE SET NULL ON UPDATE CASCADE;

-- ── Step 5: Fix students FK ───────────────────────────────────
ALTER TABLE `students`
  DROP FOREIGN KEY IF EXISTS `stud_fk_dept`;

ALTER TABLE `students`
  ADD CONSTRAINT `stud_fk_dept`
    FOREIGN KEY (`department_id`)
    REFERENCES `departments`(`id`)
    ON DELETE SET NULL ON UPDATE CASCADE;

-- ── Step 6: Fix hods FK ───────────────────────────────────────
ALTER TABLE `hods`
  DROP FOREIGN KEY IF EXISTS `hod_fk_dept`;

ALTER TABLE `hods`
  ADD CONSTRAINT `hod_fk_dept`
    FOREIGN KEY (`department_id`)
    REFERENCES `departments`(`id`)
    ON DELETE SET NULL ON UPDATE CASCADE;

-- ── Step 7: Add performance indexes ──────────────────────────
ALTER TABLE `attendance`
  DROP INDEX IF EXISTS `idx_att_student`,
  DROP INDEX IF EXISTS `idx_att_session_date`;

ALTER TABLE `attendance`
  ADD INDEX `idx_att_student`      (`student_id`),
  ADD INDEX `idx_att_session_date` (`session_id`, `marked_at`);

ALTER TABLE `attendance_sessions`
  DROP INDEX IF EXISTS `idx_sess_teacher`;

ALTER TABLE `attendance_sessions`
  ADD INDEX `idx_sess_teacher` (`teacher_id`);

ALTER TABLE `students`
  DROP INDEX IF EXISTS `idx_stud_dept_class`;

ALTER TABLE `students`
  ADD INDEX `idx_stud_dept_class` (`department_id`, `class`);

-- ── Re-enable FK checks ───────────────────────────────────────
SET FOREIGN_KEY_CHECKS = 1;

SELECT 'v12 patch applied successfully — FK constraints and indexes are now correct.' AS status;

-- ── v11 patch: Update D.T. Suryawanshi as Class Teacher ──────
UPDATE teachers
SET designation = 'Class Teacher', is_class_teacher = 'yes'
WHERE email = 'digusuryawanshi@gmail.com';

COMMIT;
