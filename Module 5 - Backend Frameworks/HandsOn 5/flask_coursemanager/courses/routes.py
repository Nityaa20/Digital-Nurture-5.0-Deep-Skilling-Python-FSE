from flask import Blueprint, jsonify, request

from courses.models import Course, Enrollment, Student
from extensions import db

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')


def make_response_json(data, status_code=200):
    return jsonify({'status': 'success', 'data': data}), status_code


@courses_bp.route('/', methods=['GET'])
def list_courses():
    courses = Course.query.all()
    return make_response_json([course.to_dict() for course in courses])


@courses_bp.route('/', methods=['POST'])
def create_course():
    body = request.get_json()
    if body is None:
        return jsonify({'status': 'error', 'message': 'Invalid JSON body'}), 400
    required = ['name', 'code', 'credits', 'department_id']
    missing = [field for field in required if field not in body]
    if missing:
        return jsonify({
            'status': 'error',
            'message': f'Missing required fields: {", ".join(missing)}',
        }), 400
    course = Course(
        name=body['name'],
        code=body['code'],
        credits=body['credits'],
        department_id=body['department_id'],
    )
    db.session.add(course)
    db.session.commit()
    return make_response_json(course.to_dict(), 201)


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return make_response_json(course.to_dict())


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    body = request.get_json()
    if body is None:
        return jsonify({'status': 'error', 'message': 'Invalid JSON body'}), 400
    for field in ['name', 'code', 'credits', 'department_id']:
        if field in body:
            setattr(course, field, body[field])
    db.session.commit()
    return make_response_json(course.to_dict())


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return make_response_json({'deleted': course_id})


@courses_bp.route('/<int:course_id>/students/', methods=['GET'])
def course_students(course_id):
    Course.query.get_or_404(course_id)
    students = (
        db.session.query(Student)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .filter(Enrollment.course_id == course_id)
        .all()
    )
    return make_response_json([student.to_dict() for student in students])
