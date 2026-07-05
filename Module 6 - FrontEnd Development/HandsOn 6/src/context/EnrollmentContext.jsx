import { createContext, useState, useContext } from 'react';

// Task 81: Context for enrollment state.
// NOTE: This was used for Task 2 (Context API practice). In Task 3 the app
// switches to Redux Toolkit (see store/enrollmentSlice.js) as the single
// source of truth. This file is kept as a reference for the Context
// approach but is no longer wired into App.jsx.
const EnrollmentContext = createContext(null);

export function EnrollmentProvider({ children }) {
  const [enrolledCourses, setEnrolledCourses] = useState([]);

  function enrollCourse(course) {
    setEnrolledCourses((prev) =>
      prev.some((c) => c.id === course.id) ? prev : [...prev, course]
    );
  }

  // Task 84: remove function to un-enroll.
  function removeCourse(courseId) {
    setEnrolledCourses((prev) => prev.filter((c) => c.id !== courseId));
  }

  return (
    <EnrollmentContext.Provider value={{ enrolledCourses, enrollCourse, removeCourse }}>
      {children}
    </EnrollmentContext.Provider>
  );
}

export function useEnrollment() {
  return useContext(EnrollmentContext);
}
