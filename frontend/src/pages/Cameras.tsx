import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import { useAuth } from '../hooks/useAuth'
import type { Camera } from '../api/types'

export default function Cameras() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [cameras, setCameras] = useState<Camera[]>([])
  const [stats, setStats] = useState({ total: 0, online: 0, offline: 0 })

  useEffect(() => {
    if (!user) { navigate('/login'); return }
    api.get<Camera[]>('/cameras/').then(setCameras).catch(() => {})
    api.get<{ total: number; online: number; offline: number }>('/cameras/stats').then(setStats).catch(() => {})
  }, [user, navigate])

  const toggleStatus = async (cam: Camera) => {
    const newStatus = cam.status === 'online' ? 'offline' : 'online'
    await api.put<Camera>(`/cameras/${cam.id}`, { status: newStatus })
    setCameras(prev => prev.map(c => c.id === cam.id ? { ...c, status: newStatus } : c))
    setStats(prev => ({
      ...prev,
      online: prev.online + (newStatus === 'online' ? 1 : -1),
      offline: prev.offline + (newStatus === 'offline' ? 1 : -1),
    }))
  }

  return (
    <div className="cameras-page">
      <div className="dash-header">
        <h1>Camera Network</h1>
        <div className="header-stats">
          <span className="online">{stats.online} Online</span>
          <span className="offline">{stats.offline} Offline</span>
        </div>
      </div>

      <div className="camera-grid">
        {cameras.map(cam => (
          <div key={cam.id} className={`camera-card ${cam.status}`}>
            <div className="cam-feed">
              <div className={`cam-indicator ${cam.status}`} />
            </div>
            <div className="cam-info">
              <h3>{cam.name}</h3>
              <p className="cam-location">{cam.location || 'No location'}</p>
              <div className="cam-meta">
                <span className={`status-tag ${cam.status}`}>{cam.status}</span>
                {cam.latitude && cam.longitude && (
                  <span className="coords">{cam.latitude.toFixed(4)}, {cam.longitude.toFixed(4)}</span>
                )}
              </div>
              <button onClick={() => toggleStatus(cam)} className="btn-small">
                {cam.status === 'online' ? 'Disable' : 'Enable'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
