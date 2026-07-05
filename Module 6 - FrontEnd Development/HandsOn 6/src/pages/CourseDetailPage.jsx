import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { enroll } from '../store/enrollmentSlice';
import { useCourses } from '../hooks/useCourses';

function CourseDetailPage() {
  // Task 79: read the courseId from the URL.
  const { courseId } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const { courses, loading } = useCourses();
  const enrolledCourses = useSelector((state) => state.enrollment.enrolledCourses);

  if (loading) return <p>Loading course...</p>;

  const course = courses.find((c) => String(c.id) === courseId);

  if (!course) {
    return <p>Course not found.</p>;
  }

  const isEnrolled = enrolledCourses.some((c) => c.id === course.id);

  // Task 80: after enrolling, navigate to /profile automatically.
  function handleEnroll() {
    dispatch(enroll(course));
    navigate('/profile');
  }

  return (
    <section className="course-detail">
      <h2>{course.name}</h2>
      <p className="course-code">{course.code}</p>
      <p>{course.credits} credits</p>
      <p>Grade: {course.grade}</p>

      <button type="button" disabled={isEnrolled} onClick={handleEnroll}>
        {isEnrolled ? 'Enrolled' : 'Enroll'}
      </button>
    </section>
  );
}

export default CourseDetailPage;
