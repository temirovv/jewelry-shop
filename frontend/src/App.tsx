import React, { Suspense, useEffect, useSyncExternalStore } from "react";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { Sparkles, Loader2 } from "lucide-react";
import { HomePage } from "./pages/HomePage";
import { useTelegram } from "./hooks/useTelegram";
import { useCartStore } from "./stores/cartStore";
import { useUserStore } from "./stores/userStore";
import { ToastContainer } from "./components/Toast";
import { OfflineBanner } from "./components/OfflineBanner";
import { springs, pageSlideForward, pageSlideBack, pageVariants } from "./lib/animations";
import "./index.css";

// Lazy-loaded pages
const ProductDetailPage = React.lazy(() =>
  import("./pages/ProductDetailPage").then((m) => ({ default: m.ProductDetailPage }))
);
const CheckoutPage = React.lazy(() =>
  import("./pages/CheckoutPage").then((m) => ({ default: m.CheckoutPage }))
);
const SearchPage = React.lazy(() =>
  import("./pages/SearchPage").then((m) => ({ default: m.SearchPage }))
);
const FavoritesPage = React.lazy(() =>
  import("./pages/FavoritesPage").then((m) => ({ default: m.FavoritesPage }))
);
const ProfilePage = React.lazy(() =>
  import("./pages/ProfilePage").then((m) => ({ default: m.ProfilePage }))
);

function LazyFallback() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <Loader2 className="w-6 h-6 animate-spin text-primary" />
    </div>
  );
}

// Route depth for directional transitions
function getRouteDepth(pathname: string): number {
  if (pathname === "/") return 0;
  if (/^\/(search|favorites|profile)$/.test(pathname)) return 1;
  if (/^\/product\//.test(pathname)) return 2;
  if (pathname === "/checkout") return 3;
  return 1;
}

// Page wrapper with directional slide
function PageWrapper({
  children,
  direction,
}: {
  children: React.ReactNode;
  direction: "forward" | "back" | "same";
}) {
  const variants =
    direction === "forward"
      ? pageSlideForward
      : direction === "back"
        ? pageSlideBack
        : pageVariants;

  return (
    <motion.div
      variants={variants}
      initial="initial"
      animate="enter"
      exit="exit"
    >
      {children}
    </motion.div>
  );
}

// External store for navigation direction
const navDirectionStore = {
  _prevDepth: 0,
  _direction: "same" as "forward" | "back" | "same",
  _listeners: new Set<() => void>(),
  update(pathname: string) {
    const currentDepth = getRouteDepth(pathname);
    const newDir =
      currentDepth > this._prevDepth
        ? "forward" as const
        : currentDepth < this._prevDepth
          ? "back" as const
          : "same" as const;
    this._prevDepth = currentDepth;
    if (newDir !== this._direction) {
      this._direction = newDir;
      this._listeners.forEach((l) => l());
    }
  },
  subscribe(listener: () => void) {
    navDirectionStore._listeners.add(listener);
    return () => { navDirectionStore._listeners.delete(listener); };
  },
  getSnapshot() {
    return navDirectionStore._direction;
  },
};

function AnimatedRoutes() {
  const location = useLocation();
  const direction = useSyncExternalStore(
    navDirectionStore.subscribe,
    navDirectionStore.getSnapshot,
  );

  useEffect(() => {
    navDirectionStore.update(location.pathname);
  }, [location.pathname]);

  return (
    <AnimatePresence mode="wait" initial={false}>
      <Routes location={location} key={location.pathname}>
        <Route
          path="/"
          element={
            <PageWrapper direction={direction}>
              <HomePage />
            </PageWrapper>
          }
        />
        <Route
          path="/product/:id"
          element={
            <PageWrapper direction={direction}>
              <Suspense fallback={<LazyFallback />}>
                <ProductDetailPage />
              </Suspense>
            </PageWrapper>
          }
        />
        <Route
          path="/checkout"
          element={
            <PageWrapper direction={direction}>
              <Suspense fallback={<LazyFallback />}>
                <CheckoutPage />
              </Suspense>
            </PageWrapper>
          }
        />
        <Route
          path="/search"
          element={
            <PageWrapper direction={direction}>
              <Suspense fallback={<LazyFallback />}>
                <SearchPage />
              </Suspense>
            </PageWrapper>
          }
        />
        <Route
          path="/favorites"
          element={
            <PageWrapper direction={direction}>
              <Suspense fallback={<LazyFallback />}>
                <FavoritesPage />
              </Suspense>
            </PageWrapper>
          }
        />
        <Route
          path="/profile"
          element={
            <PageWrapper direction={direction}>
              <Suspense fallback={<LazyFallback />}>
                <ProfilePage />
              </Suspense>
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
      <OfflineBanner />
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
