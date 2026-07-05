"""

COMMENT BLOCK — Query count comparison (Steps 87-90)

Lazy loading (crud.py, step_84):
    1 query  -> SELECT * FROM enrollments
    N queries -> one SELECT per row to fetch enrollment.student
    N queries -> one SELECT per row to fetch enrollment.course
    Total: 1 + N + N queries (e.g. 4 enrollments -> 9 queries; with the
    full sample dataset of 12 enrollments -> 1 + 12 + 12 = 25 queries,
    commonly summarised as "13 queries executed" when only one related
    object — e.g. student — is lazily loaded per row: 1 + 12 = 13).

Eager loading with joinedload (this file, step_89):
    1 query total -> a single SQL statement using LEFT OUTER JOIN to pull
    enrollments + students + courses together.

    Result: query count drops from 13 (or 25) down to 1.

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload

from models import Enrollment, DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)  
Session = sessionmaker(bind=engine)
session = Session()


def step_88_eager_load_with_joinedload():
    enrollments = (
        session.query(Enrollment)
        .options(
            joinedload(Enrollment.student),
            joinedload(Enrollment.course),
        )
        .all()
    )
    print("Step 88-89: Enrollments loaded with a single JOIN query:")
    for e in enrollments:
        print(f"  - {e.student.first_name} {e.student.last_name} -> {e.course.course_name}")
    return enrollments


if __name__ == "__main__":
    step_88_eager_load_with_joinedload()
    session.close()


# ----------------------------------------------------------------------------
# Equivalent fix in Django ORM, for reference only:
#
#   from myapp.models import Enrollment
#
#   enrollments = Enrollment.objects.select_related('student', 'course').all()
#   for e in enrollments:
#       print(e.student.first_name, e.student.last_name, '->', e.course.course_name)
#
# select_related() performs a SQL JOIN and includes the related object's
# fields in the SELECT statement, eliminating the extra per-row queries
# the same way joinedload() does in SQLAlchemy.
# ----------------------------------------------------------------------------
