from datetime import date
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DATABASE_URL = 'sqlite+aiosqlite:///./coursemanager.db'

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = 'department'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    head_of_dept: Mapped[str] = mapped_column(String(100))
    budget: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    courses: Mapped[list['Course']] = relationship(back_populates='department')


class Course(Base):
    __tablename__ = 'course'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    code: Mapped[str] = mapped_column(String(20), unique=True)
    credits: Mapped[int] = mapped_column()
    department_id: Mapped[int] = mapped_column(ForeignKey('department.id'))
    department: Mapped['Department'] = relationship(back_populates='courses')
    enrollments: Mapped[list['Enrollment']] = relationship(back_populates='course')


class Student(Base):
    __tablename__ = 'student'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    department_id: Mapped[int] = mapped_column(ForeignKey('department.id'))
    enrollment_year: Mapped[int] = mapped_column()
    enrollments: Mapped[list['Enrollment']] = relationship(back_populates='student')


class Enrollment(Base):
    __tablename__ = 'enrollment'
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('student.id'))
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    enrollment_date: Mapped[date] = mapped_column()
    grade: Mapped[str | None] = mapped_column(String(2), nullable=True)
    student: Mapped['Student'] = relationship(back_populates='enrollments')
    course: Mapped['Course'] = relationship(back_populates='enrollments')
    __table_args__ = (UniqueConstraint('student_id', 'course_id'),)


async def get_db():
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
