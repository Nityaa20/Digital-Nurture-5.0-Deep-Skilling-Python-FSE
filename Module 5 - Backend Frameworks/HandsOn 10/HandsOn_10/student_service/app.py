"""
====================================================================
 Digital Nurture 5.0 - Python Backend Frameworks
 HANDS-ON 10 [Advanced] - Microservices Architecture
 SERVICE: Student Service  (runs on port 5002)
====================================================================

WHO THIS IS FOR:
Written for a beginner / fresher. Every microservices concept is
explained in a comment right above where it applies.

WHAT THIS SERVICE OWNS:
   - Students and Enrollments
   - Its OWN in-memory "database" (separate from Course Service's).

WHY DOES THIS SERVICE NEED TO TALK TO COURSE SERVICE?
   Enrolling a student requires knowing the course actually exists.
   But this service does NOT own course data - Course Service does.
   So instead of peeking into Course Service's database (NOT
   allowed in microservices!), this service makes an HTTP request
   to Course Service's API, exactly like any other client would.

   This is called "synchronous inter-service communication" -
   Student Service is BLOCKED, waiting for Course Service's answer,
   before it can continue.

HOW TO RUN:
    pip install flask requests
    (Make sure course_service/app.py is ALSO running on port 5001
     first, otherwise the /enroll endpoint below will demonstrate
     the 503 Service Unavailable behaviour instead!)
    python app.py
    (runs on http://127.0.0.1:5002)
====================================================================
"""

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# --------------------------------------------------------------
# Student Service's OWN data - separate from Course Service.
# --------------------------------------------------------------
students_db = [
    {"id": 1, "first_name": "Asha", "last_name": "Rao", "email": "asha@college.edu"},
    {"id": 2, "first_name": "Rohan", "last_name": "Singh", "email": "rohan@college.edu"},
]
enrollments_db = []
next_student_id = 3
next_enrollment_id = 1

# The address of Course Service. In a real production system, this
# URL would come from a "service discovery" system (like Consul, or
# Kubernetes DNS) instead of being hard-coded - see the note at the
# bottom of this file.
COURSE_SERVICE_URL = "http://127.0.0.1:5001"


@app.route("/api/students/", methods=["GET"])
def list_students():
    return jsonify(students_db), 200


@app.route("/api/students/", methods=["POST"])
def create_student():
    global next_student_id
    data = request.get_json()
    if not data or not all(k in data for k in ("first_name", "last_name", "email")):
        return jsonify({"error": "Missing required fields"}), 400

    new_student = {
        "id": next_student_id,
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "email": data["email"],
    }
    students_db.append(new_student)
    next_student_id += 1
    return jsonify(new_student), 201


@app.route("/api/students/<int:student_id>/enroll", methods=["POST"])
def enroll_student(student_id):
    """
    Enroll a student in a course.

    STEP-BY-STEP what happens here:
      1. Check the student exists (we own this data, easy check).
      2. Call Course Service over HTTP to check the course exists.
         We do NOT trust the client to tell us a course is valid -
         we verify it ourselves by asking the service that owns it.
      3. If Course Service says the course doesn't exist -> 404.
      4. If Course Service is completely unreachable (down, network
         issue, etc.) -> catch that and return 503 Service
         Unavailable, so the CLIENT gets a clear, honest answer
         instead of our server crashing with a confusing 500 error.
      5. If everything checks out, save the enrollment.
    """
    global next_enrollment_id

    # Step 1: does the student exist? (local data, no network call needed)
    student = next((s for s in students_db if s["id"] == student_id), None)
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()
    if not data or "course_id" not in data:
        return jsonify({"error": "course_id is required"}), 400
    course_id = data["course_id"]

    # Step 2 & 4: call Course Service, and handle it being unreachable.
    try:
        # timeout=3 -> don't wait forever if Course Service is hanging;
        # fail fast instead.
        response = requests.get(
            f"{COURSE_SERVICE_URL}/api/courses/{course_id}/",
            timeout=3,
        )
    except requests.exceptions.ConnectionError:
        # This is the key line for Step 101 of the exercise:
        # Course Service is down / unreachable -> tell the client
        # honestly with a 503, rather than pretending everything is fine.
        return jsonify({
            "error": "Course Service is currently unavailable. "
                     "Please try enrolling again in a few moments."
        }), 503

    # Step 3: Course Service reached us, but said "no such course"
    if response.status_code == 404:
        return jsonify({"error": f"Course with id {course_id} does not exist"}), 404

    # At this point we know the course is real - go ahead and enroll.
    new_enrollment = {
        "id": next_enrollment_id,
        "student_id": student_id,
        "course_id": course_id,
    }
    enrollments_db.append(new_enrollment)
    next_enrollment_id += 1

    return jsonify(new_enrollment), 201


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"service": "student_service", "status": "running", "port": 5002}), 200


if __name__ == "__main__":
    app.run(port=5002, debug=True)


"""
====================================================================
NOTE ON SERVICE DISCOVERY (mentioned in the topics list):

Here we hard-coded COURSE_SERVICE_URL = "http://127.0.0.1:5001".
That's fine for learning, on your own laptop. But in a real
deployment with many servers, services get restarted, IP addresses
change, and new copies of a service get added/removed as traffic
changes (this is called "scaling"). Hard-coding an address would
break constantly.

"Service Discovery" solves this: instead of hard-coding an address,
a service asks a discovery tool (like Consul, etcd, or Kubernetes'
built-in DNS) "where is Course Service right now?" and gets back a
current, valid address. You don't need to implement this for the
exercise - just understand WHY it exists.
====================================================================
"""
