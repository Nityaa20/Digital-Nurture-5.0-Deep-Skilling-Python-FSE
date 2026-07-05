
#Task 3 — Rollback and Recovery


import subprocess


def run(cmd, check=True):
    print(f"\n$ {cmd}")
    subprocess.run(cmd, shell=True, check=check)


if __name__ == "__main__":
    # Step 104: Note the current head revision hash
    run("alembic current")
    head_hash = input(
        "\nCopy the revision hash printed above, then press Enter to continue..."
    )

    # Step 105: Roll back one step (reverts the most recently applied
    # revision — in this chain that's the course_schedules migration).
    # To specifically undo is_active, roll back two steps instead:
    #   alembic downgrade -2
    run("alembic downgrade -1")
    print(
        "Step 105: Confirm the most recently applied change "
        "(course_schedules table) has been reverted using your SQL client."
    )

    # Step 106: Roll back ALL the way to the very first revision
    run("alembic downgrade base")
    print(
        "Step 106: Confirm all 3 migrations are undone — students table no "
        "longer has is_active, course_schedules no longer exists, but the "
        "original 5 tables from Hands-On 1 remain (Alembic only manages "
        "schema changes it tracked)."
    )

    # Step 107: Re-apply everything to get back to the latest state
    run("alembic upgrade head")
    run("alembic current")
    print(
        "Step 107: Confirm 'alembic current' now matches the hash noted "
        "in Step 104 — you're back at the latest revision."
    )

    print(
        """
    Step 108 (Bonus) — Django Migrations equivalent, run manually if using Django:

        $ python manage.py makemigrations
        $ python manage.py migrate
        $ python manage.py migrate <app_name> <previous_migration_number>
    """
    )