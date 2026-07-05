// CourseList.jsx
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  fetchAllCourses,
  selectCourses,
  selectCoursesLoading,
  selectCoursesError
} from "../redux/coursesSlice";

function CourseList() {
  const dispatch = useDispatch();

  // using the selectors here instead of state.courses.list directly
  const courses = useSelector(selectCourses);
  const loading = useSelector(selectCoursesLoading);
  const error = useSelector(selectCoursesError);

  useEffect(function () {
    dispatch(fetchAllCourses());
    // empty array so this only runs once when the component first loads
  }, [dispatch]);

  function handleRetry() {
    dispatch(fetchAllCourses());
  }

  if (loading) {
    return <p>Loading courses, please wait...</p>;
  }

  if (error) {
    return (
      <div>
        <p style={{ color: "red" }}>Error: {error}</p>
        <button onClick={handleRetry}>Retry</button>
      </div>
    );
  }

  return (
    <div>
      <h2>My Courses</h2>
      <ul>
        {courses.map(function (course) {
          return (
            <li key={course.id}>
              {course.name} — {course.code} ({course.credits} credits)
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default CourseList;
