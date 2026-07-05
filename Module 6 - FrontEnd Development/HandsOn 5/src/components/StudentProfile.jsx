/*
Task 3: useEffect Hook & Lifecycle

Goal: Use useEffect to fetch data and manage side effects.
*/

import { useState } from "react";

function StudentProfile() {

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [semester, setSemester] = useState("");

    return (

        <div className="profile">

            <h2>Student Profile</h2>

            <input
                type="text"
                placeholder="Enter Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />

            <input
                type="email"
                placeholder="Enter Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />

            <input
                type="number"
                placeholder="Semester"
                value={semester}
                onChange={(e) => setSemester(e.target.value)}
            />

            <h3>Entered Details</h3>

            <p>Name : {name}</p>
            <p>Email : {email}</p>
            <p>Semester : {semester}</p>

        </div>

    );

}

export default StudentProfile;
