import { api } from './client';
import type { Order } from './types';

export const ordersApi = {
  getOrders: () => api.get<Order[]>('/orders/'),
  getById: (id: number) => api.get<Order>(`/orders/${id}`),
  create: (shippingAddress: string) =>
    api.post<Order>('/orders/', { shipping_address: shippingAddress }),
};
