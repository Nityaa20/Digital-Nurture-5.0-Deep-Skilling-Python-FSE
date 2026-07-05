
 #Task 1 — Set Up Alembic and Create a Baseline Migration

import subprocess


def run(cmd):
    print(f"\n$ {cmd}")
    subprocess.run(cmd, shell=True, check=True)


if __name__ == "__main__":
    # Step 92: Initialise Alembic

    run("alembic init migrations")

    print(
        """
    MANUAL STEP (Step 93) — edit alembic.ini:
        sqlalchemy.url = mysql+mysqlconnector://root:password@localhost:3306/college_db_orm
        (or for PostgreSQL)
        sqlalchemy.url = postgresql+psycopg2://postgres:password@localhost:5432/college_db_orm

    MANUAL STEP (Step 94) — edit migrations/env.py, add near the top:
        import sys, os
        sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
        from models import Base

        Then replace:
            target_metadata = None
        with:
            target_metadata = Base.metadata
    """
    )
    input("Press Enter once alembic.ini and env.py are edited...")

    # Step 95: Generate the first migration from the models
    run('alembic revision --autogenerate -m "initial schema"')

    # Step 96: Inspect the generated file manually
    print(
        "\nStep 96: Open migrations/versions/<hash>_initial_schema.py and "
        "confirm it contains upgrade() and downgrade() functions creating "
        "departments, students, courses, enrollments, professors."
    )

    # Step 97: Apply the migration
    run("alembic upgrade head")
    run("alembic current")

    print(
        "\nExpected Outcome: 'alembic current' shows the revision hash and "
        "all 5 tables + the alembic_version table now exist in college_db_orm."
    )
