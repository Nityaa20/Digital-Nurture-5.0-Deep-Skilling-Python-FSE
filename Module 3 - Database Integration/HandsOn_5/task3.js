use("college_nosql");

// Task 71: Calculate average rating and total feedback for each course in semester 2022-ODD
db.feedback.aggregate([
    {
        $match: {
            semester: "2022-ODD"
        }
    },
    {
        $group: {
            _id: "$course_code",
            average_rating: {
                $avg: "$rating"
            },
            total_feedback: {
                $sum: 1
            }
        }
    },
    {
        $sort: {
            average_rating: -1
        }
    }
]);

// Task 72: Display course code, average rating (rounded), and total feedback
db.feedback.aggregate([
    {
        $match: {
            semester: "2022-ODD"
        }
    },
    {
        $group: {
            _id: "$course_code",
            average_rating: {
                $avg: "$rating"
            },
            total_feedback: {
                $sum: 1
            }
        }
    },
    {
        $project: {
            _id: 0,
            course_code: "$_id",
            average_rating: {
                $round: ["$average_rating", 1]
            },
            total_feedback: 1
        }
    },
    {
        $sort: {
            average_rating: -1
        }
    }
]);

// Task 73: Display the frequency of each tag
db.feedback.aggregate([
    {
        $unwind: "$tags"
    },
    {
        $group: {
            _id: "$tags",
            frequency: {
                $sum: 1
            }
        }
    },
    {
        $sort: {
            frequency: -1
        }
    }
]);

// Task 74: Create an index on course_code
db.feedback.createIndex({
    course_code: 1
});

// Verify that the index is used
db.feedback.find({
    course_code: "CS101"
}).explain("executionStats");