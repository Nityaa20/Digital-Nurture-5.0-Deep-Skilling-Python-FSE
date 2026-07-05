import { configureStore } from '@reduxjs/toolkit';
import enrollmentReducer from './enrollmentSlice';

// Task 86: configureStore from Redux Toolkit.
const store = configureStore({
  reducer: {
    enrollment: enrollmentReducer,
  },
});

export default store;
