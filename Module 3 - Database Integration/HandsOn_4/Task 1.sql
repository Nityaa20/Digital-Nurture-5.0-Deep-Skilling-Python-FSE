use college_db;
-- Run EXPLAIN

EXPLAIN
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- Identify whether the query plan shows sequential scan or ffull table scan on any table

-- Observation:
-- Before creating indexes, MySQL performs a Full Table Scan
-- on one or more tables because no suitable index exists.

-- Note the estimated cost or rows examined in your comments

-- Estimated rows examined can be viewed in the EXPLAIN output.
-- Since this is a small dataset, the execution cost is low,
-- but for large datasets performance would decrease.