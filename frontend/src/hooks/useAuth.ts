import { useState, useEffect, useCallback } from 'react'
import { authApi } from '../api/auth'
import type { User } from '../api/types'

export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      authApi.getProfile()
        .then(setUser)
        .catch(() => localStorage.removeItem('token'))
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const login = useCallback(async (username: string, password: string) => {
    const res = await authApi.login(username, password)
    localStorage.setItem('token', res.access_token)
    const profile = await authApi.getProfile()
    setUser(profile)
    return profile
  }, [])

  const register = useCallback(async (data: { email: string; username: string; password: string; full_name?: string }) => {
    const res = await authApi.register(data)
    localStorage.setItem('token', res.access_token)
    const profile = await authApi.getProfile()
    setUser(profile)
    return profile
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('token')
    setUser(null)
  }, [])

  return { user, loading, login, register, logout }
}
