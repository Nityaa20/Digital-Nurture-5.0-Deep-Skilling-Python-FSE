# Course Management Microservices

## Service Decomposition

| Service Name | Responsibility | Endpoints it owns | Database it owns |
| --- | --- | --- | --- |
| Course Service | Department and course CRUD | `/api/courses/`, `/api/departments/` | `course_service.db` |
| Student Service | Student CRUD and enrollment | `/api/students/`, `/api/students/{id}/enroll` | `student_service.db` |
| Auth Service | Registration, login, token validation | `/api/auth/register/`, `/api/auth/login/` | `auth_service.db` |
| Notification Service | Email confirmations | Internal only | `notification_service.db` |

## Running the Services

```bash
cd course_service && python app.py    # port 5001
cd student_service && python app.py   # port 5002
cd gateway && python app.py           # port 5000
```

## Inter-Service Communication Trade-offs

**Synchronous (HTTP):** Simple to implement and debug. Creates tight coupling — if Course Service is down, enrollment fails immediately. Suitable for request/response flows that need an immediate answer.

**Asynchronous (message queue — RabbitMQ, Kafka):** Decouples services; producers and consumers operate independently. Enables eventual consistency and better resilience under load. Adds operational complexity (brokers, dead-letter queues, idempotency). Use when operations can be deferred (notifications, analytics, audit logs) or when peak load requires buffering.

## API Gateway

The gateway on port 5000 routes `/api/courses/*` to Course Service and `/api/students/*` to Student Service. A production gateway also handles authentication, rate limiting, and SSL termination.
