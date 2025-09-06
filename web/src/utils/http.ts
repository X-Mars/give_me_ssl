interface ApiResponse<T> { code: number; message: string; data: T }
interface LoginPayload { access: string; refresh: string; user: { id: number; username: string; email: string } }

const API_BASE = import.meta.env.VITE_API_BASE_URL as string

function getAccess() { return localStorage.getItem('access_token') }
function getRefresh() { return localStorage.getItem('refresh_token') }
function setTokens(access: string, refresh?: string) {
  localStorage.setItem('access_token', access)
  if (refresh) localStorage.setItem('refresh_token', refresh)
}
export function clearTokens() {
  localStorage.removeItem('access_token'); localStorage.removeItem('refresh_token')
}

async function rawFetch(path: string, options: RequestInit) {
  return fetch(`${API_BASE}${path}`, options)
}

export async function apiFetch<T>(path: string, options: RequestInit = {}, retry = true): Promise<ApiResponse<T>> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json', ...(options.headers as Record<string, string> | undefined) }
  const token = getAccess()
  if (token) headers['Authorization'] = `Bearer ${token}`
  const res = await rawFetch(path, { ...options, headers })
  if (res.status === 401 && retry && getRefresh()) {
    const refreshed = await refreshToken()
    if (refreshed) return apiFetch<T>(path, options, false)
  }
  return res.json()
}

export async function login(username: string, password: string) {
  const res = await apiFetch<LoginPayload>('/auth/login/', {
    method: 'POST',
    body: JSON.stringify({ username, password })
  })
  if (res.code === 0) setTokens(res.data.access, res.data.refresh)
  return res
}

export async function refreshToken(): Promise<boolean> {
  const refresh = getRefresh()
  if (!refresh) return false
  const res = await rawFetch('/auth/refresh/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ refresh }) })
  if (!res.ok) { clearTokens(); return false }
  const data = await res.json() as ApiResponse<{ access: string }>
  if (data.code === 0 && data.data?.access) { setTokens(data.data.access); return true }
  clearTokens();
  return false
}

export async function getMe() { return apiFetch<{ id:number; username:string; email:string }>('/auth/me/') }
