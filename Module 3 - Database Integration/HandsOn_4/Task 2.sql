-- 51 Index on enrollment_year
CREATE INDEX idx_students_enrollment_year
ON students(enrollment_year);

-- 52 Composite UNIQUE Index
CREATE UNIQUE INDEX idx_student_course
ON enrollments(student_id, course_id);

-- 53 Index on course_code
CREATE INDEX idx_course_code
ON courses(course_code);

-- 54 Run EXPLAIN Again
EXPLAIN
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e JOIN students s ON s.student_id=e.student_id JOIN courses c
ON c.course_id=e.course_id WHERE s.enrollment_year=2022;

-- Comment
-- Observation:
-- After creating indexes,
-- MySQL uses indexes instead of full table scans
-- wherever possible.
-- Query execution becomes faster.


-- 55. Partial Index

-- MySQL does NOT support Partial Indexes.


-- MySQL does not support Partial Indexes.
-- The following command works only in PostgreSQL:

-- CREATE INDEX idx_null_grade
-- ON enrollments(student_id)
-- WHERE grade IS NULL;