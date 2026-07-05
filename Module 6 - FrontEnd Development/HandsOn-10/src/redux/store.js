// store.js
import { configureStore } from "@reduxjs/toolkit";
import coursesReducer from "./coursesSlice";

const store = configureStore({
  reducer: {
    courses: coursesReducer
  }
});

export default store;
