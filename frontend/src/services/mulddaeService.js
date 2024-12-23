import axios from 'axios';

const instance = axios.create({
  baseURL: "http://13.55.133.76:5000", // Use the public IP address
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true, // Include credentials in requests
});

export const fetchMulddae = async (data) => {
  try {
    const response = await instance.post('/backend/mulddae', data);
    return response.data;
  } catch (error) {
    console.error('Error fetching mulddae data:', error);
    throw error;
  }
};
