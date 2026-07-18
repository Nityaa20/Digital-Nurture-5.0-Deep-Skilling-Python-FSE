# Hands-On 2: SDLC vs TDLC — V-Model & Agile QA Integration

**Context:** Course Management API

---

## Task 1: V-Model Mapping

### 9. V-Model Diagram (ASCII Representation)

```
   DEVELOPMENT (Left Side)              TESTING (Right Side)
   ------------------------             -----------------------
   Requirements  ─────────────────────  Acceptance Testing
         \                                      /
          \                                    /
     System Design  ───────────────────  System Testing
              \                              /
               \                            /
        Architecture Design  ────────  Integration Testing
                   \                        /
                    \                      /
              Module Design  ───────  Unit Testing
                        \                  /
                         \                /
                          \              /
                           \            /
                            \          /
                             \        /
                              \      /
                               \    /
                                \  /
                              Coding
                          (bottom vertex)
```

Each arrow represents a horizontal relationship: the development phase on the left directly defines what gets validated by the testing phase on the right, at the same "level" of the V.

### 10. SDLC Phase → TDLC Phase → Test Artifact Produced

| SDLC Phase (Left) | TDLC Phase (Right) | Test Artifact Produced During Dev Phase |
|---|---|---|
| Requirements | Acceptance Testing | Acceptance Test Plan is prepared during this phase (based on business/user requirements for the Course Management system) |
| System Design | System Testing | System Test Plan is prepared, outlining end-to-end scenarios like "create course → enroll student → generate transcript" |
| Architecture Design | Integration Testing | Integration Test Plan is prepared, identifying which components must be tested together (e.g., API layer + database, API + auth service) |
| Module Design | Unit Testing | Unit Test Cases are prepared for individual functions/modules (e.g., `validate_course_code()`, `calculate_credit_total()`) |
| Coding | — (bottom vertex; no test phase, this is where dev and QA artifacts converge) | Code is written against all the plans defined above |

### 11. Entry & Exit Criteria for Each TDLC Phase

**Unit Testing**
- **Entry Criteria:** Code for the module/function is complete and compiles/runs without syntax errors; unit test cases have been designed based on the Module Design document.
- **Exit Criteria:** All planned unit test cases have been executed; code coverage meets the agreed threshold (e.g., 80%); no open critical defects in the unit under test.

**Integration Testing**
- **Entry Criteria:** Individual units/modules have passed unit testing and are available for integration (e.g., the API layer and the database layer are both unit-tested); integration test environment is set up.
- **Exit Criteria:** All defined integration points (e.g., API ↔ DB, API ↔ Auth service) have been tested and pass; no open critical/high defects related to component interaction.

**System Testing**
- **Entry Criteria:** All modules are integrated into a complete, deployable build; the system test environment mirrors production configuration; integration testing exit criteria have been met.
- **Exit Criteria:** All planned end-to-end test cases (e.g., full course creation → enrollment → grading flow) have been executed; defect count is below the agreed threshold; no open critical/high severity defects.

**Acceptance Testing (UAT)**
- **Entry Criteria:** System testing is complete and signed off; a stable build is deployed to a UAT/staging environment; UAT test cases derived from business requirements are ready; business/end users (e.g., college admins) are available to test.
- **Exit Criteria:** All acceptance criteria (Given When Then scenarios) pass; business stakeholders formally sign off that the system meets their needs; no open critical defects.

### 12. Two Early QA Engagement Points in the V-Model

1. **Requirements Review stage:** QA reviews the requirements document for the Course Management API (e.g., "admins can create/update/delete courses") *before any code is written*, checking for ambiguity, testability, and missing edge cases (e.g., "what happens on a duplicate course code?" is a question QA should raise here, not discover during system testing).

2. **Architecture/System Design review stage:** QA participates in design reviews to understand how components will interact (e.g., how the API layer talks to the database, what error codes are planned for validation failures) and begins drafting Integration and System Test Plans in parallel with development rather than waiting until code is complete to start planning tests.

---

## Task 2: Agile QA and Shift-Left Testing

### 13. Three Problems with Waterfall (Test-After) for the Course Management API

1. **Defects are found late and are expensive to fix.** If a fundamental design flaw in how course codes are validated is only discovered during system testing (after all modules are coded), fixing it may require reworking the database schema, the API layer, and any dependent modules far more costly than catching it during the requirements review.

2. **No fast feedback loop for developers.** Developers who wrote the `POST /api/courses/` endpoint weeks or months ago have moved on to other features by the time testing starts. Context-switching back to fix defects is slow and error-prone, and they may have forgotten the original design decisions.

3. **Testing becomes a bottleneck under deadline pressure.** Because all testing is compressed into a single phase at the end of the project, if development runs late (as it often does), the testing phase gets squeezed leading to rushed, incomplete testing or a rushed release with unresolved defects.

### 14. QA's Role in Each Agile Ceremony

- **Sprint Planning:** QA collaborates with the product owner and developers to define clear, testable **Acceptance Criteria** for each user story before it's committed to the sprint (e.g., for "create a course" story, QA ensures criteria cover happy path, validation errors, and duplicate handling).

- **Daily Standup:** QA reports **blocking issues** — e.g., "I can't test the new course endpoint because the staging environment is down" or "Found a critical defect in course creation that's blocking further testing of the enrollment flow" — so the team can react immediately rather than at sprint end.

- **Sprint Review:** QA supports **demo testing** — helping validate that what's being demoed to stakeholders actually works as intended, and may highlight known limitations or edge cases not yet covered.

- **Retrospective:** QA contributes to **process improvement** — e.g., raising that too many defects related to input validation are slipping through, and proposing the team add validation-focused unit tests earlier in future sprints.

### 15. Four Shift-Left Practices Applied to the Course Management API

**(a) Reviewing requirements for testability**
Before development starts on a new "bulk course import" feature, QA reviews the requirement and asks: "What should happen if the uploaded file has 500 rows but row 250 has an invalid course code — does the whole import fail, or just that row?" This clarifies ambiguity before coding begins.

**(b) Writing test cases before code (TDD/BDD)**
For the `POST /api/courses/` endpoint, the team writes Given-When-Then acceptance criteria (see Step 16 below) *before* the endpoint is implemented. Developers then write code specifically to satisfy those pre-defined scenarios.

**(c) Static code analysis**
Tools like `pylint`, `flake8`, or `bandit` are run automatically on every commit to the Course Management API codebase, catching issues like unused variables, security vulnerabilities (e.g., SQL injection risks), or style violations before the code is even reviewed by a human, let alone tested.

**(d) API contract testing before integration**
Before the frontend team builds the course creation UI, they and the backend team agree on an OpenAPI/Swagger contract for `POST /api/courses/` (request/response schema). Contract tests validate the actual API implementation against this agreed schema *before* the frontend integrates with it, preventing integration surprises later.

### 16. Acceptance Criteria in Given-When-Then (Gherkin) Format

**User Story:** *As a college admin, I want to create a new course, so that students can enroll in it.*

```gherkin
Scenario: Successfully create a new course (Happy Path)
  Given I am logged in as an authenticated college admin
  And no course with the code "CS201" currently exists
  When I submit a request to create a course with code "CS201", name "Data Structures", credits 4, and instructor "Dr. Rao"
  Then the system should return a 201 Created response
  And the new course should appear in the course list with the provided details

Scenario: Attempt to create a course with a duplicate course code
  Given I am logged in as an authenticated college admin
  And a course with the code "CS201" already exists
  When I submit a request to create a course with code "CS201"
  Then the system should return a 409 Conflict response
  And an error message should indicate that the course code already exists
  And no duplicate course should be created in the system

Scenario: Attempt to create a course with missing required fields
  Given I am logged in as an authenticated college admin
  When I submit a request to create a course without providing a course "name"
  Then the system should return a 400 Bad Request response
  And an error message should indicate that "name" is a required field
  And no course should be created in the system
```
