import axios from "axios";

const instance = axios.create({
  baseURL: "http://localhost:5000", // Ensure this matches your backend's base URL
  withCredentials: true, // Include credentials in requests
});

export default instance;
