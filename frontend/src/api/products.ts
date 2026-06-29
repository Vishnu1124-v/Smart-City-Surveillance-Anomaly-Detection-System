import { api } from './client';
import type { Product, Category } from './types';

export const productsApi = {
  getAll: (categoryId?: number) => {
    const params = categoryId ? `?category_id=${categoryId}` : '';
    return api.get<Product[]>(`/products/${params}`);
  },
  getById: (id: number) => api.get<Product>(`/products/${id}`),
};

export const categoriesApi = {
  getAll: () => api.get<Category[]>('/categories/'),
};
