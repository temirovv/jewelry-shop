import { useEffect, useState, useCallback } from "react";

interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  language_code?: string;
}

interface ThemeParams {
  bg_color?: string;
  text_color?: string;
  hint_color?: string;
  link_color?: string;
  button_color?: string;
  button_text_color?: string;
}

interface HapticFeedback {
  impactOccurred: (style: "light" | "medium" | "heavy" | "rigid" | "soft") => void;
  notificationOccurred: (type: "error" | "success" | "warning") => void;
  selectionChanged: () => void;
}

interface UseTelegramReturn {
  webApp: any;
  user: TelegramUser | null;
  isReady: boolean;
  isTelegram: boolean;
  colorScheme: "light" | "dark";
  themeParams: ThemeParams;
  showMainButton: (text: string, onClick: () => void) => void;
  hideMainButton: () => void;
  showBackButton: (onClick: () => void) => void;
  hideBackButton: () => void;
  hapticFeedback: HapticFeedback;
  close: () => void;
  expand: () => void;
}

// Check if running in Telegram WebApp
const isTelegramWebApp = (): boolean => {
  try {
    return !!(window as any).Telegram?.WebApp?.initData;
  } catch {
    return false;
  }
};

// Mock haptic feedback for browser
const mockHapticFeedback: HapticFeedback = {
  impactOccurred: () => {},
  notificationOccurred: () => {},
  selectionChanged: () => {},
};

export function useTelegram(): UseTelegramReturn {
  const [isReady, setIsReady] = useState(false);
  const [user, setUser] = useState<TelegramUser | null>(null);
  const [isTelegram, setIsTelegram] = useState(false);

  useEffect(() => {
    const checkTelegram = isTelegramWebApp();
    setIsTelegram(checkTelegram);

    if (checkTelegram) {
      const WebApp = (window as any).Telegram.WebApp;
      WebApp.ready();
      WebApp.expand();

      if (WebApp.initDataUnsafe?.user) {
        setUser(WebApp.initDataUnsafe.user);
      }
    }

    setIsReady(true);
  }, []);

  const getWebApp = () => {
    if (isTelegram) {
      return (window as any).Telegram.WebApp;
    }
    return null;
  };

  const showMainButton = useCallback((text: string, onClick: () => void) => {
    const WebApp = getWebApp();
    if (WebApp) {
      WebApp.MainButton.setText(text);
      WebApp.MainButton.onClick(onClick);
      WebApp.MainButton.show();
    }
  }, [isTelegram]);

  const hideMainButton = useCallback(() => {
    const WebApp = getWebApp();
    if (WebApp) {
      WebApp.MainButton.hide();
    }
  }, [isTelegram]);

  const showBackButton = useCallback((onClick: () => void) => {
    const WebApp = getWebApp();
    if (WebApp) {
      WebApp.BackButton.onClick(onClick);
      WebApp.BackButton.show();
    }
  }, [isTelegram]);

  const hideBackButton = useCallback(() => {
    const WebApp = getWebApp();
    if (WebApp) {
      WebApp.BackButton.hide();
    }
  }, [isTelegram]);

  const webApp = getWebApp();

  return {
    webApp,
    user,
    isReady,
    isTelegram,
    colorScheme: webApp?.colorScheme || "light",
    themeParams: webApp?.themeParams || {},
    showMainButton,
    hideMainButton,
    showBackButton,
    hideBackButton,
    hapticFeedback: webApp?.HapticFeedback || mockHapticFeedback,
    close: () => webApp?.close?.(),
    expand: () => webApp?.expand?.(),
  };
}
