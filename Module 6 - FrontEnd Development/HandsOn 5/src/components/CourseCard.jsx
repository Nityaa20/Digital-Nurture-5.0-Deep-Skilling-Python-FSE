// Task 65: accepts name, code, credits, grade as props and renders a card.
// Task 69: also accepts an onEnroll handler (state is lifted up to App.jsx).
function CourseCard({ id, name, code, credits, grade, onEnroll, isEnrolled }) {
  return (
    <article className="course-card">
      <h3>{name}</h3>
      <p className="course-code">{code}</p>
      <p>{credits} credits</p>
      <p>Grade: {grade}</p>

      <button
        type="button"
        disabled={isEnrolled}
        onClick={() => onEnroll(id)}
      >
        {isEnrolled ? 'Enrolled' : 'Enroll'}
      </button>
    </article>
  );
}

export default CourseCard;
