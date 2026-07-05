// apiClient.js
// this is the one place where axios is configured, every other file should
// import this instead of calling axios directly. that way if the baseURL
// changes tomorrow I only have to change it here.

import axios from "axios";

const apiClient = axios.create({
  baseURL: "https://jsonplaceholder.typicode.com",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json"
  }
});

// request interceptor - attaches a fake token to every request
// (jsonplaceholder does not actually check this but in a real project
// this is where the login token would go)
apiClient.interceptors.request.use(function (config) {
  config.headers.Authorization = "Bearer mock-token-12345";
  console.log("sending request to:", config.url);
  return config;
});

// response interceptor - this does two things
// 1. it returns response.data directly so my components dont have to
//    write response.data.data everywhere, they just get the data
// 2. if something goes wrong it throws one simple Error object with a
//    message and statusCode so components dont need to know about axios
apiClient.interceptors.response.use(
  function (response) {
    return response.data;
  },
  function (error) {
    var statusCode = error.response ? error.response.status : 0;
    var message = error.response
      ? "Something went wrong (status " + statusCode + ")"
      : "Network error, please check your internet connection";

    var newError = new Error(message);
    newError.statusCode = statusCode;
    return Promise.reject(newError);
  }
);

export default apiClient;
