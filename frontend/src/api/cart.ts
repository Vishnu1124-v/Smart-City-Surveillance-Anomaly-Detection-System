import { api } from './client';
import type { CartItem } from './types';

export const cartApi = {
  getCart: () => api.get<CartItem[]>('/cart/'),
  addItem: (productId: number, quantity: number = 1) =>
    api.post<CartItem>('/cart/', { product_id: productId, quantity }),
  updateItem: (itemId: number, quantity: number) =>
    api.put<CartItem>(`/cart/${itemId}`, { quantity }),
  removeItem: (itemId: number) => api.delete(`/cart/${itemId}`),
};
