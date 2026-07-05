import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <section className="hero">
      <h2>Welcome to the Student Portal</h2>
      <p>Browse your courses, manage enrollments, and track your profile.</p>
      <Link to="/courses">
        <button type="button">Explore Courses</button>
      </Link>
    </section>
  );
}

export default HomePage;
