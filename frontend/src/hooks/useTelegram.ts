import { useState, useCallback, useMemo } from "react";

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

interface TelegramWebApp {
  initData: string;
  initDataUnsafe: { user?: TelegramUser };
  colorScheme: "light" | "dark";
  themeParams: ThemeParams;
  HapticFeedback: HapticFeedback;
  MainButton: {
    setText: (text: string) => void;
    onClick: (cb: () => void) => void;
    show: () => void;
    hide: () => void;
  };
  BackButton: {
    onClick: (cb: () => void) => void;
    show: () => void;
    hide: () => void;
  };
  ready: () => void;
  expand: () => void;
  close: () => void;
}

interface UseTelegramReturn {
  webApp: TelegramWebApp | null;
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
const getTelegramWebApp = (): TelegramWebApp | null => {
  try {
    const tg = (window as unknown as { Telegram?: { WebApp?: TelegramWebApp } }).Telegram;
    if (tg?.WebApp) {
      return tg.WebApp;
    }
  } catch {
    // not in Telegram
  }
  return null;
};

// Mock haptic feedback for browser
const mockHapticFeedback: HapticFeedback = {
  impactOccurred: () => {},
  notificationOccurred: () => {},
  selectionChanged: () => {},
};

export function useTelegram(): UseTelegramReturn {
  const [webApp] = useState(() => {
    const app = getTelegramWebApp();
    if (app) {
      app.ready();
      app.expand();
    }
    return app;
  });
  const [user] = useState(() => webApp?.initDataUnsafe?.user ?? null);

  const showMainButton = useCallback((text: string, onClick: () => void) => {
    if (webApp) {
      webApp.MainButton.setText(text);
      webApp.MainButton.onClick(onClick);
      webApp.MainButton.show();
    }
  }, [webApp]);

  const hideMainButton = useCallback(() => {
    webApp?.MainButton.hide();
  }, [webApp]);

  const showBackButton = useCallback((onClick: () => void) => {
    if (webApp) {
      webApp.BackButton.onClick(onClick);
      webApp.BackButton.show();
    }
  }, [webApp]);

  const hideBackButton = useCallback(() => {
    webApp?.BackButton.hide();
  }, [webApp]);

  const hapticFeedback = useMemo(
    () => webApp?.HapticFeedback || mockHapticFeedback,
    [webApp]
  );

  return {
    webApp,
    user,
    isReady: true,
    isTelegram: !!webApp,
    colorScheme: webApp?.colorScheme || "light",
    themeParams: webApp?.themeParams || {},
    showMainButton,
    hideMainButton,
    showBackButton,
    hideBackButton,
    hapticFeedback,
    close: () => webApp?.close?.(),
    expand: () => webApp?.expand?.(),
  };
}
