import { Link } from 'react-router-dom';

// Task 79: cards link to /courses/:courseId via <Link>.
function CourseCard({ id, name, code, credits, grade, onEnroll, isEnrolled }) {
  return (
    <article className="course-card">
      <h3>
        <Link to={`/courses/${id}`}>{name}</Link>
      </h3>
      <p className="course-code">{code}</p>
      <p>{credits} credits</p>
      <p>Grade: {grade}</p>

      <button
        type="button"
        disabled={isEnrolled}
        onClick={() => onEnroll({ id, name, code, credits, grade })}
      >
        {isEnrolled ? 'Enrolled' : 'Enroll'}
      </button>
    </article>
  );
}

export default CourseCard;
