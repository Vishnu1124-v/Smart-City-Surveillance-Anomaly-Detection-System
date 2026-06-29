import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="home">
      <div className="hero">
        <h1>Welcome to Urbaneve</h1>
        <p>Discover the latest trends in fashion</p>
        <Link to="/products" className="btn-primary">Shop Now</Link>
      </div>
    </div>
  )
}
