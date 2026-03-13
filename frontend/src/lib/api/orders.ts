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

export interface OrdersResponse {
  orders: Order[];
  next: string | null;
}

export async function createOrder(data: CreateOrderData): Promise<Order> {
  const response = await apiClient.post<Order>("/orders/", data);
  return response.data;
}

export async function getOrders(): Promise<OrdersResponse> {
  const response = await apiClient.get("/orders/");
  const data = response.data;
  if (Array.isArray(data)) {
    return { orders: data, next: null };
  }
  return { orders: data.results || [], next: data.next || null };
}

export async function getOrdersByUrl(url: string): Promise<OrdersResponse> {
  const response = await apiClient.get(url);
  const data = response.data;
  if (Array.isArray(data)) {
    return { orders: data, next: null };
  }
  return { orders: data.results || [], next: data.next || null };
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
