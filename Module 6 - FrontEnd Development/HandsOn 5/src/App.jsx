import { useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import CourseCard from './components/CourseCard';
import StudentProfile from './components/StudentProfile';
import { courses as fallbackCourses } from './data/courses';
import './App.css';

function App() {
  // ---- Task 66/71: course data, now loaded from an API instead of hardcoded ----
  const [courses, setCourses] = useState([]);

  // ---- Task 68: search state ----
  const [searchTerm, setSearchTerm] = useState('');

  // ---- Task 69: lifted-up enrollment state (shared by CourseCard + Header + Profile) ----
  const [enrolledCourses, setEnrolledCourses] = useState([]);

  // ---- Task 72/73: loading + error state for the fetch ----
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Task 71: fetch courses from JSONPlaceholder on mount, mapping the first
  // 5 posts into course-like objects. Task 72/73: track loading + error state.
  useEffect(() => {
    async function loadCourses() {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(
          'https://jsonplaceholder.typicode.com/posts?_limit=5'
        );
        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`);
        }
        const posts = await response.json();

        const mapped = posts.map((post, index) => ({
          id: post.id,
          name: post.title.slice(0, 24),
          code: `CS${100 + index}`,
          credits: 3 + (index % 2),
          grade: ['A', 'A-', 'B+', 'B', 'A'][index % 5],
        }));

        setCourses(mapped);
      } catch (err) {
        console.error('Failed to load courses:', err);
        setError('Could not load courses from the server. Showing sample data instead.');
        setCourses(fallbackCourses);
      } finally {
        setLoading(false);
      }
    }

    loadCourses();
  }, []); // empty dependency array = run once after mount

  // Task 75: log whenever the courses list changes.
  // The dependency array [courses] matters because it tells React to re-run
  // this effect ONLY when `courses` changes, instead of after every render.
  // Without it (no array at all) the effect would run after every render,
  // including ones unrelated to courses, and could cause needless work or
  // even infinite loops if the effect itself triggers a state update.
  useEffect(() => {
    if (courses.length > 0) {
      console.log('Courses updated');
    }
  }, [courses]);

  // Task 69: handler passed down to CourseCard via props (lifting state up).
  function handleEnroll(courseId) {
    const alreadyEnrolled = enrolledCourses.some((c) => c.id === courseId);
    if (alreadyEnrolled) return;

    const courseToEnroll = courses.find((c) => c.id === courseId);
    if (courseToEnroll) {
      setEnrolledCourses((prev) => [...prev, courseToEnroll]);
    }
  }

  // Task 68: filter courses by search term (case-insensitive).
  const filteredCourses = courses.filter((course) =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <>
      <Header siteName="Student Portal" enrolledCount={enrolledCourses.length} />

      <main>
        <section id="courses" className="courses-section">
          <h2>Courses</h2>

          <input
            type="text"
            placeholder="Search courses..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            aria-label="Search courses"
          />

          {loading && <p>Loading courses...</p>}
          {error && <p className="error-message">{error}</p>}

          {!loading && (
            <div className="course-grid">
              {filteredCourses.map((course) => (
                <CourseCard
                  key={course.id}
                  {...course}
                  onEnroll={handleEnroll}
                  isEnrolled={enrolledCourses.some((c) => c.id === course.id)}
                />
              ))}
            </div>
          )}
        </section>

        <StudentProfile enrolledCourses={enrolledCourses} />
      </main>

      <Footer />
    </>
  );
}

export default App;
