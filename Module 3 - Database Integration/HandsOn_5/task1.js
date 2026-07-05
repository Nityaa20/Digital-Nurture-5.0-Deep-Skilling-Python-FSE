// Create Collection & Insert Documents

use("college_nosql");

// Create collection (run only once)
db.createCollection("feedback");

// Insert 10 feedback documents

db.feedback.insertMany([
{
    student_id: 1,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 5,
    comments: "Excellent teaching.",
    tags: ["challenging", "well-structured", "good-examples"],
    submitted_at: new Date(),
    attachments: [
        {
            filename: "notes.pdf",
            size_kb: 240
        }
    ]
},
{
    student_id: 2,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 4,
    comments: "Very useful.",
    tags: ["challenging", "interactive"],
    submitted_at: new Date(),
    attachments: [
        {
            filename: "dbms.pdf",
            size_kb: 180
        }
    ]
},
{
    student_id: 5,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 5,
    comments: "Loved the course.",
    tags: ["challenging", "good-examples"],
    submitted_at: new Date(),
    attachments: [
        {
            filename: "assignment.pdf",
            size_kb: 120
        }
    ]
},
{
    student_id: 1,
    course_code: "CS102",
    semester: "2022-ODD",
    rating: 4,
    comments: "Good course.",
    tags: ["database", "practical"],
    submitted_at: new Date(),
    attachments: [
        {
            filename: "lab.pdf",
            size_kb: 210
        }
    ]
},
{
    student_id: 8,
    course_code: "CS102",
    semester: "2022-ODD",
    rating: 2,
    comments: "Needs improvement.",
    tags: ["database", "lengthy"],
    submitted_at: new Date(),
    attachments: [
        {
            filename: "report.pdf",
            size_kb: 150
        }
    ]
},
{
    student_id: 3,
    course_code: "EC101",
    semester: "2021-EVEN",
    rating: 3,
    comments: "Average.",
    tags: ["electronics"],
    submitted_at: new Date(),
    attachments: [
        {
            filename: "ec.pdf",
            size_kb: 160
        }
    ]
},
{
    student_id: 4,
    course_code: "ME101",
    semester: "2023-ODD",
    rating: 5,
    comments: "Excellent.",
    tags: ["mechanical", "practical"],
    submitted_at: new Date(),
    attachments: [
        {
            filename: "me.pdf",
            size_kb: 170
        }
    ]
},
{
    student_id: 6,
    course_code: "EC101",
    semester: "2021-EVEN",
    rating: 2,
    comments: "Needs more examples.",
    tags: ["electronics", "difficult"],
    submitted_at: new Date(),
    attachments: [
        {
            filename: "circuit.pdf",
            size_kb: 110
        }
    ]
},
{
    student_id: 7,
    course_code: "ME101",
    semester: "2023-ODD",
    rating: 4,
    comments: "Interesting course.",
    tags: ["mechanical"],
    submitted_at: new Date(),
    attachments: [
        {
            filename: "notes.doc",
            size_kb: 95
        }
    ]
},
{
    student_id: 2,
    course_code: "CS103",
    semester: "2022-ODD",
    rating: 5,
    comments: "Best programming course.",
    tags: ["oop", "coding"],
    submitted_at: new Date()
}
]);

// Verify insertion
db.feedback.countDocuments();