from decimal import Decimal

from app import create_app
from courses.models import Course, Department
from extensions import db

app = create_app()

with app.app_context():
    cs = Department(name='Computer Science', head_of_dept='Dr. Smith', budget=Decimal('500000'))
    math = Department(name='Mathematics', head_of_dept='Dr. Johnson', budget=Decimal('300000'))
    db.session.add_all([cs, math])
    db.session.commit()
    db.session.add_all([
        Course(name='Data Structures', code='CS101', credits=4, department_id=cs.id),
        Course(name='Algorithms', code='CS201', credits=4, department_id=cs.id),
        Course(name='Calculus I', code='MATH101', credits=3, department_id=math.id),
    ])
    db.session.commit()
    print('Seeded:', [c.to_dict() for c in Course.query.all()])
