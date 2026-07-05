import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';

// Task 78: use <Link> instead of <a> tags — no full page reload.
// Enrolled count now comes from Redux via useSelector (Task 89).
function Header() {
  const enrolledCount = useSelector((state) => state.enrollment.enrolledCourses.length);

  return (
    <header className="site-header">
      <h1 className="site-title">Student Portal</h1>

      <nav aria-label="Main navigation">
        <ul className="nav-links">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/courses">Courses</Link></li>
          <li><Link to="/profile">Profile</Link></li>
        </ul>
      </nav>

      <div className="enrolled-badge">
        Enrolled: <strong>{enrolledCount}</strong>
      </div>
    </header>
  );
}

export default Header;
