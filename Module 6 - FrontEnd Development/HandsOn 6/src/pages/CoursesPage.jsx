import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { enroll } from '../store/enrollmentSlice';
import { useCourses } from '../hooks/useCourses';
import CourseCard from '../components/CourseCard';

function CoursesPage() {
  const { courses, loading, error } = useCourses();
  const [searchTerm, setSearchTerm] = useState('');

  const dispatch = useDispatch();
  const enrolledCourses = useSelector((state) => state.enrollment.enrolledCourses);

  const filteredCourses = courses.filter((course) =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  function handleEnroll(course) {
    dispatch(enroll(course));
  }

  return (
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
  );
}

export default CoursesPage;
