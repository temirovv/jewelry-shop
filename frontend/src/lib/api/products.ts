import apiClient from "./client";
import type { Product, Category, PaginatedResponse } from "../../types";

export interface ProductFilters {
  category?: string;
  metal_type?: string;
  min_price?: number;
  max_price?: number;
  search?: string;
  ordering?: string;
}

export async function getProducts(
  filters?: ProductFilters
): Promise<PaginatedResponse<Product>> {
  const params = new URLSearchParams();

  if (filters) {
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== "") {
        params.append(key, String(value));
      }
    });
  }

  const response = await apiClient.get<PaginatedResponse<Product>>(
    `/products/?${params.toString()}`
  );
  return response.data;
}

export async function getProduct(id: number): Promise<Product> {
  const response = await apiClient.get<Product>(`/products/${id}/`);
  return response.data;
}

export async function getFeaturedProducts(): Promise<Product[]> {
  const response = await apiClient.get<PaginatedResponse<Product>>(
    "/products/?is_featured=true"
  );
  return response.data.results;
}

export async function getCategories(): Promise<Category[]> {
  const response = await apiClient.get<Category[]>("/categories/");
  return response.data;
}

export async function getNewArrivals(): Promise<Product[]> {
  const response = await apiClient.get<Product[]>("/products/new_arrivals/");
  return response.data;
}

export async function getProductsByCategory(
  categorySlug: string
): Promise<PaginatedResponse<Product>> {
  const response = await apiClient.get<PaginatedResponse<Product>>(
    `/products/?category=${categorySlug}`
  );
  return response.data;
}
