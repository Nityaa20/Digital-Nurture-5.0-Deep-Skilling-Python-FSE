from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///course_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    head_of_dept = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Numeric(12, 2), nullable=False)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'credits': self.credits,
            'department_id': self.department_id,
        }


with app.app_context():
    db.create_all()


@app.route('/api/courses/', methods=['GET'])
def list_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses])


@app.route('/api/courses/', methods=['POST'])
def create_course():
    body = request.get_json() or {}
    course = Course(
        name=body['name'],
        code=body['code'],
        credits=body['credits'],
        department_id=body['department_id'],
    )
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201


@app.route('/api/courses/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if course is None:
        return jsonify({'error': 'Course not found'}), 404
    return jsonify(course.to_dict())


if __name__ == '__main__':
    app.run(port=5001, debug=True)
