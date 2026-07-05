/*
Task 1: Project Setup & First Components

Goal: Scaffold the React app and create the first reusable components.
*/

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./App.css";

ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
