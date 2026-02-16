import { type Variants, type Transition } from "framer-motion";

// Easing curves - more natural feeling
export const easings = {
  // Smooth and natural
  smooth: [0.4, 0, 0.2, 1],
  // Quick start, slow end (good for enter)
  easeOut: [0, 0, 0.2, 1],
  // Slow start, quick end (good for exit)
  easeIn: [0.4, 0, 1, 1],
  // Bouncy feel
  bounce: [0.68, -0.55, 0.265, 1.55],
  // Premium luxury feel
  luxury: [0.16, 1, 0.3, 1],
  // Spring-like
  spring: [0.43, 0.13, 0.23, 0.96],
} as const;

// Spring configurations
export const springs = {
  // Soft and gentle
  soft: { type: "spring", stiffness: 100, damping: 20 } as Transition,
  // Snappy response
  snappy: { type: "spring", stiffness: 400, damping: 30 } as Transition,
  // Bouncy
  bouncy: { type: "spring", stiffness: 300, damping: 15 } as Transition,
  // Smooth
  smooth: { type: "spring", stiffness: 200, damping: 25 } as Transition,
  // Quick
  quick: { type: "spring", stiffness: 500, damping: 35 } as Transition,
} as const;

// Durations
export const durations = {
  fast: 0.15,
  normal: 0.25,
  slow: 0.4,
  slower: 0.6,
} as const;

// Fade animations
export const fadeVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: durations.normal, ease: easings.smooth }
  },
  exit: {
    opacity: 0,
    transition: { duration: durations.fast, ease: easings.easeIn }
  },
};

// Slide up animations (for modals, sheets, toasts)
export const slideUpVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { ...springs.smooth }
  },
  exit: {
    opacity: 0,
    y: 10,
    transition: { duration: durations.fast, ease: easings.easeIn }
  },
};

// Slide down animations (for dropdowns)
export const slideDownVariants: Variants = {
  hidden: { opacity: 0, y: -10, scale: 0.95 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { ...springs.snappy }
  },
  exit: {
    opacity: 0,
    y: -5,
    scale: 0.98,
    transition: { duration: durations.fast }
  },
};

// Scale animations (for modals, cards)
export const scaleVariants: Variants = {
  hidden: { opacity: 0, scale: 0.9 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { ...springs.bouncy }
  },
  exit: {
    opacity: 0,
    scale: 0.95,
    transition: { duration: durations.fast }
  },
};

// Slide from left (for sidebars)
export const slideLeftVariants: Variants = {
  hidden: { x: "-100%" },
  visible: {
    x: 0,
    transition: { ...springs.smooth }
  },
  exit: {
    x: "-100%",
    transition: { ...springs.snappy }
  },
};

// Slide from right (for sheets)
export const slideRightVariants: Variants = {
  hidden: { x: "100%" },
  visible: {
    x: 0,
    transition: { ...springs.smooth }
  },
  exit: {
    x: "100%",
    transition: { ...springs.snappy }
  },
};

// Stagger children animations
export const staggerContainerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.06,
      delayChildren: 0.1,
    },
  },
  exit: {
    opacity: 0,
    transition: {
      staggerChildren: 0.03,
      staggerDirection: -1,
    },
  },
};

export const staggerItemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { ...springs.smooth }
  },
  exit: {
    opacity: 0,
    y: -10,
    transition: { duration: durations.fast }
  },
};

// Product card specific animation
export const productCardVariants: Variants = {
  hidden: { opacity: 0, y: 30, scale: 0.95 },
  visible: (i: number = 0) => ({
    opacity: 1,
    y: 0,
    scale: 1,
    transition: {
      delay: i * 0.05,
      ...springs.smooth,
    },
  }),
  exit: {
    opacity: 0,
    scale: 0.95,
    transition: { duration: durations.fast }
  },
  hover: {
    y: -4,
    transition: { ...springs.snappy }
  },
  tap: {
    scale: 0.98,
    transition: { duration: durations.fast }
  },
};

// Image hover effect
export const imageHoverVariants: Variants = {
  rest: { scale: 1 },
  hover: {
    scale: 1.05,
    transition: { duration: durations.slow, ease: easings.luxury }
  },
};

// Button press effect
export const buttonTapVariants: Variants = {
  rest: { scale: 1 },
  tap: {
    scale: 0.95,
    transition: { duration: durations.fast }
  },
};

// Page transition variants
export const pageVariants: Variants = {
  initial: { opacity: 0, y: 10 },
  enter: {
    opacity: 1,
    y: 0,
    transition: {
      duration: durations.normal,
      ease: easings.easeOut,
      when: "beforeChildren",
    }
  },
  exit: {
    opacity: 0,
    y: -10,
    transition: {
      duration: durations.fast,
      ease: easings.easeIn
    }
  },
};

// Bottom nav item
export const navItemVariants: Variants = {
  inactive: { scale: 1, y: 0 },
  active: {
    scale: 1.05,
    y: -2,
    transition: { ...springs.bouncy }
  },
};

// Toast animations
export const toastVariants: Variants = {
  hidden: { opacity: 0, y: -20, scale: 0.9 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { ...springs.bouncy }
  },
  exit: {
    opacity: 0,
    x: 100,
    scale: 0.9,
    transition: { duration: durations.normal, ease: easings.easeIn }
  },
};

// Skeleton pulse effect (use with CSS)
export const skeletonVariants: Variants = {
  pulse: {
    opacity: [0.5, 1, 0.5],
    transition: {
      duration: 1.5,
      repeat: Infinity,
      ease: "easeInOut",
    },
  },
};

// Badge pop animation
export const badgeVariants: Variants = {
  hidden: { opacity: 0, scale: 0 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { ...springs.bouncy }
  },
  exit: {
    opacity: 0,
    scale: 0,
    transition: { duration: durations.fast }
  },
};

// Heart like animation
export const heartVariants: Variants = {
  unliked: { scale: 1 },
  liked: {
    scale: [1, 1.3, 1],
    transition: {
      duration: 0.3,
      times: [0, 0.5, 1],
    }
  },
};

// Overlay/backdrop
export const overlayVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: durations.normal }
  },
  exit: {
    opacity: 0,
    transition: { duration: durations.fast, delay: 0.1 }
  },
};

// Modal content
export const modalVariants: Variants = {
  hidden: { opacity: 0, scale: 0.9, y: 20 },
  visible: {
    opacity: 1,
    scale: 1,
    y: 0,
    transition: { ...springs.smooth, delay: 0.05 }
  },
  exit: {
    opacity: 0,
    scale: 0.95,
    y: 10,
    transition: { duration: durations.fast }
  },
};

// List item remove animation
export const listItemVariants: Variants = {
  hidden: { opacity: 0, x: -20, height: 0 },
  visible: {
    opacity: 1,
    x: 0,
    height: "auto",
    transition: { ...springs.smooth }
  },
  exit: {
    opacity: 0,
    x: 20,
    height: 0,
    transition: { duration: durations.normal }
  },
};

// Scroll reveal animation
export const scrollRevealVariants: Variants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { ...springs.smooth }
  },
};

// Tap feedback for all interactive elements
export const tapFeedback = {
  whileTap: { scale: 0.97 },
  transition: { duration: durations.fast },
};

// Hover lift effect
export const hoverLift = {
  whileHover: { y: -2 },
  transition: { ...springs.snappy },
};
