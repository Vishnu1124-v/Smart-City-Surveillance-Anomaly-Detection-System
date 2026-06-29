import { Outlet, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function Layout() {
  const { user, logout } = useAuth()

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="nav-container">
          <Link to="/" className="nav-brand">Urbaneve</Link>
          <div className="nav-links">
            <Link to="/products">Shop</Link>
            <Link to="/cart">Cart</Link>
            {user ? (
              <>
                <Link to="/orders">Orders</Link>
                <span className="nav-user">{user.username}</span>
                <button onClick={logout} className="nav-btn">Logout</button>
              </>
            ) : (
              <>
                <Link to="/login">Login</Link>
                <Link to="/register">Register</Link>
              </>
            )}
          </div>
        </div>
      </nav>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}
