"""
Run this AFTER models.py has created the tables in college_db_orm.
"""

from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Department, Student, Course, Enrollment, Professor, DATABASE_URL

# echo=True prints every SQL statement -> useful for spotting the N+1 problem
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def step_81_insert_departments_and_students():
    departments = [
        Department(dept_name="Computer Science", hod_name="Dr. Ramesh Kumar", budget=850000.00),
        Department(dept_name="Electronics", hod_name="Dr. Priya Nair", budget=620000.00),
        Department(dept_name="Mechanical", hod_name="Dr. Suresh Iyer", budget=540000.00),
    ]
    session.add_all(departments)
    session.commit()

    cs_dept = session.query(Department).filter_by(dept_name="Computer Science").first()

    students = [
        Student(first_name="Arjun", last_name="Mehta", email="arjun.mehta@college.edu",
                date_of_birth=date(2003, 4, 12), department_id=cs_dept.department_id, enrollment_year=2022),
        Student(first_name="Priya", last_name="Suresh", email="priya.suresh@college.edu",
                date_of_birth=date(2003, 7, 25), department_id=cs_dept.department_id, enrollment_year=2022),
        Student(first_name="Vikram", last_name="Das", email="vikram.das@college.edu",
                date_of_birth=date(2003, 9, 14), department_id=cs_dept.department_id, enrollment_year=2022),
        Student(first_name="Deepika", last_name="Rao", email="deepika.rao@college.edu",
                date_of_birth=date(2003, 8, 9), department_id=cs_dept.department_id, enrollment_year=2022),
        Student(first_name="Rohan", last_name="Verma", email="rohan.verma@college.edu",
                date_of_birth=date(2002, 11, 8), department_id=cs_dept.department_id, enrollment_year=2021),
    ]
    session.add_all(students)
    session.commit()
    print("Step 81: Inserted 3 departments and 5 students.")


def step_82_insert_courses_and_enrollments():
    cs_dept = session.query(Department).filter_by(dept_name="Computer Science").first()

    courses = [
        Course(course_name="Data Structures & Algorithms", course_code="CS101", credits=4,
               department_id=cs_dept.department_id),
        Course(course_name="Database Management Systems", course_code="CS102", credits=3,
               department_id=cs_dept.department_id),
        Course(course_name="Object Oriented Programming", course_code="CS103", credits=4,
               department_id=cs_dept.department_id),
    ]
    session.add_all(courses)
    session.commit()

    students = session.query(Student).limit(4).all()
    dsa = session.query(Course).filter_by(course_code="CS101").first()
    dbms = session.query(Course).filter_by(course_code="CS102").first()

    enrollments = [
        Enrollment(student_id=students[0].student_id, course_id=dsa.course_id,
                   enrollment_date=date(2022, 7, 1), grade="A"),
        Enrollment(student_id=students[0].student_id, course_id=dbms.course_id,
                   enrollment_date=date(2022, 7, 1), grade="B"),
        Enrollment(student_id=students[1].student_id, course_id=dsa.course_id,
                   enrollment_date=date(2022, 7, 1), grade="B"),
        Enrollment(student_id=students[2].student_id, course_id=dbms.course_id,
                   enrollment_date=date(2022, 7, 1), grade="C"),
    ]
    session.add_all(enrollments)
    session.commit()
    print("Step 82: Inserted 3 courses and 4 enrollments.")


def step_83_read_students_in_cs():
    results = (
        session.query(Student)
        .join(Department)
        .filter(Department.dept_name == "Computer Science")
        .all()
    )
    print("Step 83: Students in Computer Science:")
    for s in results:
        print(f"  - {s.first_name} {s.last_name}")
    return results


def step_84_read_enrollments_with_student_and_course():
    # NOTE: With lazy loading (the default), accessing enrollment.student and
    # enrollment.course inside the loop issues a SEPARATE query per row.
    # This is the N+1 problem -> 1 query for enrollments + N queries for
    # related student/course lookups. Watch the echo=True SQL log to confirm.
    print("Step 84: Enrollments (watch SQL log below for N+1 pattern):")
    enrollments = session.query(Enrollment).all()
    for e in enrollments:
        print(f"  - {e.student.first_name} {e.student.last_name} -> {e.course.course_name}")


def step_85_update_enrollment_year():
    student = session.query(Student).filter_by(email="arjun.mehta@college.edu").first()
    if student:
        student.enrollment_year = 2023
        session.commit()
        print(f"Step 85: Updated {student.first_name}'s enrollment_year to {student.enrollment_year}.")


def step_86_delete_enrollment():
    enrollment = session.query(Enrollment).first()
    if enrollment:
        enrollment_id = enrollment.enrollment_id
        session.delete(enrollment)
        session.commit()
        print(f"Step 86: Deleted enrollment_id={enrollment_id}.")


if __name__ == "__main__":
    step_81_insert_departments_and_students()
    step_82_insert_courses_and_enrollments()
    step_83_read_students_in_cs()
    step_84_read_enrollments_with_student_and_course()
    step_85_update_enrollment_year()
    step_86_delete_enrollment()
    session.close()
