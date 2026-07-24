import os
from datetime import date
from decimal import Decimal

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')
django.setup()

from django.db import connection, reset_queries
from django.db.models import Count, F

from courses.models import Course, Department, Student


def run_orm_exercises():
    cs_dept = Department.objects.create(
        name='Computer Science',
        head_of_dept='Dr. Smith',
        budget=Decimal('500000.00'),
    )
    math_dept = Department.objects.create(
        name='Mathematics',
        head_of_dept='Dr. Johnson',
        budget=Decimal('300000.00'),
    )

    Course.objects.create(
        name='Data Structures', code='CS101', credits=4, department=cs_dept
    )
    Course.objects.create(
        name='Algorithms', code='CS201', credits=4, department=cs_dept
    )
    Course.objects.create(
        name='Calculus I', code='MATH101', credits=3, department=math_dept
    )
    Course.objects.create(
        name='Linear Algebra', code='MATH201', credits=3, department=math_dept
    )

    Student.objects.create(
        first_name='Alice',
        last_name='Brown',
        email='alice@college.edu',
        department=cs_dept,
        enrollment_year=2024,
    )
    Student.objects.create(
        first_name='Bob',
        last_name='Davis',
        email='bob@college.edu',
        department=cs_dept,
        enrollment_year=2023,
    )
    Student.objects.create(
        first_name='Carol',
        last_name='Evans',
        email='carol@college.edu',
        department=math_dept,
        enrollment_year=2024,
    )
    Student.objects.create(
        first_name='David',
        last_name='Foster',
        email='david@college.edu',
        department=math_dept,
        enrollment_year=2022,
    )
    Student.objects.create(
        first_name='Eve',
        last_name='Garcia',
        email='eve@college.edu',
        department=cs_dept,
        enrollment_year=2025,
    )

    cs_courses = Course.objects.filter(department__name='Computer Science')
    print('CS courses:', list(cs_courses.values('name', 'code')))

    dept_counts = Department.objects.annotate(course_count=Count('course')).values(
        'name', 'course_count'
    )
    print('Course count per department:', list(dept_counts))

    reset_queries()
    students = list(Student.objects.select_related('department').all())
    print('Students with departments:', [(s.first_name, s.department.name) for s in students])
    print('SQL queries used:', len(connection.queries))

    Department.objects.update(budget=F('budget') * 1.1)
    updated_budgets = list(Department.objects.values('name', 'budget'))
    print('Updated budgets:', updated_budgets)


if __name__ == '__main__':
    run_orm_exercises()
