import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { productsApi } from '../api/products'
import { useAuth } from '../hooks/useAuth'
import { useCart } from '../hooks/useCart'
import type { Product } from '../api/types'

export default function ProductDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const { addItem } = useCart()
  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(true)
  const [quantity, setQuantity] = useState(1)
  const [added, setAdded] = useState(false)

  useEffect(() => {
    if (id) {
      productsApi.getById(Number(id))
        .then(setProduct)
        .catch(() => navigate('/products'))
        .finally(() => setLoading(false))
    }
  }, [id, navigate])

  const handleAddToCart = async () => {
    if (!user) {
      navigate('/login')
      return
    }
    try {
      await addItem(product!.id, quantity)
      setAdded(true)
      setTimeout(() => setAdded(false), 2000)
    } catch (err) {
      alert('Failed to add to cart')
    }
  }

  if (loading) return <p className="loading">Loading...</p>
  if (!product) return <p>Product not found</p>

  return (
    <div className="product-detail">
      <div className="detail-image" />
      <div className="detail-info">
        <h1>{product.name}</h1>
        <p className="detail-price">${product.price.toFixed(2)}</p>
        <p className="detail-description">{product.description || 'No description available.'}</p>
        <p className="detail-stock">In Stock: {product.stock}</p>
        <div className="quantity-control">
          <label>Quantity:</label>
          <input
            type="number"
            min="1"
            max={product.stock}
            value={quantity}
            onChange={(e) => setQuantity(Math.min(Number(e.target.value), product.stock))}
          />
        </div>
        <button onClick={handleAddToCart} className="btn-primary">
          {added ? 'Added!' : 'Add to Cart'}
        </button>
      </div>
    </div>
  )
}
