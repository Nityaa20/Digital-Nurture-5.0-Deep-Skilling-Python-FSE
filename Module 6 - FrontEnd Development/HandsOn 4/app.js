/*
Task 1: Promises and async/await

Goal: Understand Promise chaining and rewrite it using async/await for cleaner code.

Task 2: Fetch API with Error Handling

Goal: Build a robust data-fetching layer with proper error handling and UI feedback.
*/

const courses = [
    {
        id: 1,
        name: "Web Development",
        credits: 4
    },
    {
        id: 2,
        name: "Database Systems",
        credits: 3
    },
    {
        id: 3,
        name: "Python Programming",
        credits: 4
    },
    {
        id: 4,
        name: "Operating Systems",
        credits: 4
    },
    {
        id: 5,
        name: "Computer Networks",
        credits: 3
    }
];

const courseList = document.getElementById("course-list");
const loading = document.getElementById("loading");

const notificationList = document.getElementById("notification-list");
const spinner = document.getElementById("spinner");
const errorMessage = document.getElementById("error-message");
const retryButton = document.getElementById("retry-btn");

function fetchUser(id){

    fetch("https://jsonplaceholder.typicode.com/users/" + id)
    .then(response => response.json())
    .then(data => {
        console.log("User Name:", data.name);
    });

}

fetchUser(1);

async function fetchUserAsync(id){

    try{

        const response = await fetch("https://jsonplaceholder.typicode.com/users/" + id);

        const data = await response.json();

        console.log("Async User:", data.name);

    }

    catch(error){

        console.log(error);

    }

}

fetchUserAsync(2);

function fetchAllCourses(){

    return new Promise(resolve => {

        setTimeout(() => {

            resolve(courses);

        },1000);

    });

}

function displayCourses(courseData){

    courseList.innerHTML = "";

    courseData.forEach(course=>{

        courseList.innerHTML += `
            <div class="course-card">
                <h3>${course.name}</h3>
                <p>Credits : ${course.credits}</p>
            </div>
        `;

    });

}

async function loadCourses(){

    loading.style.display = "block";

    const data = await fetchAllCourses();

    displayCourses(data);

    loading.style.display = "none";

}

loadCourses();

Promise.all([
    fetch("https://jsonplaceholder.typicode.com/users/1").then(res => res.json()),
    fetch("https://jsonplaceholder.typicode.com/users/2").then(res => res.json())
])
.then(users=>{

    console.log(users[0].name);

    console.log(users[1].name);

});

async function apiFetch(url){

    const response = await fetch(url);

    if(!response.ok){

        throw new Error("Unable to fetch data.");

    }

    return await response.json();

}

async function loadNotifications(){

    spinner.classList.remove("hidden");

    errorMessage.textContent = "";

    retryButton.style.display = "none";

    notificationList.innerHTML = "";

    try{

        const posts = await apiFetch("https://jsonplaceholder.typicode.com/posts?_limit=5");

        posts.forEach(post=>{

            notificationList.innerHTML += `
                <div class="notification-card">
                    <h3>${post.title}</h3>
                    <p>${post.body}</p>
                </div>
            `;

        });

    }

    catch(error){

        errorMessage.textContent = error.message;

        retryButton.style.display = "inline-block";

    }

    spinner.classList.add("hidden");

}

loadNotifications();

async function show404Error(){

    try{

        await apiFetch("https://jsonplaceholder.typicode.com/nonexistent");

    }

    catch(error){

        errorMessage.textContent = "Something went wrong. Please try again.";

        retryButton.style.display = "inline-block";

    }

}

show404Error();

retryButton.addEventListener("click",()=>{

    loadNotifications();

});
