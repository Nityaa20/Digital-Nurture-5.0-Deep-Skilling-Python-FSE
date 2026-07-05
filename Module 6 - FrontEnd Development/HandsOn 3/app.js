/*
Task 1: ES6+ Syntax Practice

Goal: Rewrite common JavaScript patterns using modern ES6+ features.

Task 2: DOM Selection & Dynamic Rendering

Goal: Select elements, modify the DOM, and render data dynamically.

Task 3: Event Listeners & Interactivity

Goal: Add user interactions using event listeners and DOM updates.
*/

import { courses } from "./data.js";

const courseGrid = document.querySelector(".course-grid");
const totalCredits = document.querySelector("#total-credits");
const searchInput = document.querySelector("#search-courses");
const sortButton = document.querySelector("#sort-btn");
const selectedCourse = document.querySelector("#selected-course");

courses.forEach(({ name, credits }) => {
    console.log(`${name} - ${credits} credits`);
});

const formattedCourses = courses.map(
    ({ code, name, credits }) => `${code} — ${name} (${credits} credits)`
);

console.log(formattedCourses);

const filteredCourses = courses.filter(course => course.credits >= 4);

console.log(filteredCourses);
console.log("Number of Courses:", filteredCourses.length);

const creditSum = courses.reduce(
    (total, course) => total + course.credits,
    0
);

console.log("Total Credits:", creditSum);

function renderCourses(courseList){

    courseGrid.innerHTML = "";

    courseList.forEach(course=>{

        const article = document.createElement("article");

        article.className = "course-card";

        article.dataset.id = course.id;

        article.innerHTML = `
            <h3>${course.name}</h3>
            <p>Course Code : ${course.code}</p>
            <p>Credits : ${course.credits}</p>
            <span>Grade : ${course.grade}</span>
        `;

        courseGrid.appendChild(article);

    });

    const total = courseList.reduce(
        (sum, course)=>sum + course.credits,
        0
    );

    totalCredits.textContent = `Total Credits : ${total}`;

}

renderCourses(courses);

searchInput.addEventListener("input",()=>{

    const value = searchInput.value.toLowerCase();

    const result = courses.filter(course=>
        course.name.toLowerCase().includes(value)
    );

    renderCourses(result);

});

sortButton.addEventListener("click",()=>{

    const sorted = [...courses].sort(
        (a,b)=>b.credits-a.credits
    );

    renderCourses(sorted);

});

courseGrid.addEventListener("click",(event)=>{

    const card = event.target.closest(".course-card");

    if(!card) return;

    const id = Number(card.dataset.id);

    const course = courses.find(c=>c.id===id);

    selectedCourse.innerHTML = `
        <h3>Selected Course</h3>
        <p>Name : ${course.name}</p>
        <p>Grade : ${course.grade}</p>
    `;

});
