from contextlib import asynccontextmanager
from datetime import date
from typing import Optional

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Course, Enrollment, Student, get_db, init_db
from schemas import (
    CourseCreate,
    CourseResponse,
    CourseUpdate,
    EnrollmentCreate,
    EnrollmentResponse,
    StudentCreate,
    StudentResponse,
    StudentUpdate,
)


def send_confirmation_email(student_email: str):
    print(f'Sending confirmation to {student_email}')


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title='Course Management API',
    description='REST API for managing college courses, students, and enrollments.',
    version='1.0',
    contact={'name': 'Course Admin', 'email': 'admin@college.edu'},
    lifespan=lifespan,
)


@app.get('/', tags=['Health'])
async def root():
    return {'message': 'API running'}


@app.get('/api/courses/', response_model=list[CourseResponse], tags=['Courses'])
async def list_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Course)
    if department_id is not None:
        query = query.where(Course.department_id == department_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@app.post(
    '/api/courses/',
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Courses'],
    summary='Create a new course',
    response_description='The newly created course',
)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course


@app.get('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


@app.put('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def update_course(
    course_id: int, course: CourseCreate, db: AsyncSession = Depends(get_db)
):
    db_course = await db.get(Course, course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    for key, value in course.model_dump().items():
        setattr(db_course, key, value)
    await db.commit()
    await db.refresh(db_course)
    return db_course


@app.delete('/api/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    db_course = await db.get(Course, course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    await db.delete(db_course)
    await db.commit()


@app.get('/api/courses/{course_id}/students/', response_model=list[StudentResponse], tags=['Courses'])
async def course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    result = await db.execute(
        select(Student)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .where(Enrollment.course_id == course_id)
    )
    return result.scalars().all()


@app.get('/api/students/', response_model=list[StudentResponse], tags=['Students'])
async def list_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student))
    return result.scalars().all()


@app.post(
    '/api/students/',
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Students'],
)
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student


@app.get('/api/students/{student_id}', response_model=StudentResponse, tags=['Students'])
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')
    return student


@app.put('/api/students/{student_id}', response_model=StudentResponse, tags=['Students'])
async def update_student(
    student_id: int, student: StudentUpdate, db: AsyncSession = Depends(get_db)
):
    db_student = await db.get(Student, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail='Student not found')
    for key, value in student.model_dump(exclude_unset=True).items():
        setattr(db_student, key, value)
    await db.commit()
    await db.refresh(db_student)
    return db_student


@app.delete('/api/students/{student_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Students'])
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    db_student = await db.get(Student, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail='Student not found')
    await db.delete(db_student)
    await db.commit()


@app.get('/api/enrollments/', response_model=list[EnrollmentResponse], tags=['Enrollments'])
async def list_enrollments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Enrollment))
    return result.scalars().all()


@app.post(
    '/api/enrollments/',
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Enrollments'],
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    student = await db.get(Student, enrollment.student_id)
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')
    course = await db.get(Course, enrollment.course_id)
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    db_enrollment = Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    await db.commit()
    await db.refresh(db_enrollment)
    background_tasks.add_task(send_confirmation_email, student.email)
    return db_enrollment


@app.get('/api/enrollments/{enrollment_id}', response_model=EnrollmentResponse, tags=['Enrollments'])
async def get_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    enrollment = await db.get(Enrollment, enrollment_id)
    if enrollment is None:
        raise HTTPException(status_code=404, detail='Enrollment not found')
    return enrollment


@app.delete(
    '/api/enrollments/{enrollment_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Enrollments'],
)
async def delete_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    enrollment = await db.get(Enrollment, enrollment_id)
    if enrollment is None:
        raise HTTPException(status_code=404, detail='Enrollment not found')
    await db.delete(enrollment)
    await db.commit()
