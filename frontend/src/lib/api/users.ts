import apiClient from "./client";
import type { User } from "../../types";

export interface UserProfile extends User {
  full_name: string;
  created_at: string;
}

export interface UpdateProfileData {
  phone?: string;
  language?: "uz" | "ru";
}

export async function getProfile(): Promise<UserProfile> {
  const { data } = await apiClient.get("/users/me/");
  return data;
}

export async function updateProfile(
  payload: UpdateProfileData
): Promise<UserProfile> {
  const { data } = await apiClient.patch("/users/me/update/", payload);
  return data;
}
