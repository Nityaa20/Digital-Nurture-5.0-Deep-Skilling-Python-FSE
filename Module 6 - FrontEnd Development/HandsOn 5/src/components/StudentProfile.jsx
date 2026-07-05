import { useState } from 'react';

// Task 74: separate component with its OWN local state (name, email, semester).
// This state is local because it's a UI-only form concern — it does not need
// to be shared with any other component, so it stays here rather than being
// lifted up to App.jsx.
function StudentProfile({ enrolledCourses }) {
  const [profile, setProfile] = useState({
    name: '',
    email: '',
    semester: '',
  });

  function handleChange(event) {
    const { name, value } = event.target;
    setProfile((prev) => ({ ...prev, [name]: value }));
  }

  function handleSubmit(event) {
    event.preventDefault();
    console.log('Profile submitted:', profile);
  }

  return (
    <section id="profile" className="profile-section">
      <h2>Student Profile</h2>

      <form onSubmit={handleSubmit}>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          name="name"
          type="text"
          value={profile.name}
          onChange={handleChange}
        />

        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          value={profile.email}
          onChange={handleChange}
        />

        <label htmlFor="semester">Semester</label>
        <input
          id="semester"
          name="semester"
          type="number"
          min="1"
          max="8"
          value={profile.semester}
          onChange={handleChange}
        />

        <button type="submit">Save Profile</button>
      </form>

      <h3>Enrolled Courses ({enrolledCourses.length})</h3>
      {enrolledCourses.length === 0 ? (
        <p>You haven't enrolled in any courses yet.</p>
      ) : (
        <ul>
          {enrolledCourses.map((course) => (
            <li key={course.id}>
              {course.name} ({course.code}) — {course.credits} credits
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default StudentProfile;
