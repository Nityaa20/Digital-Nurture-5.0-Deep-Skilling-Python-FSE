from contextlib import asynccontextmanager
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Course, Enrollment, Student, get_db, init_db
from errors import http_exception_handler, not_found, paginate
from schemas import (
    CourseCreate,
    CourseResponse,
    CourseUpdate,
    EnrollmentCreate,
    EnrollmentResponse,
    StudentCreate,
    StudentResponse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title='Course Management API',
    description='REST API with versioning, pagination, and standardised errors.',
    version='1.0',
    lifespan=lifespan,
)
app.add_exception_handler(HTTPException, http_exception_handler)


@app.get('/')
async def root():
    return {'message': 'API running'}


@app.get('/api/v1/courses/', tags=['Courses'])
async def list_courses(
    request: Request,
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Course)
    count_query = select(func.count()).select_from(Course)
    if search:
        pattern = f'%{search}%'
        condition = or_(Course.name.ilike(pattern), Course.code.ilike(pattern))
        query = query.where(condition)
        count_query = count_query.where(condition)
    total = (await db.execute(count_query)).scalar_one()
    offset = (page - 1) * page_size
    result = await db.execute(query.offset(offset).limit(page_size))
    courses = [CourseResponse.model_validate(c) for c in result.scalars().all()]
    return paginate(
        [c.model_dump() for c in courses],
        total,
        page,
        page_size,
        request,
        '/api/v1/courses/',
    )


@app.post('/api/v1/courses/', status_code=status.HTTP_201_CREATED, tags=['Courses'])
async def create_course(
    course: CourseCreate, response: Response, db: AsyncSession = Depends(get_db)
):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    response.headers['Location'] = f'/api/v1/courses/{db_course.id}/'
    return CourseResponse.model_validate(db_course)


@app.get('/api/v1/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if course is None:
        return not_found('Course', course_id)
    return course


@app.put('/api/v1/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def replace_course(
    course_id: int, course: CourseCreate, db: AsyncSession = Depends(get_db)
):
    db_course = await db.get(Course, course_id)
    if db_course is None:
        return not_found('Course', course_id)
    for key, value in course.model_dump().items():
        setattr(db_course, key, value)
    await db.commit()
    await db.refresh(db_course)
    return db_course


@app.patch('/api/v1/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def patch_course(
    course_id: int, course: CourseUpdate, db: AsyncSession = Depends(get_db)
):
    db_course = await db.get(Course, course_id)
    if db_course is None:
        return not_found('Course', course_id)
    for key, value in course.model_dump(exclude_unset=True).items():
        setattr(db_course, key, value)
    await db.commit()
    await db.refresh(db_course)
    return db_course


@app.delete('/api/v1/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    db_course = await db.get(Course, course_id)
    if db_course is None:
        return not_found('Course', course_id)
    await db.delete(db_course)
    await db.commit()


@app.get('/api/v1/courses/{course_id}/students/', response_model=list[StudentResponse], tags=['Courses'])
async def course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if course is None:
        return not_found('Course', course_id)
    result = await db.execute(
        select(Student)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .where(Enrollment.course_id == course_id)
    )
    return result.scalars().all()


@app.get('/api/v1/students/', response_model=list[StudentResponse], tags=['Students'])
async def list_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student))
    return result.scalars().all()


@app.post(
    '/api/v1/students/',
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Students'],
)
async def create_student(
    student: StudentCreate, response: Response, db: AsyncSession = Depends(get_db)
):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    response.headers['Location'] = f'/api/v1/students/{db_student.id}/'
    return db_student


@app.post(
    '/api/v1/enrollments/',
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Enrollments'],
)
async def create_enrollment(
    enrollment: EnrollmentCreate, response: Response, db: AsyncSession = Depends(get_db)
):
    student = await db.get(Student, enrollment.student_id)
    if student is None:
        return not_found('Student', enrollment.student_id)
    course = await db.get(Course, enrollment.course_id)
    if course is None:
        return not_found('Course', enrollment.course_id)
    db_enrollment = Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    await db.commit()
    await db.refresh(db_enrollment)
    response.headers['Location'] = f'/api/v1/enrollments/{db_enrollment.id}/'
    return db_enrollment
