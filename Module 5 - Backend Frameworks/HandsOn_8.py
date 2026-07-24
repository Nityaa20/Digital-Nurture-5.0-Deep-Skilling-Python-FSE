"""
====================================================================
 Digital Nurture 5.0 - Python Backend Frameworks
 HANDS-ON 8 [Advanced]
 RESTful API Design Best Practices
====================================================================

WHO THIS IS FOR:
Written for a beginner / fresher. Every concept is explained in a
comment right above where it is used.

NOTE FROM THE EXERCISE BOOK:
"This hands-on applies to your Django, Flask, or FastAPI
implementation. Pick one and refactor it to meet all the criteria
below." This file continues with FastAPI (same framework as
Hands-On 6 & 7) so the whole Course Management API stays
consistent across your submission.

WHAT THIS FILE DEMONSTRATES:
   Task 1:
     - Correct REST resource naming (plural nouns, no verbs)
     - PATCH endpoint added alongside PUT
     - Correct HTTP status codes (200, 201, 204, 400, 401, 404, 422)
     - Location header on POST responses
   Task 2:
     - URL versioning (/api/v1/...)
     - Offset pagination (page, page_size) with a standard envelope
     - Search/filtering with a `search=` query parameter
     - Standardised error response format

HOW TO RUN:
    pip install fastapi uvicorn pydantic
    uvicorn HandsOn_8:app --reload
    Open http://127.0.0.1:8000/docs
====================================================================
"""

from fastapi import FastAPI, HTTPException, status, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List


# --------------------------------------------------------------
# STEP 1: Create the FastAPI app
# --------------------------------------------------------------
app = FastAPI(
    title="Course Management API",
    description="Hands-On 8: refactored to follow REST best "
                 "practices - versioned URLs, pagination, "
                 "search, and standardised errors.",
    version="1.0.0",
)


# --------------------------------------------------------------
# STEP 2: Pydantic Schemas
# --------------------------------------------------------------

class CourseCreate(BaseModel):
    """Fields required to CREATE a course (all required - used by POST and PUT)."""
    name: str
    code: str
    credits: int
    department_id: int


class CoursePatch(BaseModel):
    """
    Fields allowed on a PARTIAL update (PATCH).
    Everything is Optional - the client only sends what they want
    to change. This is different from PUT, which replaces the
    WHOLE resource and therefore requires every field.
    """
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int


class PaginatedCourses(BaseModel):
    """
    This is the standard DRF-style pagination envelope mentioned in
    the exercise book:
        {count, next, previous, results}
    Wrapping the list this way lets the client know the TOTAL number
    of items (count) and whether there are more pages (next/previous)
    without having to guess.
    """
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[CourseResponse]


# --------------------------------------------------------------
# STEP 3: Fake "Database" (a Python list, same idea as Hands-On 7)
# --------------------------------------------------------------
courses_db: List[dict] = [
    {"id": 1, "name": "Intro to Python", "code": "CS101", "credits": 4, "department_id": 1},
    {"id": 2, "name": "Data Structures", "code": "CS102", "credits": 4, "department_id": 1},
    {"id": 3, "name": "Database Systems", "code": "CS201", "credits": 3, "department_id": 1},
    {"id": 4, "name": "Financial Accounting", "code": "COM101", "credits": 3, "department_id": 2},
    {"id": 5, "name": "Marketing Basics", "code": "COM102", "credits": 3, "department_id": 2},
]
next_course_id = 6


# ================================================================
# STANDARDISED ERROR HANDLING
# ================================================================
# WHY: Step 85 in the exercise book asks for every error response
# to follow ONE consistent shape:
#     {"error": {"code": "NOT_FOUND", "message": "...", "field": null}}
# Instead of writing this dict by hand in every single endpoint, we
# use a custom exception + a FastAPI "exception handler". Write the
# logic once, FastAPI applies it everywhere automatically.
# ----------------------------------------------------------------

class APIError(Exception):
    """A custom exception that carries a machine-readable error code."""
    def __init__(self, status_code: int, code: str, message: str, field: Optional[str] = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.field = field


@app.exception_handler(APIError)
def api_error_handler(request: Request, exc: APIError):
    """
    Whenever ANY endpoint raises `APIError`, this function catches it
    and formats the JSON response the same way, every time.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "field": exc.field,
            }
        },
    )


# ================================================================
# TASK 1: Resource Naming, HTTP Methods, Status Codes, Location Header
# ================================================================
#
# Naming conventions checked here:
#   - "/api/v1/courses/"  -> plural noun "courses", no verbs like
#     "/getCourses/" or "/createCourse/". The HTTP METHOD (GET, POST,
#     PUT, PATCH, DELETE) already tells us the action - the URL
#     should only describe the RESOURCE.
#   - No underscores/camelCase in the path itself; if we had a
#     multi-word resource we would use hyphens, e.g. "/course-materials/".
# ----------------------------------------------------------------

@app.get(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"],
    summary="Get a single course by ID",
)
def get_course(course_id: int):
    for course in courses_db:
        if course["id"] == course_id:
            return course
    # 404 Not Found, using our standardised error format
    raise APIError(
        status_code=404,
        code="NOT_FOUND",
        message=f"Course with id {course_id} does not exist",
    )


@app.post(
    "/api/v1/courses/",
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create a new course",
)
def create_course(course: CourseCreate):
    global next_course_id

    # Basic validation example -> 400 Bad Request
    # (Pydantic already handles missing/wrong-type fields with a 422
    # automatically. This shows how you add YOUR OWN business-rule
    # validation on top, e.g. credits must be positive.)
    if course.credits <= 0:
        raise APIError(
            status_code=400,
            code="INVALID_INPUT",
            message="Credits must be a positive number",
            field="credits",
        )

    new_course = {
        "id": next_course_id,
        "name": course.name,
        "code": course.code,
        "credits": course.credits,
        "department_id": course.department_id,
    }
    courses_db.append(new_course)
    next_course_id += 1

    # WHY a Location header?
    # REST convention: after creating a resource, tell the client
    # exactly where to find it (its new URL), via the "Location"
    # response header. FastAPI lets us build a custom Response so
    # we can set headers directly, instead of relying only on
    # response_model.
    resp = Response(
        content=CourseResponse(**new_course).model_dump_json(),
        status_code=status.HTTP_201_CREATED,
        media_type="application/json",
    )
    resp.headers["Location"] = f"/api/v1/courses/{new_course['id']}"
    return resp


@app.put(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"],
    summary="Fully replace a course (all fields required)",
)
def replace_course(course_id: int, course: CourseCreate):
    for existing in courses_db:
        if existing["id"] == course_id:
            existing.update(course.dict())
            return existing
    raise APIError(status_code=404, code="NOT_FOUND", message=f"Course with id {course_id} does not exist")


# ----------------------------------------------------------------
# PATCH /api/v1/courses/{id}  -> Partial update (NEW in Hands-On 8)
# ----------------------------------------------------------------
# WHY PATCH is different from PUT:
#   PUT   = replace the WHOLE resource, client must send every field.
#   PATCH = update ONLY the fields the client actually sent.
# We use `exclude_unset=True` so we only touch fields the client
# actually included in their JSON body, ignoring the rest.
# ----------------------------------------------------------------
@app.patch(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"],
    summary="Partially update a course (only send the fields to change)",
)
def partial_update_course(course_id: int, course: CoursePatch):
    for existing in courses_db:
        if existing["id"] == course_id:
            updates = course.dict(exclude_unset=True)
            existing.update(updates)
            return existing
    raise APIError(status_code=404, code="NOT_FOUND", message=f"Course with id {course_id} does not exist")


@app.delete(
    "/api/v1/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"],
    summary="Delete a course",
)
def delete_course(course_id: int):
    for existing in courses_db:
        if existing["id"] == course_id:
            courses_db.remove(existing)
            return
    raise APIError(status_code=404, code="NOT_FOUND", message=f"Course with id {course_id} does not exist")


# ================================================================
# TASK 2: Versioning, Pagination, Filtering, Standardised Errors
# ================================================================

# ----------------------------------------------------------------
# GET /api/v1/courses/  -> List courses with PAGINATION + SEARCH
# ----------------------------------------------------------------
# Query parameters explained:
#   page       -> which "page" of results the client wants (1-based)
#   page_size  -> how many results per page
#   search     -> optional text to filter by course name or code
#
# WHY pagination matters:
#   If we had 10,000 courses, returning ALL of them in one response
#   would be slow and wasteful. Pagination lets the client ask for
#   a manageable "slice" at a time.
# ----------------------------------------------------------------
@app.get(
    "/api/v1/courses/",
    response_model=PaginatedCourses,
    tags=["Courses"],
    summary="List courses (supports pagination and search)",
)
def list_courses(page: int = 1, page_size: int = 10, search: Optional[str] = None):
    # Basic validation of pagination params -> 400 Bad Request
    if page < 1 or page_size < 1:
        raise APIError(
            status_code=400,
            code="INVALID_PAGINATION",
            message="page and page_size must both be 1 or greater",
        )

    # --- Filtering (search) ---
    # A case-insensitive "LIKE" style search on name OR code, done
    # here in plain Python since we're using a list instead of a
    # real database. With a real DB you'd use something like:
    #   WHERE name ILIKE '%search%' OR code ILIKE '%search%'
    filtered = courses_db
    if search:
        term = search.lower()
        filtered = [
            c for c in courses_db
            if term in c["name"].lower() or term in c["code"].lower()
        ]

    total_count = len(filtered)

    # --- Pagination math ---
    start = (page - 1) * page_size
    end = start + page_size
    page_items = filtered[start:end]

    # Build next/previous URLs (or None if there is no such page)
    base_url = "/api/v1/courses/"
    has_next = end < total_count
    has_previous = start > 0

    next_url = f"{base_url}?page={page + 1}&page_size={page_size}" if has_next else None
    previous_url = f"{base_url}?page={page - 1}&page_size={page_size}" if has_previous else None
    if search:
        if next_url:
            next_url += f"&search={search}"
        if previous_url:
            previous_url += f"&search={search}"

    return {
        "count": total_count,
        "next": next_url,
        "previous": previous_url,
        "results": page_items,
    }


# ----------------------------------------------------------------
# A quick note on VERSIONING STRATEGIES (Step 82 of the exercise):
#
# 1) URL versioning (what we used here: /api/v1/courses/)
#      + Simple, visible, easy to test directly in a browser.
#      - Every future version means duplicating URL paths (/v2/...).
#
# 2) Header-based versioning
#      e.g. a client sends:
#         Accept: application/vnd.api+json;version=1
#      + Keeps URLs clean (no /v1/, /v2/ clutter).
#      - Harder to test manually (you can't just click a link in a
#        browser - you need a tool that can set custom headers).
#
# Most beginner-friendly APIs use URL versioning because it's the
# easiest to understand and debug.
# ----------------------------------------------------------------


@app.get("/", tags=["Health Check"], summary="Check if the API is running")
def root():
    return {"message": "Course Management API v1 is running"}


"""
====================================================================
HOW TO TEST EVERYTHING (using /docs):

1. Run:
       uvicorn HandsOn_8:app --reload
   Open http://127.0.0.1:8000/docs

2. Naming & methods:
   a. GET    /api/v1/courses/1        -> fetch a single course
   b. POST   /api/v1/courses/         -> create one; check the
                                          response headers for
                                          "Location: /api/v1/courses/6"
   c. PUT    /api/v1/courses/1        -> replace ALL fields
   d. PATCH  /api/v1/courses/1        -> send just {"credits": 5}
                                          and see only that field
                                          change
   e. DELETE /api/v1/courses/1        -> 204, no response body

3. Pagination & search:
   f. GET /api/v1/courses/?page=1&page_size=2
        -> returns count, next, previous, results (first 2 courses)
   g. GET /api/v1/courses/?page=2&page_size=2
        -> returns the NEXT 2 courses, "previous" is now filled in
   h. GET /api/v1/courses/?search=CS
        -> returns only courses whose name/code contains "CS"

4. Standardised errors:
   i. GET /api/v1/courses/999
        -> {"error": {"code": "NOT_FOUND", "message": "...", "field": null}}
   j. POST /api/v1/courses/ with credits = -1
        -> {"error": {"code": "INVALID_INPUT", "message": "...", "field": "credits"}}

   Notice EVERY error, no matter which endpoint raised it, has the
   exact same {"error": {...}} shape - that's the whole point of
   Task 2, Step 85.
====================================================================
"""
