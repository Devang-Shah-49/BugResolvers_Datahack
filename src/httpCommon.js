import axios from "axios";


export default axios.create({
    baseURL: "",  // enter backend url here

    headers: {
        "Content-type": "application/json",
        Accept: "application/json",
        "Access-Control-Allow-Origin": "*"
    },
    mode: "cors"
});