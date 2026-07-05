Use college_db;

-- Add phone_number column
ALTER TABLE students
ADD phone_number VARCHAR(15);

-- Add max_seats column
ALTER TABLE courses
ADD max_seats INT DEFAULT 60;

-- Add CHECK constraint for grades
ALTER TABLE enrollments
ADD CONSTRAINT chk_grade
CHECK (grade IN ('A','B','C','D','F') OR grade IS NULL);

-- Rename hod_name to head_of_dept
ALTER TABLE departments
RENAME COLUMN hod_name TO head_of_dept;

-- Drop phone_number column
ALTER TABLE students
DROP COLUMN phone_number;