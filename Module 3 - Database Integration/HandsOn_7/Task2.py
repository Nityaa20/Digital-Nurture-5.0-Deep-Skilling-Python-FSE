# Task 2 — Add and Apply Incremental Migrations


import subprocess


def run(cmd):
    print(f"\n$ {cmd}")
    subprocess.run(cmd, shell=True, check=True)


MODELS_SNIPPET_IS_ACTIVE = '''
# --- Step 98: add to the Student class in models.py ---
from sqlalchemy import Boolean

class Student(Base):
    __tablename__ = "students"
    ...
    is_active = Column(Boolean, default=True)
'''

MODELS_SNIPPET_COURSE_SCHEDULE = '''
# --- Step 102: add a new model to models.py ---
from sqlalchemy import Time

class CourseSchedule(Base):
    __tablename__ = "course_schedules"

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    day_of_week = Column(String(10))
    start_time = Column(Time)
    end_time = Column(Time)

    course = relationship("Course")
'''


if __name__ == "__main__":
    # Step 98: Add is_active to the Student model
    print(MODELS_SNIPPET_IS_ACTIVE)
    input("Add the snippet above to models.py, save, then press Enter...")

    # Step 99: Generate the migration
    run('alembic revision --autogenerate -m "add is_active to students"')

    # Step 100: Inspect the generated migration manually
    print(
        "\nStep 100: Confirm the new file's upgrade() calls "
        "op.add_column('students', sa.Column('is_active', sa.Boolean(), "
        "server_default=sa.true())) and downgrade() drops it."
    )

    # Step 101: Apply it
    run("alembic upgrade head")

    # Step 102: Add the CourseSchedule model
    print(MODELS_SNIPPET_COURSE_SCHEDULE)
    input("Add the snippet above to models.py, save, then press Enter...")

    run('alembic revision --autogenerate -m "add course_schedule table"')
    run("alembic upgrade head")

    # Step 103: View the full migration chain
    run("alembic history --verbose")

    print(
        "\nExpected Outcome: 'alembic history' shows 3 revisions. The "
        "students table has an is_active column and a course_schedules "
        "table now exists."
    )
