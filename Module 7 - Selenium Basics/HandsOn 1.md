# Hands-On 1: QA Concepts, Functional Testing & Defect Lifecycle

**Context:** Course Management API

---

## Task 1: Map Testing Types to a Real System

### 1. Test Cases Across Test Levels

**Unit Testing** (test a single function in isolation)
- **Test Case:** Test the `validate_course_code()` function that checks a course code matches the pattern `CS101` style (2-4 letters + 3 digits). Call the function directly with inputs like `"CS101"` (valid), `"C1"` (invalid), `"12345"` (invalid), and assert the correct boolean/exception is returned — no database or API layer involved.

**Integration Testing** (test two components working together)
- **Test Case:** Test that the `POST /api/courses/` endpoint correctly writes a new course record to the database. Call the endpoint with a valid payload, then query the database directly to confirm the row exists with matching field values. This verifies the API layer and the database layer work correctly together.

**System Testing** (test a full end-to-end flow)
- **Test Case:** Simulate the complete flow: send `POST /api/courses/` to create a course → send `GET /api/courses/{id}` to retrieve it → send `PUT /api/courses/{id}` to update the instructor → send `GET /api/courses/{id}` again to confirm the update persisted. This tests the system as a whole, end to end, exactly as a client application would use it.

**User Acceptance Testing (UAT)** (from the perspective of an actual college admin user)
- **Test Case:** A college admin logs into the Course Management portal, creates a new course "Introduction to Data Structures" for the Fall semester using the UI, and confirms it appears correctly in the course listing page with the right department, credits, and instructor — without any knowledge of the underlying API or database.

### 2. Functional vs Non-Functional Classification

| Test Case | Classification |
|---|---|
| Unit test on `validate_course_code()` | Functional |
| Integration test on `POST /api/courses/` + DB | Functional |
| System test: full CRUD flow | Functional |
| UAT: admin creates course via UI | Functional |

**Non-Functional Example:** Performance test — verify `GET /api/courses/` responds within 500ms when the database contains 10,000 course records and the endpoint is hit by 50 concurrent users. This doesn't ask "does it work?" but "how well does it work under load?"

Other non-functional examples worth noting: **Security** (can an unauthenticated user call `DELETE /api/courses/{id}`?) and **Reliability** (does the API stay up and return consistent results over a 24-hour soak test?).

### 3. Black-Box vs White-Box Testing

- **Black-Box Testing:** Testing the software's behavior purely from the outside — inputs and expected outputs — without any knowledge of how the code is implemented internally. The tester treats the system as a sealed box: they know *what* it should do, not *how* it does it.
- **White-Box Testing:** Testing with full visibility into the internal code structure, logic branches, and data paths. The tester designs test cases to exercise specific lines, conditions, and loops in the source code.

**Who performs which:** A **QA tester** typically performs black-box testing (e.g., functional, system, UAT testing) since their role is to validate behavior against requirements, not code structure. A **developer** typically performs white-box testing (e.g., unit tests, code coverage analysis) since they need direct knowledge of the code to test internal logic paths.

### 4. Formal Test Cases — `POST /api/courses/`

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC_COURSE_001 | Create a course with all valid required fields | API server is running; admin auth token is valid | 1. Send `POST /api/courses/` with valid JSON body (`code`, `name`, `credits`, `instructor`) and valid auth header 2. Capture response | HTTP 201 Created returned; response body contains the created course with a generated `id` | | |
| TC_COURSE_002 | Attempt to create a course with a duplicate course code | A course with code "CS101" already exists in the database | 1. Send `POST /api/courses/` with `code: "CS101"` (duplicate) and other valid fields 2. Capture response | HTTP 409 Conflict (or 400) returned; response body contains an error message indicating the course code already exists | | |
| TC_COURSE_003 | Attempt to create a course with a missing required field | API server is running; admin auth token is valid | 1. Send `POST /api/courses/` with the `name` field omitted from the JSON body 2. Capture response | HTTP 400 Bad Request returned; response body indicates `name` is a required field | | |

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. Defect Lifecycle States

**Main flow:**
`New` → `Assigned` → `Open` → `Fixed` → `Retest` → `Verified` → `Closed`

- **New:** Defect is logged by QA/tester for the first time; not yet reviewed.
- **Assigned:** A lead/manager reviews the defect and assigns it to a specific developer.
- **Open:** The developer accepts the defect and begins investigating/fixing it.
- **Fixed:** The developer has implemented a code change believed to resolve the defect and moved it forward for verification.
- **Retest:** QA re-executes the original failing test steps against the fix.
- **Verified:** QA confirms the fix resolves the issue as expected.
- **Closed:** The defect is confirmed resolved and the ticket is archived.

**Alternate/branch paths:**
- **Rejected:** The developer or lead determines the reported behavior is not actually a defect (e.g., it's working as designed, a duplicate, or not reproducible). Moves from `New`/`Assigned` directly to `Rejected` instead of `Open`.
- **Deferred:** The defect is valid but the team decides not to fix it in the current release (e.g., low priority, tight deadline). It's parked and may be revisited in a future release cycle. Can occur from `Open` or `Assigned`.
- **Reopened:** If, during `Retest`, QA finds the fix did not actually resolve the issue, the defect goes back to `Open` (or `Reopened` as an explicit state) rather than proceeding to `Verified`.

### 6. Severity & Priority Classification

| Bug | Severity | Priority | Justification |
|---|---|---|---|
| (a) `POST /api/courses/` returns 500 for all requests | **Critical** | **P1** | Core functionality (creating courses) is completely broken for every user — no workaround exists. This blocks the primary use case of the API. |
| (b) Course names >150 chars are silently truncated, no error | **Medium** | **P3** | The system doesn't crash and most course names are short, so impact is limited, but silent data loss is a real correctness problem that should be fixed — just not urgently. |
| (c) Typo in the `/docs` Swagger description | **Low** | **P4** | Purely cosmetic; has zero impact on functionality. Can be fixed whenever convenient. |
| (d) Login with correct credentials occasionally returns 401 (intermittent) | **High** | **P2** (arguably P1) | Even though it doesn't fail 100% of the time, an intermittent authentication failure undermines trust in the entire login system and is hard to reproduce/debug — this instability needs urgent investigation despite not being "Critical" severity. |

### 7. Defect Report — Bug (a)

| Field | Value |
|---|---|
| **Defect ID** | DEF-2026-0142 |
| **Title** | POST /api/courses/ returns HTTP 500 Internal Server Error for all requests |
| **Environment** | Staging — Course Management API v1.3.0, Ubuntu 22.04, Python 3.11, PostgreSQL 15 |
| **Build Version** | v1.3.0-rc2 |
| **Severity** | Critical |
| **Priority** | P1 |
| **Steps to Reproduce** | 1. Authenticate as an admin user to obtain a valid bearer token. 2. Send `POST /api/courses/` with a valid JSON body containing `code`, `name`, `credits`, and `instructor`. 3. Observe the response. |
| **Expected Result** | HTTP 201 Created is returned along with the newly created course object, including a generated `id`. |
| **Actual Result** | HTTP 500 Internal Server Error is returned with no course created; server logs show an unhandled exception in the database insert layer. |
| **Attachments** | screenshot of 500 error |

### 8. Severity vs Priority

**Severity** measures the *impact* of the defect on the system's functionality — how badly it breaks things from a technical/functional standpoint. **Priority** measures the *urgency* with which the defect should be fixed — how soon it needs attention from a business standpoint.

**Real-world example where High Severity ≠ High Priority:**
A rarely-used "Export to PDF" feature on an internal admin reporting page crashes the entire application when clicked (High Severity — it's a full crash). However, this feature is used by only one internal employee once a month, and a manual workaround (exporting from the database directly) already exists. The team may classify this as **P3/Low Priority** because, despite the severe technical impact when it occurs, it affects almost no users and has a workaround — so fixing it can wait behind other work.

Conversely, a cosmetic bug where the CEO's name is misspelled on the company's public homepage is **Low Severity** (nothing is broken) but **High Priority** (P1) — it needs to be fixed immediately due to reputational/business concerns, even though it has no functional impact.
