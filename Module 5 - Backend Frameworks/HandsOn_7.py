"""
====================================================================
 Digital Nurture 5.0 - Python Backend Frameworks
 HANDS-ON 7 [Intermediate]
 FastAPI - Dependency Injection, CRUD & OpenAPI Documentation
====================================================================

WHO THIS IS FOR:
This file is written for a beginner / fresher who only knows basic
Python. Every FastAPI concept used here is explained in a comment
right above the line where it is used. Nothing fancy - no external
database, no async SQLAlchemy - we use a simple Python list as our
"database" so you can focus 100% on learning FastAPI concepts:

    - Dependency Injection (Depends)
    - Full CRUD (Create, Read, Update, Delete)
    - response_model and proper HTTP status codes
    - HTTPException for errors
    - Background Tasks
    - OpenAPI customisation (title, tags, summary, description)

HOW TO RUN THIS FILE:
    1. Install requirements:
         pip install fastapi uvicorn pydantic
    2. Run the server:
         uvicorn HandsOn_7:app --reload
    3. Open your browser at:
         http://127.0.0.1:8000/docs
       This is the auto-generated Swagger UI - you can test every
       endpoint directly from the browser, no Postman needed.

====================================================================
"""

from fastapi import FastAPI, HTTPException, status, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List


# --------------------------------------------------------------
# STEP 1: Create the FastAPI app
# --------------------------------------------------------------
# We pass in "metadata" (title, description, version, contact) so
# that the auto-generated documentation at /docs looks professional.
# This is the "OpenAPI Customisation" part of the topics list.
# --------------------------------------------------------------
app = FastAPI(
    title="Course Management API",
    description="A simple API to manage Departments, Courses, "
                 "Students and Enrollments - built for Hands-On 7 "
                 "of the Digital Nurture 5.0 program.",
    version="1.0.0",
    contact={
        "name": "Digital Nurture 5.0 Participant",
        "email": "student@college.edu",
    },
)


# --------------------------------------------------------------
# STEP 2: Define Pydantic Schemas (these are just "shapes" of data)
# --------------------------------------------------------------
# Pydantic models tell FastAPI exactly what fields a request should
# contain, and what fields a response will contain. FastAPI uses
# these to auto-validate data AND to auto-generate the Swagger docs.
# --------------------------------------------------------------

class CourseCreate(BaseModel):
    """Fields required when a client wants to CREATE a new course."""
    name: str
    code: str
    credits: int
    department_id: int


class CourseUpdate(BaseModel):
    """
    Fields allowed when UPDATING a course.
    Everything is Optional because PATCH allows partial updates -
    the client only sends the fields they want to change.
    """
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


class CourseResponse(BaseModel):
    """
    This is what we SEND BACK to the client.
    Notice it has an 'id' field - the client never sends this,
    the server creates and assigns the id.
    """
    id: int
    name: str
    code: str
    credits: int
    department_id: int


class EnrollmentCreate(BaseModel):
    """Fields required to enroll a student in a course."""
    student_id: int
    course_id: int
    student_email: str  # used to "send" a confirmation email


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int


# --------------------------------------------------------------
# STEP 3: Fake "Database" (a simple Python list)
# --------------------------------------------------------------
# In a real project this would be a proper database (see Hands-On
# 6, where we used async SQLAlchemy). For this hands-on, a plain
# list keeps things simple so we can focus on FastAPI itself.
# --------------------------------------------------------------
courses_db: List[dict] = [
    {"id": 1, "name": "Intro to Python", "code": "CS101", "credits": 4, "department_id": 1},
    {"id": 2, "name": "Data Structures", "code": "CS102", "credits": 4, "department_id": 1},
]
enrollments_db: List[dict] = []
next_course_id = 3
next_enrollment_id = 1


# ================================================================
# TASK 1: Complete CRUD with Proper HTTP Conventions
# ================================================================

# ----------------------------------------------------------------
# GET /api/courses/{id}  -> Read a single course
# ----------------------------------------------------------------
# WHY response_model=CourseResponse?
#   It tells FastAPI (and the Swagger docs) exactly what shape the
#   response will have. If our internal data ever had extra fields,
#   response_model would filter them out automatically.
# WHY tags=["Courses"]?
#   Tags group related endpoints together in the Swagger UI, so
#   /docs looks organised instead of one long flat list.
# ----------------------------------------------------------------
@app.get(
    "/api/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"],
    summary="Get a single course by ID",
)
def get_course(course_id: int):
    for course in courses_db:
        if course["id"] == course_id:
            return course
    # HTTPException is FastAPI's way of returning a proper error
    # response with a status code AND a JSON error message.
    raise HTTPException(status_code=404, detail="Course not found")


# ----------------------------------------------------------------
# GET /api/courses/  -> List all courses
# ----------------------------------------------------------------
@app.get(
    "/api/courses/",
    response_model=List[CourseResponse],
    tags=["Courses"],
    summary="List all courses",
)
def list_courses():
    return courses_db


# ----------------------------------------------------------------
# POST /api/courses/  -> Create a new course
# ----------------------------------------------------------------
# status_code=status.HTTP_201_CREATED
#   REST convention: a successful POST that creates something
#   should return 201 Created, not the default 200 OK.
# ----------------------------------------------------------------
@app.post(
    "/api/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create a new course",
    response_description="The course that was created",
)
def create_course(course: CourseCreate):
    global next_course_id
    new_course = {
        "id": next_course_id,
        "name": course.name,
        "code": course.code,
        "credits": course.credits,
        "department_id": course.department_id,
    }
    courses_db.append(new_course)
    next_course_id += 1
    return new_course


# ----------------------------------------------------------------
# PUT /api/courses/{id}  -> Full update (replace all fields)
# ----------------------------------------------------------------
@app.put(
    "/api/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"],
    summary="Fully update a course (all fields required)",
)
def update_course(course_id: int, course: CourseCreate):
    for existing in courses_db:
        if existing["id"] == course_id:
            existing.update(course.dict())
            return existing
    raise HTTPException(status_code=404, detail="Course not found")


# ----------------------------------------------------------------
# DELETE /api/courses/{id}  -> Delete a course
# ----------------------------------------------------------------
# status_code=status.HTTP_204_NO_CONTENT
#   204 means "success, but there is nothing to send back".
#   Notice the function does not return any data - that's correct
#   for a 204 response.
# ----------------------------------------------------------------
@app.delete(
    "/api/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"],
    summary="Delete a course",
)
def delete_course(course_id: int):
    for existing in courses_db:
        if existing["id"] == course_id:
            courses_db.remove(existing)
            return
    raise HTTPException(status_code=404, detail="Course not found")


# ----------------------------------------------------------------
# GET /api/courses/{id}/students/  -> Students enrolled in a course
# ----------------------------------------------------------------
# (Simplified: since we don't have a real Student table in this
# beginner version, we just return the enrollment records that
# match this course_id. In your real project, join with the
# Student table to return full student details.)
# ----------------------------------------------------------------
@app.get(
    "/api/courses/{course_id}/students/",
    tags=["Courses"],
    summary="List students enrolled in a course",
)
def get_students_for_course(course_id: int):
    # First check the course itself exists
    course_exists = any(c["id"] == course_id for c in courses_db)
    if not course_exists:
        raise HTTPException(status_code=404, detail="Course not found")

    matching = [e for e in enrollments_db if e["course_id"] == course_id]
    return matching


# ================================================================
# TASK 2: Background Tasks and OpenAPI Customisation
# ================================================================

def send_confirmation_email(student_email: str):
    """
    This function simulates sending a confirmation email.
    In a real project this could call an email service (e.g. SMTP,
    SendGrid, etc). Here we just print to the console.

    IMPORTANT: This function runs AFTER the response has already
    been sent back to the client - the client does NOT wait for
    this to finish.
    """
    print(f"Sending confirmation email to {student_email} ...")
    print(f"Email sent to {student_email}!")


# ----------------------------------------------------------------
# POST /api/enrollments/  -> Enroll a student in a course
# ----------------------------------------------------------------
# WHY BackgroundTasks?
#   Sending an email can be slow. We don't want the client to wait
#   for the email to be "sent" before getting their response.
#   FastAPI lets us schedule that work to run AFTER the response
#   is returned, using the BackgroundTasks parameter.
# ----------------------------------------------------------------
@app.post(
    "/api/enrollments/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"],
    summary="Enroll a student in a course",
    response_description="The enrollment that was created",
)
def create_enrollment(enrollment: EnrollmentCreate, background_tasks: BackgroundTasks):
    # Check the course exists before enrolling
    course_exists = any(c["id"] == enrollment.course_id for c in courses_db)
    if not course_exists:
        raise HTTPException(status_code=404, detail="Course not found")

    global next_enrollment_id
    new_enrollment = {
        "id": next_enrollment_id,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id,
    }
    enrollments_db.append(new_enrollment)
    next_enrollment_id += 1

    # Schedule the "email" to be sent AFTER this response is returned.
    # Try it: call this endpoint, notice the response comes back
    # instantly, then check your terminal - the print statements
    # appear a moment later.
    background_tasks.add_task(send_confirmation_email, enrollment.student_email)

    return new_enrollment


# ----------------------------------------------------------------
# Root route - just to confirm the API is running
# ----------------------------------------------------------------
@app.get("/", tags=["Health Check"], summary="Check if the API is running")
def root():
    return {"message": "Course Management API is running"}


"""
====================================================================
HOW TO TEST EVERYTHING (step by step, using /docs):

1. Run the server:
       uvicorn HandsOn_7:app --reload

2. Open http://127.0.0.1:8000/docs

3. Try these in order:
   a. GET  /api/courses/           -> should show 2 sample courses
   b. POST /api/courses/           -> create a new course, note the
                                       new "id" returned, and that
                                       the status code is 201
   c. GET  /api/courses/{id}       -> fetch the course you just made
   d. PUT  /api/courses/{id}       -> update all its fields
   e. DELETE /api/courses/{id}     -> delete it, notice status 204
                                       and no response body
   f. GET  /api/courses/999        -> a non-existent id, should
                                       return 404 with a JSON error
   g. POST /api/enrollments/       -> enroll a student, then check
                                       your terminal/console window
                                       - you'll see the "email sent"
                                       messages appear AFTER the
                                       response came back

4. Notice in the Swagger UI (/docs) that endpoints are grouped
   under "Courses", "Enrollments", and "Health Check" - that's the
   'tags' parameter at work. Also notice the title, description,
   and contact info shown at the top of the page - that comes from
   the FastAPI(...) constructor at the top of this file.
====================================================================
"""
