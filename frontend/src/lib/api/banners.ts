import apiClient from "./client";
import type { Banner } from "../../types";

export async function getBanners(): Promise<Banner[]> {
  const response = await apiClient.get<Banner[]>("/banners/");
  return response.data;
}
