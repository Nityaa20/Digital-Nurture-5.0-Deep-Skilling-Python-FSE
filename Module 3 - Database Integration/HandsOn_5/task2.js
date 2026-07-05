use("college_nosql");

// Task 65: Find all feedback with rating 5
db.feedback.find({
    rating: 5
});

// Task 66: Find feedback for CS101 having the tag "challenging"
db.feedback.find({
    course_code: "CS101",
    tags: "challenging"
});

// Task 67: Display only student_id, course_code and rating
db.feedback.find(
    {},
    {
        _id: 0,
        student_id: 1,
        course_code: 1,
        rating: 1
    }
);

// Task 68: Add needs_review field where rating is less than 3
db.feedback.updateMany(
    {
        rating: { $lt: 3 }
    },
    {
        $set: {
            needs_review: true
        }
    }
);

// Verify Task 68
db.feedback.find({
    needs_review: true
});

// Task 69: Add "reviewed" tag to documents needing review
db.feedback.updateMany(
    {
        needs_review: true
    },
    {
        $push: {
            tags: "reviewed"
        }
    }
);

// Verify Task 69
db.feedback.find({
    needs_review: true
});

// Task 70: Delete all feedback for semester 2021-EVEN
db.feedback.deleteMany({
    semester: "2021-EVEN"
});

// Verify Task 70
db.feedback.find();

// Count remaining documents
db.feedback.countDocuments();