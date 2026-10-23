import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const checkAvailability = async (productId) => {
  const res = await api.get(`/inventory/${productId}`);
  return res.data;
};

export default api;