import { create } from "zustand";
import { getProfile, updateProfile } from "../lib/api/users";
import type { UserProfile, UpdateProfileData } from "../lib/api/users";

interface UserState {
  profile: UserProfile | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchProfile: () => Promise<void>;
  saveProfile: (data: UpdateProfileData) => Promise<UserProfile>;
  reset: () => void;
}

export const useUserStore = create<UserState>((set, get) => ({
  profile: null,
  isLoading: false,
  error: null,

  fetchProfile: async () => {
    if (get().isLoading) return;
    set({ isLoading: true, error: null });
    try {
      const profile = await getProfile();
      set({ profile, isLoading: false });
    } catch {
      set({ isLoading: false, error: "Profil yuklanmadi" });
    }
  },

  saveProfile: async (data: UpdateProfileData) => {
    const updated = await updateProfile(data);
    set({ profile: updated });
    return updated;
  },

  reset: () => set({ profile: null, isLoading: false, error: null }),
}));
