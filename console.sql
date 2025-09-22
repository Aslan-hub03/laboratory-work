--Task 1.1 1)
DROP DATABASE IF EXISTS university_main;
CREATE DATABASE university_main
    WITH OWNER = postgres
    TEMPLATE = template0
    ENCODING 'UTF8';
--Task 1.1 2)
CREATE DATABASE university_archive
 WITH template = template0
    CONNECTION LIMIT = 50;
--Task 1.1 3)
CREATE DATABASE university_test
    WITH IS_TEMPLATE = TRUE
        CONNECTION LIMIT = 10;
--Task 1.2
CREATE TABLESPACE student_data LOCATION 'C:\student_data';

CREATE TABLESPACE course_data
    OWNER postgres
    LOCATION 'C:\course_data';
CREATE DATABASE university_distributed
    WITH TABLESPACE = student_data
    ENCODING 'UTF8'
    TEMPLATE template0;

--Task 2
CREATE TABLE students(
    student_id SERIAL PRIMARY KEY ,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone CHAR(15),
    date_of_birth DATE,
    enrollment_date DATE,
    gpa NUMERIC(3,2),
    is_active BOOLEAN,
    graduation_year SMALLINT
);

CREATE TABLE professors(
                        professor_id SERIAL PRIMARY KEY ,
                        first_name VARCHAR(50),
                        last_name VARCHAR(50),
                        email VARCHAR(100),
                        office_number VARCHAR(20),
                        hire_date DATE,
                        salary NUMERIC(12,2),
                        is_tenured BOOLEAN,
                        years_experience INT
);
CREATE TABLE courses(
    course_id SERIAL PRIMARY KEY ,
    course_code CHAR(8),
    course_title VARCHAR(100),
    description TEXT,
    credits SMALLINT,
    max_enrollment INT,
    course_fee NUMERIC(10,2),
    is_online BOOLEAN,
    duration INTERVAL
);
CREATE TABLE class_schedule(
    schedule_id SERIAL PRIMARY KEY ,
    course_id INT,
    professor_id INT,
    classroom VARCHAR(20),
    class_date DATE,
    start_time TIME WITHOUT TIME ZONE,
    end_time TIME WITHOUT TIME ZONE,
    duration INTERVAL
);
CREATE TABLE student_records(
    record_id SERIAL PRIMARY KEY ,
    student_id INT,
    course_id INT,
    semester VARCHAR(20),
    year INT,
    grade CHAR(2),
    attendance_percentage NUMERIC(4,1),
    submission_timestamp TIMESTAMP WITH TIME ZONE,
    last_updated TIMESTAMP WITH TIME ZONE
);

ALTER TABLE students
ADD COLUMN middle_name VARCHAR(30),
ADD COLUMN student_status VARCHAR(20);

ALTER TABLE students
ALTER COLUMN phone TYPE varchar(20);

ALTER TABLE students
ALTER COLUMN student_status SET DEFAULT 'ACTIVE';

ALTER TABLE students
ALTER COLUMN gpa SET DEFAULT 0.00;

ALTER TABLE professors
ADD COLUMN department_code CHAR(5),
ADD COLUMN student_status TEXT;

ALTER TABLE professors
ALTER COLUMN years_experience TYPE smallint;

ALTER TABLE professors
ALTER COLUMN is_tenured SET DEFAULT FALSE;

ALTER TABLE professors
ADD COLUMN last_promotion_date DATE;

ALTER TABLE courses
ADD COLUMN prerequisite_course_id INT,
ADD COLUMN difficulty_level smallint;

ALTER TABLE courses
ALTER COLUMN course_code TYPE VARCHAR(10);

ALTER TABLE courses
ALTER COLUMN credits SET DEFAULT 3;

ALTER TABLE courses
ADD COLUMN lab_required BOOLEAN  DEFAULT FALSE;

ALTER TABLE class_schedule
    ADD COLUMN room_capacity INT,
    DROP COLUMN duration,
    ADD COLUMN session_type VARCHAR(15),
    ALTER COLUMN classroom TYPE VARCHAR(30),
    ADD COLUMN equipment_needed TEXT;

ALTER TABLE student_records
    ADD COLUMN extra_credit_points NUMERIC(4,1),
    ALTER COLUMN grade TYPE VARCHAR(5),
    ALTER COLUMN extra_credit_points SET DEFAULT 0.0,
    ADD COLUMN final_exam_date DATE,
    DROP COLUMN last_updated;
--Task 4.1
CREATE TABLE departments(
    department_id SERIAL PRIMARY KEY ,
    department_name VARCHAR(100),
    department_code CHAR(5),
    building VARCHAR(50),
    phone VARCHAR(15),
    budget DECIMAL(12,2),
    established_year INT
);
CREATE TABLE library_books(
    book_id SERIAL PRIMARY KEY ,
    isbn CHAR(13),
    title VARCHAR(200),
    author VARCHAR(100),
    publisher VARCHAR(100),
    publication_date DATE,
    price DECIMAL (10,2),
    is_avaiable BOOLEAN,
    acquisition_timesamp TIMESTAMP WITHOUT TIME ZONE
);

CREATE TABLE student_book_loans (
    loan_id SERIAL PRIMARY KEY,
    student_id INT,
    book_id INT,
    loan_date DATE,
    due_date DATE,
    return_date DATE,
    fine_amount NUMERIC(10,2),
    loan_status VARCHAR(20)
);

--TASK 4.2
ALTER TABLE professors
    ADD COLUMN department_id INT;

ALTER TABLE students
    ADD COLUMN advisor_id INT;

ALTER TABLE courses
    ADD COLUMN department_id INT;

CREATE TABLE grade_scale (
                             grade_id SERIAL PRIMARY KEY,
                             letter_grade CHAR(2) NOT NULL,
                             min_percentage DECIMAL(4,1),
                             max_percentage DECIMAL(4,1),
                             gpa_points DECIMAL(3,2)
);

CREATE TABLE semester_calendar (
                                   semester_id SERIAL PRIMARY KEY,
                                   semester_name VARCHAR(20) NOT NULL,
                                   academic_year INT NOT NULL,
                                   start_date DATE NOT NULL,
                                   end_date DATE NOT NULL,
                                   registration_deadline TIMESTAMPTZ NOT NULL,
                                   is_current BOOLEAN DEFAULT FALSE
);

--TASK 5.1
DROP TABLE IF EXISTS student_book_loans;
DROP TABLE IF EXISTS library_books;
DROP TABLE IF EXISTS grade_scale;

CREATE TABLE grade_scale (
                             grade_id SERIAL PRIMARY KEY,
                             letter_grade CHAR(2),
                             min_percentage DECIMAL(4,1),
                             max_percentage DECIMAL(4,1),
                             gpa_points DECIMAL(3,2),
                             description TEXT
);

DROP TABLE IF EXISTS semester_calendar CASCADE;

CREATE TABLE semester_calendar (
                                   semester_id SERIAL PRIMARY KEY,
                                   semester_name VARCHAR(20),
                                   academic_year INT,
                                   start_date DATE,
                                   end_date DATE,
                                   registration_deadline TIMESTAMP WITH TIME ZONE,
                                   is_current BOOLEAN
);

UPDATE pg_database
SET datistemplate = false
WHERE datname = 'university_test';


UPDATE pg_database
SET datistemplate = false
WHERE datname = 'university_distributed';


DROP DATABASE IF EXISTS university_test;
DROP DATABASE IF EXISTS university_distributed;

CREATE DATABASE university_backup
    WITH TEMPLATE = university_main
    OWNER = postgres;