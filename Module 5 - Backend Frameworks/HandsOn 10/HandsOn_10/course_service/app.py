"""
====================================================================
 Digital Nurture 5.0 - Python Backend Frameworks
 HANDS-ON 10 [Advanced] - Microservices Architecture
 SERVICE: Course Service  (runs on port 5001)
====================================================================

WHO THIS IS FOR:
Written for a beginner / fresher. Every microservices concept is
explained in a comment right above where it applies.

WHAT THIS SERVICE OWNS:
   - Departments and Courses
   - Its OWN in-memory "database" (a Python list). In a real system
     this would be its own separate database (e.g. its own Postgres
     instance) - the golden rule of microservices is:

         "Each service owns its data. No other service is allowed
          to reach into this service's database directly."

   Other services (like Student Service) are NOT allowed to read
   this list directly - they must call this service's HTTP API
   instead. That's what makes it a "service" and not just a shared
   module.

HOW TO RUN:
    pip install flask
    python app.py
    (runs on http://127.0.0.1:5001)
====================================================================
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# --------------------------------------------------------------
# This service's OWN data. Nothing outside this file/process
# should ever touch this list directly.
# --------------------------------------------------------------
courses_db = [
    {"id": 1, "name": "Intro to Python", "code": "CS101", "credits": 4, "department_id": 1},
    {"id": 2, "name": "Data Structures", "code": "CS102", "credits": 4, "department_id": 1},
]
next_course_id = 3


@app.route("/api/courses/", methods=["GET"])
def list_courses():
    """List all courses. This is the endpoint Student Service (and
    the Gateway) will call to check whether a course exists."""
    return jsonify(courses_db), 200


@app.route("/api/courses/", methods=["POST"])
def create_course():
    global next_course_id
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "code", "credits", "department_id")):
        return jsonify({"error": "Missing required fields"}), 400

    new_course = {
        "id": next_course_id,
        "name": data["name"],
        "code": data["code"],
        "credits": data["credits"],
        "department_id": data["department_id"],
    }
    courses_db.append(new_course)
    next_course_id += 1
    return jsonify(new_course), 201


@app.route("/api/courses/<int:course_id>/", methods=["GET"])
def get_course(course_id):
    """
    Student Service calls THIS endpoint (over HTTP, using the
    `requests` library) whenever it needs to check "does this
    course exist?" before enrolling a student.
    """
    for course in courses_db:
        if course["id"] == course_id:
            return jsonify(course), 200
    return jsonify({"error": "Course not found"}), 404


@app.route("/", methods=["GET"])
def health_check():
    """
    A tiny endpoint just to confirm this service is alive. Real
    microservice systems often have a dedicated /health endpoint
    that load balancers and service-discovery tools ping regularly.
    """
    return jsonify({"service": "course_service", "status": "running", "port": 5001}), 200


if __name__ == "__main__":
    # debug=True auto-reloads on code changes - handy while learning,
    # turn this OFF in production.
    app.run(port=5001, debug=True)
