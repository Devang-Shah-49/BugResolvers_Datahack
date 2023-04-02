import axios from "axios";

const errHandler = async (promise) => {
    try {
        const res = await promise;
        return [res, null];
    } catch (err) {
        console.log(err);
        return [null, err];
    }
}

const ApiService = {
    init: (baseUrl) => {
        axios.defaults.baseURL = baseUrl;
    },

    setHeader: () => {
        axios.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem("token")}`;
    },

    removeHeader: () => {
        delete axios.defaults.headers.common["Authorization"];
    },
    
    get: (url, config) => {
        return errHandler(axios.get(url, config));
    },

    post: (url, data, config) => {
        return errHandler(axios.post(url, data, config));
    },

    put: (url, data, config) => {
        return errHandler(axios.put(url, data, config));
    },

    delete: (url, config) => {
        return errHandler(axios.delete(url, config));
    },
}

export default ApiService;