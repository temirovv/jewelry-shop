import apiClient from "./client";
import type { Cart } from "../../types";

export async function getCart(): Promise<Cart> {
  const { data } = await apiClient.get("/cart/");
  return data;
}

export async function addToCart(
  productId: number,
  quantity: number = 1,
  size: string = ""
): Promise<Cart> {
  const { data } = await apiClient.post("/cart/add/", {
    product_id: productId,
    quantity,
    size,
  });
  return data;
}

export async function updateCartItem(
  itemId: number,
  quantity: number
): Promise<Cart> {
  const { data } = await apiClient.patch(`/cart/items/${itemId}/`, {
    quantity,
  });
  return data;
}

export async function removeCartItem(itemId: number): Promise<Cart> {
  const { data } = await apiClient.delete(`/cart/items/${itemId}/remove/`);
  return data;
}

export async function clearCartApi(): Promise<Cart> {
  const { data } = await apiClient.delete("/cart/clear/");
  return data;
}
