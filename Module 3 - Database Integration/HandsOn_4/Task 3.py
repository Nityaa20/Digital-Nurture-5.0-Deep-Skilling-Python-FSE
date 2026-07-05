import mysql.connector
import time

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
    database="college_db"
)

cursor = conn.cursor()

# VERSION 1 - N+1 Problem


print("========== VERSION 1 : N+1 PROBLEM ==========")

start = time.time()

# Query 1
cursor.execute("SELECT * FROM enrollments")
enrollments = cursor.fetchall()

query_count = 1

for enrollment in enrollments:
    student_id = enrollment[1]

    
    cursor.execute(
        "SELECT first_name, last_name FROM students WHERE student_id=%s",
        (student_id,)
    )

    student = cursor.fetchone()

    print(student[0], student[1])

    query_count += 1

end = time.time()

print("\nTotal Queries Executed :", query_count)
print("Execution Time :", round(end - start, 5), "seconds")


# VERSION 2 - USING JOIN


print("\n========== VERSION 2 : USING JOIN ==========")

start = time.time()

cursor.execute("""
SELECT
    s.first_name,
    s.last_name,
    c.course_name,
    e.grade
FROM enrollments e
JOIN students s
ON e.student_id = s.student_id
JOIN courses c
ON e.course_id = c.course_id;
""")

records = cursor.fetchall()

for row in records:
    print(row)

end = time.time()

print("\nTotal Queries Executed : 1")
print("Execution Time :", round(end - start, 5), "seconds")

cursor.close()
conn.close()

"""
Task 59 - Observation

Version 1 (N+1 Problem):
- One query retrieves all enrollments.
- One additional query is executed for each enrollment.
- Total Queries = 13 (1 + 12)

Version 2 (JOIN):
- Only one JOIN query retrieves all required data.
- Total Queries = 1

For a database containing 10,000 enrollments:

N+1 Problem:
1 + 10,000 = 10,001 queries

JOIN Solution:
Only 1 query

Using JOIN greatly improves performance by reducing
database round-trips.
"""