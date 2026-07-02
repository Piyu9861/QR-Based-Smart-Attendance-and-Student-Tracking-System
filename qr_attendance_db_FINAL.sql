-- ============================================================
-- K.P. Patil Institute of Technology (Polytechnic), Mudal
-- Smart QR Attendance DB — FINAL v3
-- Principal: Mr. S.P. More | Real Staff from Website
-- ============================================================
SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone="+00:00";
SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS `qr_attendance_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `qr_attendance_db`;

DROP TABLE IF EXISTS `departments`;
CREATE TABLE `departments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `department_name` varchar(100) NOT NULL,
  `short_name` varchar(20) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `departments` VALUES
(1,'Artificial Intelligence & Machine Learning','AIML','2026-01-01 00:00:00'),
(2,'Computer Engineering','COMP','2026-01-01 00:00:00'),
(3,'Civil Engineering','CIVIL','2026-01-01 00:00:00'),
(4,'Mechanical Engineering','MECH','2026-01-01 00:00:00'),
(5,'Electrical Engineering','ELEC','2026-01-01 00:00:00');

-- Principal: S.P. More (from website)
DROP TABLE IF EXISTS `principal`;
CREATE TABLE `principal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `department_id` int(11) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `principal` VALUES
(1,'Mr. S.P. More','spmore@kppatil.edu','9421042674',1,'spmore','spmore123','2026-01-01 00:00:00');

-- HODs from website
DROP TABLE IF EXISTS `hods`;
CREATE TABLE `hods` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `department_id` int(11) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `hods` VALUES
(1,'Mr. Patil Avadhut P.','avadhut404@gmail.com','9405161392',1,'avadhut_aiml','avadhut123','2026-01-01 00:00:00'),
(2,'HOD Computer Engg','hod_comp@kppatil.edu','9876543212',2,'hod_comp','hodcomp123','2026-01-01 00:00:00'),
(3,'HOD Civil Engg','hod_civil@kppatil.edu','9876543213',3,'hod_civil','hodcivil123','2026-01-01 00:00:00'),
(4,'HOD Mechanical Engg','hod_mech@kppatil.edu','9876543214',4,'hod_mech','hodmech123','2026-01-01 00:00:00'),
(5,'HOD Electrical Engg','hod_elec@kppatil.edu','9876543215',5,'hod_elec','hodelec123','2026-01-01 00:00:00');

-- Teachers — real from website (AIML dept)
DROP TABLE IF EXISTS `teachers`;
CREATE TABLE `teachers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `department_id` int(11) DEFAULT NULL,
  `designation` varchar(100) DEFAULT NULL,
  `joining_date` date DEFAULT NULL,
  `status` enum('active','inactive') DEFAULT 'active',
  `is_class_teacher` varchar(5) DEFAULT 'no',
  `subjects` text DEFAULT '',
  `username` varchar(50) DEFAULT '',
  `password` varchar(100) DEFAULT 'teacher123',
  `whatsapp` varchar(15) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  CONSTRAINT `teachers_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `teachers` VALUES
-- AIML Teachers (from website)
(1,'Mr. D.T. Suryawanshi','digusuryawanshi@gmail.com','9503096463',1,'Class Teacher','2021-06-01','active','yes','Advanced Algorithm in AI & ML,Network Management','TCH001','teacher123','9503096463',NOW(),NOW()),
(2,'Miss. P.M. Kumbhar','poojakumbhar912@gmail.com','9096203504',1,'Lecturer','2022-07-01','active','no','Mobile Application Development,Mathematics','TCH002','teacher123','9096203504',NOW(),NOW()),
(3,'Mr. D.R. Bhat','digvijaybhat2301@gmail.com','8007809343',1,'Lecturer','2021-08-01','active','no','Java Programming,Data Communication','TCH003','teacher123','8007809343',NOW(),NOW()),
(4,'Miss. S.S. Patil','psupriyav37@gmail.com','9075728773',1,'Lecturer','2023-06-01','active','no','Principles of Image Processing,Network Management','TCH004','teacher123','9075728773',NOW(),NOW()),
(5,'Mr. K.A. Maskar','maskarkirtiraj@gmail.com','7588490498',1,'Lecturer','2022-09-01','active','no','Big Data Analytics,UI/UX Design','TCH005','teacher123','7588490498',NOW(),NOW()),
(6,'Mr. A.B. Huddar','akshayhuddar108@gmail.com','7387576108',1,'Lecturer','2023-01-01','active','no','Management,Advanced Algorithm','TCH006','teacher123','7387576108',NOW(),NOW()),
(7,'Mr. A.P. Patil','appatil@kppatil.edu','9405161392',1,'Assistant Professor','2018-06-01','active','no','Capstone Project,Management','TCH007','teacher123','9405161392',NOW(),NOW()),
(8,'Mr. R.D. Patil','rdpatil@kppatil.edu','9876543108',1,'Lecturer','2020-06-01','active','no','Mathematics for ML','TCH008','teacher123','9876543108',NOW(),NOW()),
-- Other dept teachers
(9,'Teacher COMP 1','teacher_comp1@kppatil.edu','8765432109',2,'Lecturer','2019-06-01','active','yes','Operating Systems,DBMS','TCH009','teacher123','8765432109',NOW(),NOW()),
(10,'Teacher CIVIL 1','teacher_civil1@kppatil.edu','8765432110',3,'Lecturer','2018-06-01','active','yes','Steel Structures,Concrete','TCH010','teacher123','8765432110',NOW(),NOW()),
(11,'Teacher MECH 1','teacher_mech1@kppatil.edu','8765432111',4,'Lecturer','2017-06-01','active','yes','Thermodynamics,Fluid Mechanics','TCH011','teacher123','8765432111',NOW(),NOW()),
(12,'Teacher ELEC 1','teacher_elec1@kppatil.edu','8765432112',5,'Lecturer','2019-06-01','active','yes','Power Systems,Control Systems','TCH012','teacher123','8765432112',NOW(),NOW());

-- Classes — WITHOUT division suffix (just Div A, B, C as separate rows)
DROP TABLE IF EXISTS `classes`;
CREATE TABLE `classes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class_name` varchar(10) DEFAULT NULL,
  `division` varchar(10) DEFAULT NULL,
  `department_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `classes` VALUES
-- AIML: 3 divs per year
(1,'1st Year','A',1),(2,'1st Year','B',1),(3,'1st Year','C',1),
(4,'2nd Year','A',1),(5,'2nd Year','B',1),(6,'2nd Year','C',1),
(7,'3rd Year','A',1),(8,'3rd Year','B',1),(9,'3rd Year','C',1),
-- COMP
(10,'1st Year','A',2),(11,'2nd Year','A',2),(12,'3rd Year','A',2),
-- CIVIL
(13,'1st Year','A',3),(14,'2nd Year','A',3),(15,'3rd Year','A',3),
-- MECH
(16,'1st Year','A',4),(17,'2nd Year','A',4),(18,'3rd Year','A',4),
-- ELEC
(19,'1st Year','A',5),(20,'2nd Year','A',5),(21,'3rd Year','A',5);

-- Subjects from both timetables
DROP TABLE IF EXISTS `subjects`;
CREATE TABLE `subjects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject_name` varchar(255) DEFAULT NULL,
  `subject_code` varchar(20) DEFAULT NULL,
  `department_id` int(11) DEFAULT NULL,
  `semester` varchar(10) DEFAULT NULL,
  `class` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `subjects` (id,subject_name,subject_code,department_id,semester,class) VALUES
(1,'Management','315301',1,'6','3rd Year'),
(2,'Big Data Analytics','316318',1,'6','3rd Year'),
(3,'Principles of Image Processing','316319',1,'6','3rd Year'),
(4,'Mobile Application Development','316006',1,'6','3rd Year'),
(5,'Network Management and Administration','316007',1,'6','3rd Year'),
(6,'Capstone Project','316004',1,'6','3rd Year'),
(7,'Advanced Algorithm in AI & ML','316320',1,'6','3rd Year'),
(8,'Environmental Education & Sustainability','314301',1,'4','2nd Year'),
(9,'Java Programming','314317',1,'4','2nd Year'),
(10,'Data Communication & Computer Network','314318',1,'4','2nd Year'),
(11,'Mathematics for Machine Learning','314320',1,'4','2nd Year'),
(12,'Microprocessor Programming','314321',1,'4','2nd Year'),
(13,'UI/UX Design','314005',1,'4','2nd Year'),
(14,'Engineering Maths-I','S201',1,'2','1st Year'),
(15,'Applied Physics','S202',1,'2','1st Year'),
(16,'Basic Electronics','S203',1,'2','1st Year'),
(17,'Operating Systems','C601',2,'6','3rd Year'),
(18,'DBMS','C401',2,'4','2nd Year'),
(19,'Computer Networks','C602',2,'6','3rd Year'),
(20,'Design of Steel Structures','V601',3,'6','3rd Year'),
(21,'Concrete Technology','V401',3,'4','2nd Year'),
(22,'Thermodynamics','M601',4,'6','3rd Year'),
(23,'Fluid Mechanics','M401',4,'4','2nd Year'),
(24,'Power Systems','E601',5,'6','3rd Year'),
(25,'Control Systems','E401',5,'4','2nd Year');

-- Students
DROP TABLE IF EXISTS `students`;
CREATE TABLE `students` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `roll_no` varchar(50) DEFAULT NULL,
  `enrollment_no` varchar(100) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `class` varchar(10) DEFAULT NULL,
  `department_id` int(11) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `seat_type` varchar(50) DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `parent_mobile` varchar(15) DEFAULT NULL,
  `parent_whatsapp` varchar(15) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `blood_group` varchar(5) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT 'Stud123',
  `mark_10th` decimal(5,2) DEFAULT NULL,
  `mark_sem1` decimal(5,2) DEFAULT NULL,
  `mark_sem2` decimal(5,2) DEFAULT NULL,
  `mark_sem3` decimal(5,2) DEFAULT NULL,
  `mark_sem4` decimal(5,2) DEFAULT NULL,
  `mark_sem5` decimal(5,2) DEFAULT NULL,
  `mark_sem6` decimal(5,2) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `students` VALUES
(1,'01','AIML601','Patil Ankita Tanaji','ankita@student.kppatil.edu','3rd Year',1,'Female','OBC (Other Backward Class)','CAP Round (Regular)','9988770001','8898890001','8898890001','Mudal','O+','','Stud123',88.00,79.00,82.00,77.00,80.00,75.00,NULL,NOW(),NOW()),
(2,'02','AIML602','Anushka Patil','anushka@student.kppatil.edu','3rd Year',1,'Female','OPEN (General)','CAP Round (Regular)','9988770002','8898890002','8898890002','Sangli','B+','','Stud123',91.00,83.00,85.00,80.00,82.00,79.00,NULL,NOW(),NOW()),
(3,'03','AIML603','Rahul Patil','rahulp@student.kppatil.edu','3rd Year',1,'Male','OPEN (General)','CAP Round (Regular)','9988770003','8898890003','8898890003','Pune','A+','','Stud123',76.00,70.00,72.00,68.00,74.00,73.00,NULL,NOW(),NOW()),
(4,'04','AIML401','Divya Balugade','divya@student.kppatil.edu','2nd Year',1,'Female','OBC (Other Backward Class)','CAP Round (Regular)','9988770004','8898890004','8898890004','Kolhapur','A+','','Stud123',85.50,75.00,78.00,74.00,NULL,NULL,NULL,NOW(),NOW()),
(5,'05','AIML402','Samiksha Barad','samiksha@student.kppatil.edu','2nd Year',1,'Female','OPEN (General)','CAP Round (Regular)','9988770005','8898890005','8898890005','Miraj','B-','','Stud123',79.00,72.00,74.00,70.00,NULL,NULL,NULL,NOW(),NOW()),
(6,'06','AIML201','Sana Khan','sana@student.kppatil.edu','1st Year',1,'Female','OBC (Other Backward Class)','CAP Round (Regular)','9988770006','8898890006','8898890006','Nashik','A-','','Stud123',85.00,71.00,NULL,NULL,NULL,NULL,NULL,NOW(),NOW()),
(7,'07','AIML202','Amit Shinde','amits@student.kppatil.edu','1st Year',1,'Male','SC (Scheduled Caste)','CAP Round (Regular)','9988770007','8898890007','8898890007','Solapur','B+','','Stud123',72.00,68.00,NULL,NULL,NULL,NULL,NULL,NOW(),NOW()),
(8,'01','COMP601','Suraj Jadhav','suraj@student.kppatil.edu','3rd Year',2,'Male','OPEN (General)','CAP Round (Regular)','9988770008','8898890008','8898890008','Kolhapur','B+','','Stud123',82.50,71.00,73.00,76.00,78.00,72.00,NULL,NOW(),NOW()),
(9,'01','MECH601','Akash Yadav','akash@student.kppatil.edu','3rd Year',4,'Male','OPEN (General)','CAP Round (Regular)','9988770018','8898890018','8898890018','Pune','A+','','Stud123',79.00,72.00,74.00,77.00,75.00,70.00,NULL,NOW(),NOW()),
(10,'01','ELEC601','Snehal Jagtap','snehal@student.kppatil.edu','3rd Year',5,'Female','OPEN (General)','CAP Round (Regular)','9988770022','8898890022','8898890022','Sangli','A-','','Stud123',83.00,76.00,78.00,81.00,79.00,74.00,NULL,NOW(),NOW());

-- Academic Calendar (real MSBTE events)
DROP TABLE IF EXISTS `academic_calendar`;
CREATE TABLE `academic_calendar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `department_id` int(11) DEFAULT NULL COMMENT 'NULL=all depts',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `academic_calendar` VALUES
(1,'Eid - Public Holiday','2026-03-28','holiday','Eid celebration — Public Holiday',NULL),
(2,'Mid-Term Exam Begins','2026-04-07','exam','Mid-Term Examination — All departments',NULL),
(3,'Annual Sports Day','2026-04-15','event','Annual sports day celebration',NULL),
(4,'Independence Day','2026-08-15','holiday','Independence Day — National Holiday',NULL),
(5,'Diwali Break','2026-10-20','holiday','Diwali vacation begins',NULL),
(6,'End Semester Exam','2026-05-10','exam','End Semester Examination — All depts',NULL),
(7,'New Academic Year','2026-06-15','event','New academic year begins — 2026-27',NULL),
(8,'MSBTE Winter Exam','2025-11-15','exam','MSBTE Winter 2025 Examination',NULL),
(9,'Republic Day','2026-01-26','holiday','Republic Day — National Holiday',NULL),
(10,'Parents Meeting — AIML','2026-04-20','event','Parent-Teacher Meeting for AIML Dept',1),
(11,'Industrial Visit — AIML','2026-03-15','event','Industrial Visit — AIML SEM6',1);

-- Timetable (from both images)
DROP TABLE IF EXISTS `timetable`;
CREATE TABLE `timetable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class_id` int(11) DEFAULT NULL,
  `subject_id` int(11) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `day` varchar(20) DEFAULT NULL,
  `time_slot` varchar(50) DEFAULT NULL,
  `room_no` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- AIML SEM6 Div A timetable (Image 1: AN 6K)
INSERT INTO `timetable` VALUES
(1,7,2,5,'Monday','10:10-11:05','AIML-6A'),   -- BDA - Maskar
(2,7,7,6,'Tuesday','10:10-11:05','AIML-6A'),  -- AAM - Huddar
(3,7,4,2,'Wednesday','10:10-12:00','AIML-6A'), -- MAD - Kumbhar
(4,7,5,4,'Wednesday','10:10-12:00','AIML-6A'), -- NMA - SS Patil
(5,7,4,4,'Thursday','10:10-11:05','AIML-6A'),  -- MAD - SS Patil
(6,7,5,4,'Thursday','10:10-11:05','AIML-6A'),  -- NMA
(7,7,3,4,'Friday','10:10-11:05','AIML-6A'),    -- PIP
(8,7,1,6,'Monday','12:30-01:30','AIML-6A'),    -- MAN - Huddar
(9,7,7,6,'Monday','12:30-02:30','AIML-6A'),    -- AAM
(10,7,5,4,'Tuesday','12:30-01:30','AIML-6A'),  -- NMA
(11,7,6,7,'Thursday','02:45-04:35','AIML-6A'), -- CPE - AP Patil
(12,7,3,4,'Friday','02:45-03:40','AIML-6A'),   -- PIP
(13,7,1,6,'Saturday','02:45-03:40','AIML-6A'), -- MAN
-- AIML SEM4 Div A timetable (Image 2: AN 4K)
(14,4,13,3,'Monday','10:10-11:05','AIML-4A'),  -- JPR - Bhat
(15,4,11,2,'Tuesday','10:10-11:05','AIML-4A'), -- MML - Kumbhar
(16,4,11,2,'Wednesday','10:10-11:05','AIML-4A'),-- MML
(17,4,12,7,'Thursday','10:10-11:05','AIML-4A'),-- MIC
(18,4,8,4,'Monday','12:30-01:30','AIML-4A'),   -- EES - SS Patil
(19,4,10,3,'Tuesday','12:30-01:30','AIML-4A'), -- DCN - Bhat
(20,4,11,2,'Wednesday','01:30-02:30','AIML-4A'),-- MML
(21,4,13,3,'Tuesday','01:30-02:30','AIML-4A'), -- JPR
(22,4,11,2,'Monday','02:45-03:40','AIML-4A'),  -- MML
(23,4,10,3,'Tuesday','02:45-03:40','AIML-4A'), -- DCN
(24,4,13,3,'Monday','03:40-04:35','AIML-4A'),  -- JPR
(25,4,11,2,'Tuesday','03:40-04:35','AIML-4A'); -- MML

-- Attendance sessions
DROP TABLE IF EXISTS `attendance_sessions`;
CREATE TABLE `attendance_sessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class_id` int(11) DEFAULT NULL,
  `subject_id` int(11) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `qr_token` varchar(255) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'active',
  `qr_image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Attendance
DROP TABLE IF EXISTS `attendance`;
CREATE TABLE `attendance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session_id` int(11) DEFAULT NULL,
  `student_id` int(11) DEFAULT NULL,
  `marked_at` datetime DEFAULT NULL,
  `status` varchar(20) DEFAULT 'present',
  `latitude` varchar(50) DEFAULT NULL,
  `longitude` varchar(50) DEFAULT NULL,
  `location_verified` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_attendance` (`session_id`,`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- SMS/WhatsApp Log
DROP TABLE IF EXISTS `sms_log`;
CREATE TABLE `sms_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) DEFAULT NULL,
  `parent_mobile` varchar(15) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `sent_at` datetime DEFAULT NULL,
  `status` varchar(20) DEFAULT 'sent',
  `type` varchar(30) DEFAULT 'attendance',
  `channel` varchar(20) DEFAULT 'sms',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

COMMIT;

-- ============================================================
-- LOGIN CREDENTIALS v3
-- ============================================================
-- PRINCIPAL : spmore / spmore123
-- HOD AIML  : avadhut_aiml / avadhut123
-- HOD COMP  : hod_comp / hodcomp123
-- TEACHERS  : email / teacher123
--   e.g.  digusuryawanshi@gmail.com / teacher123
--         poojakumbhar912@gmail.com / teacher123
--         maskarkirtiraj@gmail.com  / teacher123
-- STUDENTS  : mobile / Stud123
--   e.g.  9988770001 / Stud123
-- ============================================================

-- ============================================================
-- v11 PATCH: Update D.T. Suryawanshi as Class Teacher (3rd Year)
-- Run this if upgrading an existing database from v10
-- ============================================================
UPDATE teachers
SET designation = 'Class Teacher', is_class_teacher = 'yes'
WHERE email = 'digusuryawanshi@gmail.com';
