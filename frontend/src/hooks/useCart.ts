import { useState, useEffect, useCallback } from 'react'
import { cartApi } from '../api/cart'
import type { CartItem } from '../api/types'

export function useCart() {
  const [items, setItems] = useState<CartItem[]>([])
  const [loading, setLoading] = useState(false)

  const fetchCart = useCallback(async () => {
    try {
      setLoading(true)
      const data = await cartApi.getCart()
      setItems(data)
    } catch {
      setItems([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (localStorage.getItem('token')) {
      fetchCart()
    }
  }, [fetchCart])

  const addItem = useCallback(async (productId: number, quantity = 1) => {
    await cartApi.addItem(productId, quantity)
    await fetchCart()
  }, [fetchCart])

  const updateItem = useCallback(async (itemId: number, quantity: number) => {
    await cartApi.updateItem(itemId, quantity)
    await fetchCart()
  }, [fetchCart])

  const removeItem = useCallback(async (itemId: number) => {
    await cartApi.removeItem(itemId)
    await fetchCart()
  }, [fetchCart])

  const total = items.reduce((sum, item) => sum + item.product.price * item.quantity, 0)

  return { items, loading, total, addItem, updateItem, removeItem, fetchCart }
}
