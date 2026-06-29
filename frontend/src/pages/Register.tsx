import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function Register() {
  const [form, setForm] = useState({ email: '', username: '', password: '', full_name: '' })
  const [error, setError] = useState('')
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await register(form)
      navigate('/')
    } catch (err) {
      setError('Registration failed. Try again.')
    }
  }

  const updateField = (field: string) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm({ ...form, [field]: e.target.value })

  return (
    <div className="auth-page">
      <div className="auth-form">
        <h1>Register</h1>
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Full Name" value={form.full_name} onChange={updateField('full_name')} />
          <input type="email" placeholder="Email" value={form.email} onChange={updateField('email')} required />
          <input type="text" placeholder="Username" value={form.username} onChange={updateField('username')} required />
          <input type="password" placeholder="Password" value={form.password} onChange={updateField('password')} required />
          <button type="submit" className="btn-primary">Register</button>
        </form>
        <p>Already have an account? <Link to="/login">Login</Link></p>
      </div>
    </div>
  )
}
