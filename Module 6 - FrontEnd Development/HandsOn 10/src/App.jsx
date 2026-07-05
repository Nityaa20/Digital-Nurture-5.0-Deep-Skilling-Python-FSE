// App.jsx
import CourseList from "./components/CourseList";
import "./App.css";

// this component exists only to test that ErrorBoundary actually works
// clicking the button throws an error on purpose
function CrashTest() {
  function breakIt() {
    throw new Error("this is a fake crash to test the error boundary");
  }

  return <button onClick={breakIt}>Test Error Boundary (click to crash)</button>;
}

function App() {
  return (
    <div className="app">
      <header>
        <h1>Student Portal</h1>
      </header>

      <main>
        <CourseList />
        <CrashTest />
      </main>

      <footer>
        <p>&copy; 2026 Student Portal</p>
      </footer>
    </div>
  );
}

export default App;

/*
  testing the rejected thunk (this was step 147 in the exercise book):
  i changed the baseURL in apiClient.js from
  "https://jsonplaceholder.typicode.com" to
  "https://jsonplaceholder.typicode.com/xyz-does-not-exist" for a minute
  and reloaded the page. the rejected case in coursesSlice ran, the error
  text showed up on screen and the Retry button appeared, so the error
  handling is working. changed the baseURL back after testing.
*/
