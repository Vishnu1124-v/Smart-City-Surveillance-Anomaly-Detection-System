const BASE = '/api';

async function request<T>(endpoint: string, opts?: RequestInit): Promise<T> {
  const token = localStorage.getItem('token');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(opts?.headers as Record<string, string>),
  };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${BASE}${endpoint}`, { ...opts, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

export const api = {
  get: <T>(e: string) => request<T>(e),
  post: <T>(e: string, d?: unknown) => request<T>(e, { method: 'POST', body: JSON.stringify(d) }),
  put: <T>(e: string, d?: unknown) => request<T>(e, { method: 'PUT', body: JSON.stringify(d) }),
  delete: <T>(e: string) => request<T>(e, { method: 'DELETE' }),
};
