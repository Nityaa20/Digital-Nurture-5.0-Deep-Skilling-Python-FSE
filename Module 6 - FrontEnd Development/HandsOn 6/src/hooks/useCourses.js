import { useState, useEffect } from 'react';
import { courses as fallbackCourses } from '../data/courses';

// Shared fetch logic reused by CoursesPage and CourseDetailPage,
// same approach as Hands-On 5 Task 71/72/73.
export function useCourses() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadCourses() {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(
          'https://jsonplaceholder.typicode.com/posts?_limit=5'
        );
        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`);
        }
        const posts = await response.json();

        const mapped = posts.map((post, index) => ({
          id: post.id,
          name: post.title.slice(0, 24),
          code: `CS${100 + index}`,
          credits: 3 + (index % 2),
          grade: ['A', 'A-', 'B+', 'B', 'A'][index % 5],
        }));

        setCourses(mapped);
      } catch (err) {
        console.error('Failed to load courses:', err);
        setError('Could not load courses from the server. Showing sample data instead.');
        setCourses(fallbackCourses);
      } finally {
        setLoading(false);
      }
    }

    loadCourses();
  }, []);

  return { courses, loading, error };
}
