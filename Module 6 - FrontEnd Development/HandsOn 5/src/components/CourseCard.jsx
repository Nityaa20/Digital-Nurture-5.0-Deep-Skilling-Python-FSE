/*
Task 1: Project Setup & First Components

Goal: Scaffold the React app and create the first reusable components.

Task 2: State with useState and Dynamic Lists

Goal: Use useState to manage component state and render dynamic lists.
*/

function CourseCard({

    id,
    name,
    code,
    credits,
    grade,
    onEnroll

}){

    return(

        <div className="course-card">

            <h2>{name}</h2>

            <p><strong>Code :</strong> {code}</p>

            <p><strong>Credits :</strong> {credits}</p>

            <p><strong>Grade :</strong> {grade}</p>

            <button onClick={() => onEnroll(id)}>
                Enroll
            </button>

        </div>

    );

}

export default CourseCard;
