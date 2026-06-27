import apiClient from "./client";
import type { Brand } from "../../types";

export async function getBrands(): Promise<Brand[]> {
  const response = await apiClient.get<Brand[]>("/brands/");
  return response.data;
}

export async function getFeaturedBrands(): Promise<Brand[]> {
  const response = await apiClient.get<Brand[]>("/brands/featured/");
  return response.data;
}

export async function getBrand(slug: string): Promise<Brand> {
  const response = await apiClient.get<Brand>(`/brands/${slug}/`);
  return response.data;
}
