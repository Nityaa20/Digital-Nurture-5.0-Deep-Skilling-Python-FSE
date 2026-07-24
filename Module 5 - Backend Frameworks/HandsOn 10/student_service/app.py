from datetime import date

import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['COURSE_SERVICE_URL'] = 'http://127.0.0.1:5001'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department_id = db.Column(db.Integer, nullable=False)
    enrollment_year = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'department_id': self.department_id,
            'enrollment_year': self.enrollment_year,
        }


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id'),)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'enrollment_date': self.enrollment_date.isoformat(),
        }


with app.app_context():
    db.create_all()


@app.route('/api/students/', methods=['GET'])
def list_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])


@app.route('/api/students/', methods=['POST'])
def create_student():
    body = request.get_json() or {}
    student = Student(
        first_name=body['first_name'],
        last_name=body['last_name'],
        email=body['email'],
        department_id=body['department_id'],
        enrollment_year=body['enrollment_year'],
    )
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201


@app.route('/api/students/<int:student_id>/', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if student is None:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student.to_dict())


@app.route('/api/students/<int:student_id>/enroll', methods=['POST'])
def enroll_student(student_id):
    student = Student.query.get(student_id)
    if student is None:
        return jsonify({'error': 'Student not found'}), 404
    body = request.get_json() or {}
    course_id = body.get('course_id')
    if course_id is None:
        return jsonify({'error': 'course_id is required'}), 400
    try:
        response = requests.get(
            f"{app.config['COURSE_SERVICE_URL']}/api/courses/{course_id}/",
            timeout=5,
        )
    except requests.ConnectionError:
        return jsonify({
            'error': 'Course Service is unavailable. Enrollment cannot be completed.',
        }), 503
    if response.status_code != 200:
        return jsonify({'error': f'Course {course_id} does not exist'}), 404
    enrollment = Enrollment(
        student_id=student_id,
        course_id=course_id,
        enrollment_date=date.today(),
    )
    db.session.add(enrollment)
    db.session.commit()
    return jsonify(enrollment.to_dict()), 201


if __name__ == '__main__':
    app.run(port=5002, debug=True)
