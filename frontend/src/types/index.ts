export interface Banner {
  id: number;
  title: string;
  subtitle: string;
  emoji: string;
  gradient: string;
  link?: string;
  image?: string;
}

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  old_price?: number;
  images: ProductImage[];
  category: Category;
  metal_type: MetalType;
  weight: number;
  size?: string;
  in_stock: boolean;
  is_featured: boolean;
  created_at: string;
}

export interface ProductImage {
  id: number;
  image: string;
  is_main: boolean;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  icon?: string;
  image?: string;
}

export type MetalType = "gold" | "silver" | "platinum" | "white_gold";

export interface CartItem {
  id: number;
  product: Product;
  quantity: number;
  size?: string;
}

export interface Cart {
  items: CartItem[];
  total: number;
  items_count: number;
}

export interface User {
  id: number;
  telegram_id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  phone?: string;
  language: "uz" | "ru";
}

export type PaymentMethod = "cash" | "transfer";

export interface Order {
  id: number;
  user: User;
  items: OrderItem[];
  total: number;
  status: OrderStatus;
  delivery_address?: string;
  phone: string;
  comment?: string;
  payment_method: PaymentMethod;
  payment_method_display: string;
  is_paid: boolean;
  created_at: string;
}

export interface OrderItem {
  id: number;
  product: Product;
  quantity: number;
  price: number;
  size?: string;
}

export type OrderStatus =
  | "pending"
  | "confirmed"
  | "processing"
  | "shipped"
  | "delivered"
  | "cancelled";

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
