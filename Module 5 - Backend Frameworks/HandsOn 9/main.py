from contextlib import asynccontextmanager
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Course, User, get_db, init_db
from errors import http_exception_handler, not_found, paginate
from schemas import (
    CourseCreate,
    CourseResponse,
    CourseUpdate,
    TokenResponse,
    UserLogin,
    UserRegister,
)
from security import create_access_token, decode_access_token, get_password_hash, verify_password

# OAuth2 Authorization Code flow: the client redirects the user to an authorization server,
# the user grants consent, and the server returns an authorization code exchanged for tokens.
# It is suited for third-party apps and browser-based login. Simple JWT login (Resource Owner
# Password flow) sends credentials directly to the API — simpler but less secure for public clients.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login/', auto_error=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title='Course Management API',
    description='Secured REST API with JWT authentication and CORS.',
    version='1.0',
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_exception_handler(HTTPException, http_exception_handler)


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    if token is None:
        raise HTTPException(status_code=401, detail='Not authenticated')
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail='Invalid or expired token')
    email = payload.get('sub')
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail='Invalid or expired token')
    return user


@app.get('/')
async def root():
    return {'message': 'API running'}


@app.post('/api/v1/auth/register/', status_code=status.HTTP_201_CREATED, tags=['Auth'])
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == user_data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail='Email already registered')
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        is_active=True,
    )
    db.add(user)
    await db.commit()
    return {'email': user.email}


@app.post('/api/v1/auth/login/', response_model=TokenResponse, tags=['Auth'])
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token({'sub': user.email})
    return TokenResponse(access_token=token)


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
    course: CourseCreate,
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
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


@app.patch('/api/v1/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def patch_course(
    course_id: int,
    course: CourseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
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
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_course = await db.get(Course, course_id)
    if db_course is None:
        return not_found('Course', course_id)
    await db.delete(db_course)
    await db.commit()
