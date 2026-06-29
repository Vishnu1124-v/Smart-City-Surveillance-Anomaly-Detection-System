import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { ordersApi } from '../api/orders'
import { useAuth } from '../hooks/useAuth'
import type { Order } from '../api/types'

export default function Orders() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [orders, setOrders] = useState<Order[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!user) {
      navigate('/login')
      return
    }
    ordersApi.getOrders()
      .then(setOrders)
      .catch(() => setOrders([]))
      .finally(() => setLoading(false))
  }, [user, navigate])

  if (loading) return <p className="loading">Loading...</p>

  return (
    <div className="orders-page">
      <h1>My Orders</h1>
      {orders.length === 0 ? (
        <p>No orders yet</p>
      ) : (
        <div className="orders-list">
          {orders.map((order) => (
            <div key={order.id} className="order-card">
              <div className="order-header">
                <span>Order #{order.id}</span>
                <span className={`order-status ${order.status}`}>{order.status}</span>
                <span>{new Date(order.created_at).toLocaleDateString()}</span>
              </div>
              <div className="order-items">
                {order.items.map((item) => (
                  <div key={item.id} className="order-item">
                    <span>{item.product.name} x{item.quantity}</span>
                    <span>${(item.price * item.quantity).toFixed(2)}</span>
                  </div>
                ))}
              </div>
              <div className="order-total">
                <strong>Total: ${order.total.toFixed(2)}</strong>
              </div>
              <div className="order-address">
                <small>Shipping: {order.shipping_address}</small>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
