/*
Task 2: State with useState and Dynamic Lists

Goal: Use useState to manage component state and render dynamic lists.

Task 3: useEffect Hook & Lifecycle

Goal: Use useEffect to fetch data and manage side effects.
*/

import { useEffect, useState } from "react";

import Header from "./components/Header";
import Footer from "./components/Footer";
import CourseCard from "./components/CourseCard";
import StudentProfile from "./components/StudentProfile";

import coursesData from "./data";

function App() {

    const [courses, setCourses] = useState([]);

    const [searchTerm, setSearchTerm] = useState("");

    const [enrolledCourses, setEnrolledCourses] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");

    useEffect(() => {

        async function fetchCourses() {

            try {

                const response = await fetch("https://jsonplaceholder.typicode.com/posts");

                if (!response.ok) {

                    throw new Error("Failed to fetch courses");

                }

                const posts = await response.json();

                const apiCourses = posts.slice(0, 5).map((post, index) => ({

                    id: index + 1,

                    name: post.title,

                    code: `CS10${index + 1}`,

                    credits: coursesData[index].credits,

                    grade: coursesData[index].grade

                }));

                setCourses(apiCourses);

            }

            catch (err) {

                setError(err.message);

                setCourses(coursesData);

            }

            finally {

                setLoading(false);

            }

        }

        fetchCourses();

    }, []);

    useEffect(() => {

        console.log("Courses updated");

    }, [courses]);

    function handleEnroll(id) {

        const selectedCourse = courses.find(course => course.id === id);

        if (selectedCourse && !enrolledCourses.some(course => course.id === id)) {

            setEnrolledCourses([...enrolledCourses, selectedCourse]);

        }

    }

    const filteredCourses = courses.filter(course =>
        course.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (loading) {

        return <h2>Loading...</h2>;

    }

    return (

        <>

            <Header
                siteName="Student Portal"
                enrolledCount={enrolledCourses.length}
            />

            <div className="container">

                <input
                    type="text"
                    placeholder="Search Course"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />

                {error && <h3>{error}</h3>}

                <div className="course-grid">

                    {filteredCourses.map(course => (

                        <CourseCard

                            key={course.id}

                            {...course}

                            onEnroll={handleEnroll}

                        />

                    ))}

                </div>

                <StudentProfile />

            </div>

            <Footer />

        </>

    );

}

export default App;
