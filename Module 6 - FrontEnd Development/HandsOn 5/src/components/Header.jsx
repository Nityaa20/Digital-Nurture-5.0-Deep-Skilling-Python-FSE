/*
Task 1: Project Setup & First Components

Goal: Scaffold the React app and create the first reusable components.
*/

function Header({ siteName, enrolledCount }) {

    return (

        <header className="header">

            <h1>{siteName}</h1>

            <nav>

                <a href="#">Home</a>

                <a href="#">Courses</a>

                <a href="#">Profile</a>

            </nav>

            <h3>Enrolled : {enrolledCount}</h3>

        </header>

    );

}

export default Header;
