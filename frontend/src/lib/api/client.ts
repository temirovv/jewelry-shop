import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

// Get Telegram WebApp safely
const getTelegramWebApp = () => {
  try {
    return (window as any).Telegram?.WebApp;
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
      // Unauthorized - Telegram auth muammo
      console.error("Authentication error");
    }
    return Promise.reject(error);
  }
);

export default apiClient;
