import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import { useAuth } from '../hooks/useAuth'
import type { Alert } from '../api/types'

export default function Alerts() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [filter, setFilter] = useState('')
  const [stats, setStats] = useState({ total: 0, open: 0, high_severity: 0 })

  useEffect(() => {
    if (!user) { navigate('/login'); return }
    fetchAlerts()
    api.get<{ total: number; open: number; high_severity: number }>('/alerts/stats').then(setStats).catch(() => {})
  }, [user, navigate])

  const fetchAlerts = async (status?: string) => {
    const params = status ? `?status=${status}` : ''
    api.get<Alert[]>(`/alerts/${params}`).then(setAlerts).catch(() => {})
  }

  const resolveAlert = async (id: number) => {
    await api.put<Alert>(`/alerts/${id}`, { status: 'resolved' })
    setAlerts(prev => prev.map(a => a.id === id ? { ...a, status: 'resolved' } : a))
  }

  return (
    <div className="alerts-page">
      <div className="dash-header">
        <h1>Anomaly Alerts</h1>
        <div className="header-stats">
          <span className="high">{stats.high_severity} High</span>
          <span>{stats.open} Open</span>
          <span>{stats.total} Total</span>
        </div>
      </div>

      <div className="filter-bar">
        <button className={`filter-btn ${filter === '' ? 'active' : ''}`} onClick={() => { setFilter(''); fetchAlerts() }}>All</button>
        <button className={`filter-btn ${filter === 'open' ? 'active' : ''}`} onClick={() => { setFilter('open'); fetchAlerts('open') }}>Open</button>
        <button className={`filter-btn ${filter === 'resolved' ? 'active' : ''}`} onClick={() => { setFilter('resolved'); fetchAlerts('resolved') }}>Resolved</button>
      </div>

      <div className="alerts-list">
        {alerts.length === 0 ? (
          <p className="no-data">No alerts found</p>
        ) : (
          alerts.map(alert => (
            <div key={alert.id} className={`alert-card ${alert.severity}`}>
              <div className="alert-head">
                <span className={`badge badge-${alert.severity}`}>{alert.severity}</span>
                <span className={`badge badge-status`}>{alert.status}</span>
                <span className="alert-type">{alert.anomaly_type?.replace(/_/g, ' ')}</span>
              </div>
              <h3>{alert.title}</h3>
              <p>{alert.description}</p>
              <div className="alert-meta">
                <span>Camera: {alert.camera?.name || 'Unknown'}</span>
                <span>Confidence: {(alert.confidence * 100).toFixed(0)}%</span>
                <span>{new Date(alert.created_at).toLocaleString()}</span>
              </div>
              {alert.status === 'open' && (
                <button onClick={() => resolveAlert(alert.id)} className="btn-small resolve">
                  Mark Resolved
                </button>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}
