// Task 62/64: functional component, receives siteName as a prop.
// Task 70: also receives enrolledCount as a prop and displays it.
function Header({ siteName, enrolledCount }) {
  return (
    <header className="site-header">
      <h1 className="site-title">{siteName}</h1>

      <nav aria-label="Main navigation">
        <ul className="nav-links">
          <li><a href="#home">Home</a></li>
          <li><a href="#courses">Courses</a></li>
          <li><a href="#profile">Profile</a></li>
        </ul>
      </nav>

      <div className="enrolled-badge">
        Enrolled: <strong>{enrolledCount}</strong>
      </div>
    </header>
  );
}

export default Header;
