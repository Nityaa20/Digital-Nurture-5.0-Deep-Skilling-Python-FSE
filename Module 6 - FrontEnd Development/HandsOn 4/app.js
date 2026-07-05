/*
Task 3: Introduction to Axios

Goal: Compare Fetch with Axios and use Axios for API calls.
*/

// Fetch vs Axios
// 1. Fetch is built into browsers, Axios is an external library.
// 2. Fetch requires response.json(), Axios automatically converts JSON.
// 3. Fetch does not throw errors for HTTP errors, Axios throws automatically.

axios.interceptors.request.use(function(config){

    console.log("API call started:", config.url);

    return config;

});

async function axiosFetch(url){

    try{

        const response = await axios.get(url);

        return response.data;

    }

    catch(error){

        throw error;

    }

}

async function loadAxiosPosts(){

    try{

        const posts = await axiosFetch(
            "https://jsonplaceholder.typicode.com/posts"
        );

        console.log("Axios Posts");

        console.log(posts.slice(0,5));

    }

    catch(error){

        console.log(error.message);

    }

}

loadAxiosPosts();

async function loadUserPosts(){

    try{

        const response = await axios.get(

            "https://jsonplaceholder.typicode.com/posts",

            {

                params:{

                    userId:1

                }

            }

        );

        console.log("Posts of User 1");

        console.log(response.data);

    }

    catch(error){

        console.log(error.message);

    }

}

loadUserPosts();
