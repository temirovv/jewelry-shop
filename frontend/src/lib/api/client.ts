import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

// Get Telegram WebApp safely
const getTelegramWebApp = () => {
  try {
    return (window as unknown as { Telegram?: { WebApp?: { initData?: string } } }).Telegram?.WebApp;
  } catch {
    return null;
  }
};

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor - Telegram auth qo'shish
apiClient.interceptors.request.use(
  (config) => {
    // Telegram WebApp initData ni header ga qo'shish
    const webApp = getTelegramWebApp();
    if (webApp?.initData) {
      config.headers["X-Telegram-Init-Data"] = webApp.initData;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - xatoliklarni boshqarish
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.error("Telegram authentication failed");
    }

    // Extract readable error message from response
    const data = error.response?.data;
    if (data) {
      const message =
        typeof data === "string"
          ? data
          : data.error || data.detail || Object.values(data).flat().join(", ");
      if (message) {
        error.message = message;
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
