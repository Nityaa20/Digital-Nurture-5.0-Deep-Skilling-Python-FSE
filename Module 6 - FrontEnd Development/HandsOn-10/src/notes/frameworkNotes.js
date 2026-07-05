// frameworkNotes.js
// I picked React for the actual coding part of this handson (like the note
// in the exercise book said we only need to pick one). This file is just my
// notes on how the other two frameworks (Angular with NgRx, Vue with Pinia)
// would have done the same thing, since the exercise asked to at least read
// and understand all three.

// ---------------------------------------------------------
// NgRx (Angular) - how it would work
// ---------------------------------------------------------
// NgRx follows the same redux pattern as what i did with Redux Toolkit,
// just with different names and more files.
//
// courses.actions.ts   -> would have something like: export const loadCourses
//                         = createAction('[Courses] Load Courses')
// courses.reducer.ts   -> a pure function that listens for that action and
//                         updates the state, no API calls allowed inside here
// courses.effects.ts   -> this is where the actual API call happens, it
//                         "listens" for loadCourses being dispatched, calls
//                         CourseService, and then dispatches a success or
//                         failure action back
//
// the data flow (this is basically the same idea as my thunk):
// Component dispatches loadCourses
//   -> Effect catches it and calls the CourseService (the actual http call)
//   -> Effect dispatches loadCoursesSuccess with the data
//   -> Reducer updates the state
//   -> Selector reads the state
//   -> Component gets the new courses through the selector
//
// the big difference from my React version is that in NgRx the reducer is
// never allowed to touch the API, that job belongs only to Effects.

// ---------------------------------------------------------
// Pinia (Vue) - advanced patterns
// ---------------------------------------------------------
// if i had built this in Vue, the enrollment store would look something
// like this (writing it here just as a rough idea, not real working code):
//
// export const useEnrollmentStore = defineStore('enrollment', () => {
//   const enrolledCourses = ref([])
//
//   async function fetchAndEnroll(courseId) {
//     const course = await getCourseById(courseId)
//     enrolledCourses.value.push(course)
//   }
//
//   function $reset() {
//     enrolledCourses.value = []
//   }
//
//   return { enrolledCourses, fetchAndEnroll, $reset }
// })
//
// fetchAndEnroll does the API call AND the state update in one single
// action, that is basically the same idea as my createAsyncThunk.
// storeToRefs(store) is used in components so you can pull out
// enrolledCourses without it losing its reactivity, normal destructuring
// like "const { enrolledCourses } = store" would break that in Vue.

// ---------------------------------------------------------
// Comparison - React+Redux vs Angular+NgRx vs Vue+Pinia
// ---------------------------------------------------------
// - Boilerplate: NgRx needs the most files (actions, reducers, effects,
//   selectors all separate). Redux Toolkit cut this down a lot compared to
//   old redux. Pinia needs the least code out of all three, it feels the
//   closest to just writing normal javascript functions.
//
// - Learning curve: NgRx felt the hardest to understand at first because of
//   Effects and RxJS observables. Redux Toolkit was medium, mainly need to
//   understand what a thunk is. Pinia was the easiest to just start using.
//
// - Built in tooling: all three have good devtools (Redux DevTools, NgRx
//   Devtools inside Angular Devtools, and Vue Devtools has a whole Pinia
//   tab). All of them let you see the state change live which is genuinely
//   useful for debugging.
//
// overall, for a small project like this Student Portal, Pinia or Redux
// Toolkit would be enough, NgRx starts making more sense in a bigger
// enterprise style app where teams need very strict structure.
