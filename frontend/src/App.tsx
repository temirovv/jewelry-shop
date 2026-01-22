import { useEffect } from "react";
import { HomePage } from "./pages/HomePage";
import { useTelegram } from "./hooks/useTelegram";
import { ToastContainer } from "./components/Toast";
import "./index.css";

function App() {
  const { colorScheme, themeParams, isReady } = useTelegram();

  useEffect(() => {
    // Set theme based on Telegram
    if (colorScheme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [colorScheme]);

  useEffect(() => {
    // Apply Telegram theme colors
    if (themeParams) {
      const root = document.documentElement;

      if (themeParams.bg_color) {
        root.style.setProperty("--tg-bg-color", themeParams.bg_color);
      }
      if (themeParams.text_color) {
        root.style.setProperty("--tg-text-color", themeParams.text_color);
      }
    }
  }, [themeParams]);

  if (!isReady) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="animate-pulse text-primary text-xl font-display">
          Loading...
        </div>
      </div>
    );
  }

  return (
    <>
      <HomePage />
      <ToastContainer />
    </>
  );
}

export default App;
