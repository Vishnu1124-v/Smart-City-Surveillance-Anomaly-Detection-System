export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string | null;
  is_admin: boolean;
  created_at: string;
}

export interface Category {
  id: number;
  name: string;
  description: string | null;
  image_url: string | null;
}

export interface Product {
  id: number;
  name: string;
  description: string | null;
  price: number;
  stock: number;
  image_url: string | null;
  category_id: number | null;
  created_at: string;
}

export interface CartItem {
  id: number;
  user_id: number;
  product_id: number;
  quantity: number;
  product: Product;
}

export interface OrderItem {
  id: number;
  product_id: number;
  quantity: number;
  price: number;
  product: Product;
}

export interface Order {
  id: number;
  user_id: number;
  status: string;
  total: number;
  shipping_address: string | null;
  created_at: string;
  items: OrderItem[];
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}
