import apiClient from "./client";
import type { Order, CartItem, PaymentMethod } from "../../types";

export interface CreateOrderData {
  items: {
    product_id: number;
    quantity: number;
    size?: string;
  }[];
  phone: string;
  delivery_address?: string;
  comment?: string;
  payment_method: PaymentMethod;
}

export async function createOrder(data: CreateOrderData): Promise<Order> {
  const response = await apiClient.post<Order>("/orders/", data);
  return response.data;
}

export async function getOrders(): Promise<Order[]> {
  const response = await apiClient.get("/orders/");
  const data = response.data;
  return Array.isArray(data) ? data : data.results || [];
}

export async function getOrder(id: number): Promise<Order> {
  const response = await apiClient.get<Order>(`/orders/${id}/`);
  return response.data;
}

export function prepareOrderItems(cartItems: CartItem[]) {
  return cartItems.map((item) => ({
    product_id: item.product.id,
    quantity: item.quantity,
    size: item.size,
  }));
}
