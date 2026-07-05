// Task 63: simple functional component with a copyright line.
function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="site-footer">
      <p>&copy; {year} Student Portal. All rights reserved.</p>
    </footer>
  );
}

export default Footer;
