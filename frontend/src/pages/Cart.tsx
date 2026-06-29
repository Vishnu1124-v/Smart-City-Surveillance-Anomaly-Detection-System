import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { useCart } from '../hooks/useCart'
import { ordersApi } from '../api/orders'

export default function Cart() {
  const { user } = useAuth()
  const { items, loading, total, updateItem, removeItem, fetchCart } = useCart()
  const navigate = useNavigate()
  const [address, setAddress] = useState('')
  const [checkingOut, setCheckingOut] = useState(false)

  if (!user) {
    navigate('/login')
    return null
  }

  if (loading) return <p className="loading">Loading...</p>

  const handleCheckout = async () => {
    if (!address.trim()) {
      alert('Please enter a shipping address')
      return
    }
    try {
      setCheckingOut(true)
      await ordersApi.create(address)
      await fetchCart()
      navigate('/orders')
    } catch (err) {
      alert('Checkout failed')
    } finally {
      setCheckingOut(false)
    }
  }

  return (
    <div className="cart-page">
      <h1>Shopping Cart</h1>
      {items.length === 0 ? (
        <p>Your cart is empty</p>
      ) : (
        <>
          <div className="cart-items">
            {items.map((item) => (
              <div key={item.id} className="cart-item">
                <div className="cart-item-image" />
                <div className="cart-item-info">
                  <h3>{item.product.name}</h3>
                  <p>${item.product.price.toFixed(2)}</p>
                </div>
                <div className="cart-item-qty">
                  <input
                    type="number"
                    min="1"
                    value={item.quantity}
                    onChange={(e) => updateItem(item.id, Number(e.target.value))}
                  />
                </div>
                <div className="cart-item-total">
                  ${(item.product.price * item.quantity).toFixed(2)}
                </div>
                <button onClick={() => removeItem(item.id)} className="btn-remove">Remove</button>
              </div>
            ))}
          </div>
          <div className="cart-summary">
            <h2>Total: ${total.toFixed(2)}</h2>
            <div className="checkout-section">
              <input
                type="text"
                placeholder="Shipping Address"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                className="address-input"
              />
              <button onClick={handleCheckout} disabled={checkingOut} className="btn-primary">
                {checkingOut ? 'Processing...' : 'Checkout'}
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
