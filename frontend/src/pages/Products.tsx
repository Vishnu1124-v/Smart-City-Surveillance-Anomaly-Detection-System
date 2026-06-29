import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { productsApi, categoriesApi } from '../api/products'
import type { Product, Category } from '../api/types'

export default function Products() {
  const [products, setProducts] = useState<Product[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [selectedCategory, setSelectedCategory] = useState<number | undefined>()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    categoriesApi.getAll().then(setCategories).catch(() => {})
  }, [])

  useEffect(() => {
    setLoading(true)
    productsApi.getAll(selectedCategory)
      .then(setProducts)
      .catch(() => setProducts([]))
      .finally(() => setLoading(false))
  }, [selectedCategory])

  return (
    <div className="products-page">
      <h1>Our Collection</h1>
      <div className="category-filters">
        <button
          className={`filter-btn ${!selectedCategory ? 'active' : ''}`}
          onClick={() => setSelectedCategory(undefined)}
        >
          All
        </button>
        {categories.map((cat) => (
          <button
            key={cat.id}
            className={`filter-btn ${selectedCategory === cat.id ? 'active' : ''}`}
            onClick={() => setSelectedCategory(cat.id)}
          >
            {cat.name}
          </button>
        ))}
      </div>
      {loading ? (
        <p className="loading">Loading...</p>
      ) : (
        <div className="product-grid">
          {products.map((product) => (
            <Link to={`/products/${product.id}`} key={product.id} className="product-card">
              <div className="product-image" />
              <div className="product-info">
                <h3>{product.name}</h3>
                <p className="product-price">${product.price.toFixed(2)}</p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
