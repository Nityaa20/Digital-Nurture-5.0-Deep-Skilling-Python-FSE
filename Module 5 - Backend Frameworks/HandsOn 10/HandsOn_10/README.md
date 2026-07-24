# Hands-On 10 — Microservices Architecture

Beginner-friendly writeup covering both tasks in the exercise book.

## Task 1: Service Decomposition (Steps 96–99)

We reviewed the monolithic Course Management API from Hands-On 1–9
and split it into independent services. Each row below is a
"bounded context" — a self-contained chunk of functionality with
its own data:

| Service Name         | Responsibility                              | Endpoints it owns                                                  | Database it owns          |
|-----------------------|----------------------------------------------|----------------------------------------------------------------------|-----------------------------|
| **Course Service**    | Departments & Courses (create, read, etc.)   | `/api/courses/`, `/api/courses/{id}/`                                | Its own courses DB (list/SQLite) |
| **Student Service**   | Students & Enrollments                       | `/api/students/`, `/api/students/{id}/enroll`                       | Its own students/enrollments DB |
| **Auth Service** *(not built in this exercise, described for completeness)* | User registration, login, token validation | `/api/auth/register/`, `/api/auth/login/` | Its own users DB |
| **Notification Service** *(not built, described for completeness)* | Sending emails/SMS confirmations | (internal, triggered by events) | None (stateless) |

For this hands-on we actually **built two services** (as the exercise
asks — "start with 2 services, do not over-engineer"):

- `course_service/` — runs on **port 5001**
- `student_service/` — runs on **port 5002**
- `gateway/` — runs on **port 5000** (routes requests to the two above)

**The core microservices rule demonstrated here:** each service owns
its data. `student_service` never reaches directly into
`course_service`'s in-memory list — it only ever talks to it over
HTTP, exactly like an outside client would.

## Task 2: Inter-Service Communication & API Gateway (Steps 100–104)

### How enrollment works across services
1. Client calls `POST /api/students/1/enroll` (through the Gateway).
2. Student Service checks the student exists locally (its own data).
3. Student Service then calls `GET /api/courses/{id}/` on Course
   Service over plain HTTP, using the `requests` library, to confirm
   the course is real.
4. If Course Service says "not found" → Student Service returns 404.
5. If Course Service is **unreachable** (down, crashed, network
   issue) → Student Service catches the `ConnectionError` and
   returns **503 Service Unavailable** with a clear message, instead
   of crashing or hanging.
6. If everything checks out, the enrollment is saved.

This was tested directly: with `course_service` stopped, calling the
enroll endpoint returns exactly:
```
HTTP 503
{"error": "Course Service is currently unavailable. Please try enrolling again in a few moments."}
```

### API Gateway
A single Flask app (`gateway/app.py`) listens on port 5000 and
forwards ("proxies") every request to the right backend service
based on the URL prefix:
- `/api/courses/*`  → Course Service (`http://127.0.0.1:5001`)
- `/api/students/*` → Student Service (`http://127.0.0.1:5002`)

This means a client (e.g. a frontend app) only ever needs to know
**one address** — the Gateway — instead of tracking where every
individual service lives.

### Synchronous (HTTP) vs Asynchronous (message queue) communication

**Synchronous (what we built — plain HTTP requests):**
- Simple to understand and debug — it's just a normal HTTP call.
- **Downside:** tight coupling. If Course Service is slow or down,
  the enrollment request fails or hangs, right there, immediately.
  The caller is *blocked* waiting for an answer.

**Asynchronous (message queue — e.g. RabbitMQ, Kafka):**
- Student Service would publish an "EnrollmentRequested" event to a
  queue and move on immediately, without waiting.
- Course Service (or a worker) picks up the event whenever it's
  ready, validates it, and publishes back a result event.
- **Upside:** services are decoupled — one being temporarily down
  doesn't immediately break the other; messages just queue up and
  get processed once it's back.
- **Downside:** "eventual consistency" — there's a delay before the
  enrollment is confirmed, and the system is more complex to build,
  monitor, and debug (you now have a message broker to run too).

**When to choose which:**
- Use **synchronous HTTP** when the caller genuinely needs an
  immediate answer to continue (e.g. "does this course exist, right
  now, so I can show the enroll button?").
- Use a **message queue** for things that can happen "eventually"
  and shouldn't block the user — e.g. sending a confirmation email,
  updating analytics, generating a report.

## How to run everything yourself

Open 3 terminals:

```bash
# Terminal 1
cd course_service
pip install flask
python app.py          # http://127.0.0.1:5001

# Terminal 2
cd student_service
pip install flask requests
python app.py          # http://127.0.0.1:5002

# Terminal 3
cd gateway
pip install flask requests
python app.py          # http://127.0.0.1:5000
```

Then test through the Gateway:

```bash
curl http://127.0.0.1:5000/api/courses/
curl http://127.0.0.1:5000/api/students/

curl -X POST http://127.0.0.1:5000/api/students/1/enroll \
     -H "Content-Type: application/json" \
     -d '{"course_id": 1}'
```

Now stop `course_service` (Ctrl+C in Terminal 1) and try enrolling
again — you'll see the 503 response described above.
