import { useEffect, useState, useCallback } from "react";
import WebApp from "@twa-dev/sdk";

interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  language_code?: string;
}

interface UseTelegramReturn {
  webApp: typeof WebApp;
  user: TelegramUser | null;
  isReady: boolean;
  colorScheme: "light" | "dark";
  themeParams: typeof WebApp.themeParams;
  showMainButton: (text: string, onClick: () => void) => void;
  hideMainButton: () => void;
  showBackButton: (onClick: () => void) => void;
  hideBackButton: () => void;
  hapticFeedback: typeof WebApp.HapticFeedback;
  close: () => void;
  expand: () => void;
}

export function useTelegram(): UseTelegramReturn {
  const [isReady, setIsReady] = useState(false);
  const [user, setUser] = useState<TelegramUser | null>(null);

  useEffect(() => {
    WebApp.ready();
    WebApp.expand();
    setIsReady(true);

    if (WebApp.initDataUnsafe?.user) {
      setUser(WebApp.initDataUnsafe.user);
    }
  }, []);

  const showMainButton = useCallback((text: string, onClick: () => void) => {
    WebApp.MainButton.setText(text);
    WebApp.MainButton.onClick(onClick);
    WebApp.MainButton.show();
  }, []);

  const hideMainButton = useCallback(() => {
    WebApp.MainButton.hide();
  }, []);

  const showBackButton = useCallback((onClick: () => void) => {
    WebApp.BackButton.onClick(onClick);
    WebApp.BackButton.show();
  }, []);

  const hideBackButton = useCallback(() => {
    WebApp.BackButton.hide();
  }, []);

  return {
    webApp: WebApp,
    user,
    isReady,
    colorScheme: WebApp.colorScheme,
    themeParams: WebApp.themeParams,
    showMainButton,
    hideMainButton,
    showBackButton,
    hideBackButton,
    hapticFeedback: WebApp.HapticFeedback,
    close: WebApp.close,
    expand: WebApp.expand,
  };
}
