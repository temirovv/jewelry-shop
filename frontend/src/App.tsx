import React, { useEffect } from "react";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { Sparkles } from "lucide-react";
import { HomePage } from "./pages/HomePage";
import { ProductDetailPage } from "./pages/ProductDetailPage";
import { CheckoutPage } from "./pages/CheckoutPage";
import { SearchPage } from "./pages/SearchPage";
import { FavoritesPage } from "./pages/FavoritesPage";
import { ProfilePage } from "./pages/ProfilePage";
import { useTelegram } from "./hooks/useTelegram";
import { useCartStore } from "./stores/cartStore";
import { useUserStore } from "./stores/userStore";
import { ToastContainer } from "./components/Toast";
import { springs } from "./lib/animations";
import "./index.css";

// Page wrapper with animation - faster, no exit delay
function PageWrapper({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.15, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="popLayout" initial={false}>
      <Routes location={location} key={location.pathname}>
        <Route
          path="/"
          element={
            <PageWrapper>
              <HomePage />
            </PageWrapper>
          }
        />
        <Route
          path="/product/:id"
          element={
            <PageWrapper>
              <ProductDetailPage />
            </PageWrapper>
          }
        />
        <Route
          path="/checkout"
          element={
            <PageWrapper>
              <CheckoutPage />
            </PageWrapper>
          }
        />
        <Route
          path="/search"
          element={
            <PageWrapper>
              <SearchPage />
            </PageWrapper>
          }
        />
        <Route
          path="/favorites"
          element={
            <PageWrapper>
              <FavoritesPage />
            </PageWrapper>
          }
        />
        <Route
          path="/profile"
          element={
            <PageWrapper>
              <ProfilePage />
            </PageWrapper>
          }
        />
      </Routes>
    </AnimatePresence>
  );
}

function AppContent() {
  const { colorScheme, themeParams, isReady } = useTelegram();
  const syncWithBackend = useCartStore((state) => state.syncWithBackend);
  const fetchProfile = useUserStore((state) => state.fetchProfile);

  useEffect(() => {
    if (colorScheme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [colorScheme]);

  // Ilova yuklanganda savatni va profil ma'lumotlarini backend bilan sinxronlash
  useEffect(() => {
    if (isReady) {
      syncWithBackend();
      fetchProfile();
    }
  }, [isReady, syncWithBackend, fetchProfile]);

  useEffect(() => {
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
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ ...springs.bouncy }}
          className="flex flex-col items-center gap-4"
        >
          <motion.div
            animate={{
              scale: [1, 1.1, 1],
              opacity: [0.5, 1, 0.5],
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              ease: "easeInOut",
            }}
            className="w-16 h-16 rounded-full gold-gradient flex items-center justify-center"
          >
            <Sparkles className="w-7 h-7 text-white" />
          </motion.div>
          <p className="text-muted-foreground text-sm">Yuklanmoqda...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <>
      <AnimatedRoutes />
      <ToastContainer />
    </>
  );
}

class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean; error: Error | null }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-background p-6">
          <div className="text-center space-y-4">
            <p className="text-lg font-semibold text-foreground">Xatolik yuz berdi</p>
            <p className="text-sm text-muted-foreground">{this.state.error?.message}</p>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm"
            >
              Qayta yuklash
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </ErrorBoundary>
  );
}

export default App;
