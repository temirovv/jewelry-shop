import apiClient from "./client";
import type { Product } from "../../types";

export interface FavoriteRecord {
  id: number;
  product: Product;
  created_at: string;
}

export interface ToggleFavoriteResponse {
  is_favorite: boolean;
  product_id: number;
}

export async function getFavorites(): Promise<FavoriteRecord[]> {
  const { data } = await apiClient.get("/users/favorites/");
  return Array.isArray(data) ? data : data.results || [];
}

export async function toggleFavorite(
  productId: number,
): Promise<ToggleFavoriteResponse> {
  const { data } = await apiClient.post("/users/favorites/toggle/", {
    product_id: productId,
  });
  return data;
}

export async function clearFavoritesApi(): Promise<void> {
  await apiClient.delete("/users/favorites/clear/");
}
