import axios, { AxiosError, AxiosInstance } from "axios";
import WebApp from "@twa-dev/sdk";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor - Telegram auth qo'shish
apiClient.interceptors.request.use(
  (config) => {
    // Telegram WebApp initData ni header ga qo'shish
    if (WebApp.initData) {
      config.headers["X-Telegram-Init-Data"] = WebApp.initData;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - xatoliklarni boshqarish
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Unauthorized - Telegram auth muammo
      console.error("Authentication error");
    }
    return Promise.reject(error);
  }
);

export default apiClient;
