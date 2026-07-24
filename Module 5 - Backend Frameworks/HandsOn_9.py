"""
====================================================================
 Digital Nurture 5.0 - Python Backend Frameworks
 HANDS-ON 9 [Advanced]
 Authentication & Security - JWT, OAuth2 & OWASP
====================================================================

WHO THIS IS FOR:
Written for a beginner / fresher. Every security concept is
explained in a comment right above the line where it is used.

WHAT THIS FILE DEMONSTRATES:
   Task 1:
     - A User "model" (id, email, hashed_password, is_active)
     - Password hashing with bcrypt (never store plain-text passwords)
     - POST /api/v1/auth/register/ with duplicate-email check (409)
   Task 2:
     - POST /api/v1/auth/login/ that returns a JWT access token
     - A get_current_user() dependency that protects routes
     - Protecting POST/DELETE on courses with Depends()
     - CORS configuration for a frontend on localhost:3000
     - Notes on the OAuth2 Authorization Code flow vs simple JWT login

HOW TO RUN:
    pip install fastapi uvicorn "pydantic[email]" "python-jose[cryptography]" bcrypt python-multipart
    uvicorn HandsOn_9:app --reload
    Open http://127.0.0.1:8000/docs
====================================================================
"""

from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import bcrypt
from jose import jwt, JWTError


# --------------------------------------------------------------
# STEP 1: Create the FastAPI app
# --------------------------------------------------------------
app = FastAPI(
    title="Course Management API",
    description="Hands-On 9: adds JWT authentication, password "
                 "hashing, CORS, and protected routes.",
    version="1.0.0",
)


# --------------------------------------------------------------
# STEP 2: CORS configuration (Step 94)
# --------------------------------------------------------------
# WHAT IS CORS?
#   By default, browsers BLOCK a webpage running on one origin
#   (e.g. http://localhost:3000, your React frontend) from calling
#   an API running on a different origin (e.g. http://localhost:8000).
#   CORSMiddleware tells the browser "it's OK, these origins are
#   allowed to call me".
# IMPORTANT: CORS is enforced by the BROWSER, not the server. A
# non-browser client (like Postman, curl, or another backend
# service) completely ignores CORS headers - CORS does NOT protect
# your API from server-to-server requests or scripts.
# --------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # our frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------------------
# STEP 3: Standardised error handling (carried over from Hands-On 8)
# --------------------------------------------------------------
class APIError(Exception):
    def __init__(self, status_code: int, code: str, message: str, field: Optional[str] = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.field = field


@app.exception_handler(APIError)
def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message, "field": exc.field}},
    )


# ================================================================
# TASK 1: Password Hashing and User Registration
# ================================================================

# ----------------------------------------------------------------
# security.py logic (kept in this same file for simplicity)
# ----------------------------------------------------------------
# We use the `bcrypt` library directly to hash and verify passwords.
#
# WHY bcrypt and NOT md5/sha256 for passwords?
#   md5/sha256 are designed to be FAST - great for checking file
#   integrity, terrible for passwords, because an attacker with a
#   stolen password database can try billions of guesses per second.
#   bcrypt is DELIBERATELY SLOW (it has a configurable "work factor")
#   which makes brute-forcing millions of passwords impractical.
#   bcrypt also automatically adds a random "salt" to every password,
#   so two users with the same password get two different hashes.
# ----------------------------------------------------------------

def get_password_hash(password: str) -> str:
    """Turn a plain-text password into a secure bcrypt hash."""
    # bcrypt.gensalt() creates a random salt; bcrypt.hashpw() combines
    # the salt + password + work factor into the final hash.
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_bytes.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plain-text password against a stored bcrypt hash."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


# ----------------------------------------------------------------
# User "model" - again a simple Python list instead of a real DB,
# to keep the focus on FastAPI + security concepts.
# ----------------------------------------------------------------
users_db: List[dict] = []
next_user_id = 1


class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    """
    What we SEND BACK after registration.
    Notice: NO password field here at all, hashed or otherwise.
    Never return password data in an API response.
    """
    id: int
    email: str
    is_active: bool


@app.post(
    "/api/v1/auth/register/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Auth"],
    summary="Register a new user",
)
def register(user: UserRegister):
    global next_user_id

    # Check the email is not already registered -> 409 Conflict
    # (A UNIQUE constraint in a real DB would also prevent this, but
    # checking here first lets us return a friendly, specific error.)
    for existing in users_db:
        if existing["email"] == user.email:
            raise APIError(
                status_code=409,
                code="EMAIL_ALREADY_REGISTERED",
                message="An account with this email already exists",
                field="email",
            )

    # Hash the password BEFORE storing it. We NEVER store or log the
    # plain-text password, not even temporarily.
    hashed = get_password_hash(user.password)

    new_user = {
        "id": next_user_id,
        "email": user.email,
        "hashed_password": hashed,
        "is_active": True,
    }
    users_db.append(new_user)
    next_user_id += 1

    return new_user


# ================================================================
# TASK 2: JWT Login, Protected Routes and CORS
# ================================================================

# ----------------------------------------------------------------
# JWT settings
# ----------------------------------------------------------------
# WARNING (for real projects): never hard-code a secret key like
# this in source code. Load it from an environment variable, e.g.
#   import os
#   SECRET_KEY = os.environ["JWT_SECRET_KEY"]
# It is left as a plain string here ONLY to keep this exercise easy
# to run without extra setup.
# ----------------------------------------------------------------
SECRET_KEY = "dev-only-secret-change-me"   # DO NOT use in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    """
    Build a JWT (JSON Web Token).
    A JWT has 3 parts: header.payload.signature
      - header    -> which algorithm was used (HS256 here)
      - payload   -> the actual data (e.g. {"sub": "user@email.com"})
      - signature -> proves the token was created by US, and was not
                     tampered with, using our SECRET_KEY

    IMPORTANT: the payload is only BASE64-ENCODED, not encrypted.
    Anyone can decode a JWT and read its contents (try jwt.io).
    NEVER put passwords, credit card numbers, or other sensitive
    data inside a JWT payload.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ----------------------------------------------------------------
# OAuth2PasswordBearer tells FastAPI: "expect clients to send a
# Bearer token in the Authorization header, and here's the URL
# where they can go get one". This also makes the Swagger UI show
# a padlock icon and an "Authorize" button automatically.
# ----------------------------------------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


class Token(BaseModel):
    access_token: str
    token_type: str


@app.post(
    "/api/v1/auth/login/",
    response_model=Token,
    tags=["Auth"],
    summary="Login and receive a JWT access token",
)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2PasswordRequestForm expects the client to send
    `username` and `password` as regular form fields (not JSON).
    We treat the `username` field as the user's email here.
    """
    user = None
    for existing in users_db:
        if existing["email"] == form_data.username:
            user = existing
            break

    # Same error for "user not found" AND "wrong password" -
    # this is intentional! Telling an attacker "that email doesn't
    # exist" vs "wrong password" leaks information about which
    # emails are registered. Always give one generic message.
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise APIError(
            status_code=401,
            code="INVALID_CREDENTIALS",
            message="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}


# ----------------------------------------------------------------
# get_current_user() - a FastAPI Dependency
# ----------------------------------------------------------------
# WHY a dependency?
#   Any endpoint that needs "who is calling me right now?" can just
#   add `current_user: dict = Depends(get_current_user)` as a
#   parameter. FastAPI automatically:
#     1. Extracts the token from the Authorization header
#     2. Runs this function
#     3. Passes the returned user into your endpoint
#   Write the logic ONCE, reuse it on every protected route.
# ----------------------------------------------------------------
def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise APIError(status_code=401, code="INVALID_TOKEN", message="Invalid authentication token")
    except JWTError:
        # Covers: expired token, tampered signature, malformed token
        raise APIError(status_code=401, code="INVALID_TOKEN", message="Invalid or expired authentication token")

    for user in users_db:
        if user["email"] == email:
            return user

    raise APIError(status_code=401, code="INVALID_TOKEN", message="User for this token no longer exists")


# ================================================================
# Courses - some endpoints protected, some public
# (Carried over from Hands-On 7 & 8, trimmed down to show the auth
# pattern clearly.)
# ================================================================

class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int


class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int


courses_db: List[dict] = [
    {"id": 1, "name": "Intro to Python", "code": "CS101", "credits": 4, "department_id": 1},
]
next_course_id = 2


@app.get(
    "/api/v1/courses/",
    response_model=List[CourseResponse],
    tags=["Courses"],
    summary="List all courses (public - no login required)",
)
def list_courses():
    # Reading course data is not sensitive, so this stays PUBLIC -
    # no Depends(get_current_user) here.
    return courses_db


@app.post(
    "/api/v1/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create a course (requires login)",
)
def create_course(course: CourseCreate, current_user: dict = Depends(get_current_user)):
    # Because `current_user` is a dependency, FastAPI will reject
    # this request with 401 Unauthorized BEFORE this function body
    # even runs, if the token is missing/invalid/expired.
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


@app.delete(
    "/api/v1/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"],
    summary="Delete a course (requires login)",
)
def delete_course(course_id: int, current_user: dict = Depends(get_current_user)):
    for existing in courses_db:
        if existing["id"] == course_id:
            courses_db.remove(existing)
            return
    raise APIError(status_code=404, code="NOT_FOUND", message=f"Course with id {course_id} does not exist")


@app.get("/", tags=["Health Check"], summary="Check if the API is running")
def root():
    return {"message": "Course Management API v1 is running"}


"""
====================================================================
NOTES: OAuth2 Authorization Code Flow vs. our simple JWT login
        (Step 95)

Our login endpoint above is a "password flow" - the client sends
email + password directly to our API, and we hand back a JWT. This
is simple, but it means the frontend app has to directly handle the
user's raw password. It's fine for a first-party app you fully
control (your own React frontend calling your own API).

The OAuth2 AUTHORIZATION CODE flow is different and is what you use
when logging in "with Google" or "with GitHub" on other websites:
  1. Your app redirects the user to the provider's login page
     (e.g. accounts.google.com) - the user types their password
     THERE, never into your app.
  2. After login, the provider redirects back to your app with a
     short-lived "authorization code" in the URL.
  3. Your BACKEND exchanges that code (plus a secret known only to
     your backend) for an access token, by calling the provider's
     token endpoint directly (server-to-server).
  4. Your backend uses that access token to fetch the user's profile
     info.

Key difference: with the Authorization Code flow, your app NEVER
sees the user's password - a third party (Google, GitHub, etc.)
handles authentication entirely. This is essential when you want
users to log in with an account you don't own/manage.
====================================================================

HOW TO TEST EVERYTHING (using /docs):

1. Install and run:
     pip install fastapi uvicorn "pydantic[email]" "python-jose[cryptography]" bcrypt python-multipart
     uvicorn HandsOn_9:app --reload
   Open http://127.0.0.1:8000/docs

2. Register a user:
   POST /api/v1/auth/register/
   {
     "email": "student@college.edu",
     "password": "MyPassword123"
   }
   -> 201, and the response has NO password field.
   -> Try registering the SAME email again -> 409 Conflict.

3. Login:
   POST /api/v1/auth/login/  (this one uses a FORM, not JSON, in
   the Swagger UI - just fill in username=student@college.edu and
   password=MyPassword123)
   -> Returns {"access_token": "...", "token_type": "bearer"}

4. Authorize in Swagger:
   Click the green "Authorize" button at the top of /docs, paste
   your access_token, click Authorize.

5. Test protected routes:
   GET    /api/v1/courses/       -> works with NO token (public)
   POST   /api/v1/courses/       -> WITHOUT being authorized: 401
                                     WITH the token: 201, course created
   DELETE /api/v1/courses/{id}   -> same as above, needs a valid token
====================================================================
"""
