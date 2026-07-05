// coursesSlice.js
// this handles fetching courses using redux toolkit's createAsyncThunk
// so i dont have to write loading/error state manually every time

import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { getAllCourses } from "../api/courseApi";

// this is the thunk. redux toolkit automatically creates 3 action types
// for this: pending, fulfilled and rejected
export const fetchAllCourses = createAsyncThunk(
  "courses/fetchAll",
  async function () {
    var data = await getAllCourses();
    return data;
  }
);

const coursesSlice = createSlice({
  name: "courses",
  initialState: {
    list: [],
    loading: false,
    error: null
  },
  reducers: {
    // not using any normal reducers for now, only the thunk below
  },
  extraReducers: function (builder) {
    builder
      .addCase(fetchAllCourses.pending, function (state) {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAllCourses.fulfilled, function (state, action) {
        state.loading = false;
        state.list = action.payload;
      })
      .addCase(fetchAllCourses.rejected, function (state, action) {
        state.loading = false;
        // action.error.message comes from the Error we threw in apiClient.js
        state.error = action.error.message;
      });
  }
});

// selectors - components use these instead of touching state.courses directly
// this way if i ever rename "courses" to something else in the store, i only
// fix it here and not in every component
export const selectCourses = function (state) {
  return state.courses.list;
};

export const selectCoursesLoading = function (state) {
  return state.courses.loading;
};

export const selectCoursesError = function (state) {
  return state.courses.error;
};

export default coursesSlice.reducer;
