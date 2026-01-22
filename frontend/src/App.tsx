import { useEffect } from "react";
import { HomePage } from "./pages/HomePage";
import { useTelegram } from "./hooks/useTelegram";
import "./index.css";

function App() {
  const { webApp, colorScheme } = useTelegram();

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
    if (webApp.themeParams) {
      const root = document.documentElement;
      const params = webApp.themeParams;

      if (params.bg_color) {
        root.style.setProperty("--tg-bg-color", params.bg_color);
      }
      if (params.text_color) {
        root.style.setProperty("--tg-text-color", params.text_color);
      }
    }
  }, [webApp.themeParams]);

  return <HomePage />;
}

export default App;
