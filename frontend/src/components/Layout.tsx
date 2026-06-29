import { Outlet, Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="nav-container">
          <Link to="/" className="nav-brand">UrbanEye</Link>
          {user && (
            <div className="nav-links">
              <Link to="/">Dashboard</Link>
              <Link to="/cameras">Cameras</Link>
              <Link to="/alerts">Alerts</Link>
              <span className="nav-user">{user.username}</span>
              <button onClick={handleLogout} className="nav-btn">Logout</button>
            </div>
          )}
        </div>
      </nav>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}
