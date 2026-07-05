// courseApi.js
// all the course related API calls live here. components should only ever
// call these functions, they should never import axios or apiClient directly.

import apiClient from "./apiClient";

// jsonplaceholder does not really have a "courses" endpoint so I am reusing
// their /posts endpoint and just renaming the fields to look like courses.
// this is the same trick i used in handson 4 and handson 5.

export async function getAllCourses() {
  var posts = await apiClient.get("/posts?_limit=5");

  var courses = posts.map(function (post, index) {
    return {
      id: post.id,
      name: post.title,
      code: "CS10" + index,
      credits: (index % 3) + 2
    };
  });

  return courses;
}

export async function getCourseById(id) {
  var post = await apiClient.get("/posts/" + id);
  return {
    id: post.id,
    name: post.title,
    code: "CS10" + post.id,
    credits: 3
  };
}

export async function enrollStudent(studentId, courseId) {
  // jsonplaceholder lets you POST and it fakes a success response
  var result = await apiClient.post("/posts", {
    studentId: studentId,
    courseId: courseId
  });
  return result;
}
