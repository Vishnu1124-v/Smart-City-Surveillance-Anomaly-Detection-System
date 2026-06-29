import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import { useAuth } from '../hooks/useAuth'
import type { DashboardData } from '../api/types'

export default function Dashboard() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [data, setData] = useState<DashboardData | null>(null)
  const [scanning, setScanning] = useState(false)

  useEffect(() => {
    if (!user) { navigate('/login'); return }
    api.get<DashboardData>('/dashboard/').then(setData).catch(() => {})
  }, [user, navigate])

  const handleScan = async () => {
    setScanning(true)
    try {
      await api.post<{ alerts_detected: number }>('/alerts/scan')
      const fresh = await api.get<DashboardData>('/dashboard/')
      setData(fresh)
    } catch {}
    setScanning(false)
  }

  if (!data) return <p className="loading">Loading dashboard...</p>

  return (
    <div className="dashboard">
      <div className="dash-header">
        <h1>Control Center</h1>
        <button onClick={handleScan} disabled={scanning} className="btn-primary">
          {scanning ? 'Scanning...' : 'Run Anomaly Scan'}
        </button>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>{data.cameras.total}</h3>
          <p>Total Cameras</p>
          <div className="stat-sub">
            <span className="online">{data.cameras.online} online</span>
            <span className="offline">{data.cameras.offline} offline</span>
          </div>
        </div>
        <div className="stat-card">
          <h3>{data.alerts.open}</h3>
          <p>Open Alerts</p>
          <div className="stat-sub">
            <span>{data.alerts.total} total</span>
            <span className="high">{data.alerts.high_severity} high</span>
          </div>
        </div>
        <div className="stat-card">
          <h3>{data.cameras.online}</h3>
          <p>Cameras Online</p>
          <div className="stat-sub">
            <span>{Math.round((data.cameras.online / Math.max(data.cameras.total, 1)) * 100)}% uptime</span>
          </div>
        </div>
      </div>

      <div className="section">
        <h2>Recent Alerts</h2>
        <div className="alert-feed">
          {data.recent_alerts.length === 0 ? (
            <p className="no-data">No recent alerts</p>
          ) : (
            data.recent_alerts.map(a => (
              <div key={a.id} className={`alert-item ${a.severity}`}>
                <span className={`badge badge-${a.severity}`}>{a.severity}</span>
                <span className="alert-title">{a.title}</span>
                <span className="alert-camera">{a.camera_name}</span>
                <span className="alert-time">{new Date(a.created_at).toLocaleString()}</span>
              </div>
            ))
          )}
        </div>
      </div>

      <div className="section">
        <h2>Quick Actions</h2>
        <div className="quick-actions">
          <button onClick={() => navigate('/cameras')} className="action-btn">Manage Cameras</button>
          <button onClick={() => navigate('/alerts')} className="action-btn">View All Alerts</button>
        </div>
      </div>
    </div>
  )
}
