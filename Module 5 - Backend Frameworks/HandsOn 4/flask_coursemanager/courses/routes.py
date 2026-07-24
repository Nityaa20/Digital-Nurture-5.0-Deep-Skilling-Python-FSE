from flask import Blueprint, jsonify, request

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

_courses = []
_next_id = 1


def make_response_json(data, status_code=200):
    return jsonify({'status': 'success', 'data': data}), status_code


@courses_bp.route('/', methods=['GET'])
def list_courses():
    return make_response_json(_courses)


@courses_bp.route('/', methods=['POST'])
def create_course():
    body = request.get_json()
    if body is None:
        return jsonify({'status': 'error', 'message': 'Invalid JSON body'}), 400
    required = ['name', 'code', 'credits']
    missing = [field for field in required if field not in body]
    if missing:
        return jsonify({
            'status': 'error',
            'message': f'Missing required fields: {", ".join(missing)}',
        }), 400
    global _next_id
    course = {
        'id': _next_id,
        'name': body['name'],
        'code': body['code'],
        'credits': body['credits'],
        'department_id': body.get('department_id'),
    }
    _next_id += 1
    _courses.append(course)
    return make_response_json(course, 201)


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = next((c for c in _courses if c['id'] == course_id), None)
    if course is None:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    return make_response_json(course)


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = next((c for c in _courses if c['id'] == course_id), None)
    if course is None:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    body = request.get_json()
    if body is None:
        return jsonify({'status': 'error', 'message': 'Invalid JSON body'}), 400
    for field in ['name', 'code', 'credits']:
        if field in body:
            course[field] = body[field]
    if 'department_id' in body:
        course['department_id'] = body['department_id']
    return make_response_json(course)


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    global _courses
    course = next((c for c in _courses if c['id'] == course_id), None)
    if course is None:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    _courses = [c for c in _courses if c['id'] != course_id]
    return make_response_json({'deleted': course_id})
