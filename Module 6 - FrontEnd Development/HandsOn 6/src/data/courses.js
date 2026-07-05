// Fallback / seed course data.
// Task 66 originally seeds state with this; Task 71 replaces it with a live
// fetch from JSONPlaceholder, so this file is kept only as a shape reference
// and as a safety fallback if the fetch fails.

export const courses = [
  { id: 1, name: 'Data Structures', code: 'CS101', credits: 4, grade: 'A' },
  { id: 2, name: 'Web Development', code: 'CS205', credits: 3, grade: 'A-' },
  { id: 3, name: 'Database Systems', code: 'CS210', credits: 4, grade: 'B+' },
  { id: 4, name: 'Operating Systems', code: 'CS220', credits: 4, grade: 'B' },
  { id: 5, name: 'Software Engineering', code: 'CS230', credits: 3, grade: 'A' },
];
