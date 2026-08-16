import axios from 'axios'

const ACCESS_KEY = 'escaque.access'
const REFRESH_KEY = 'escaque.refresh'

export const tokens = {
  get access() {
    return localStorage.getItem(ACCESS_KEY)
  },
  get refresh() {
    return localStorage.getItem(REFRESH_KEY)
  },
  set({ access, refresh }) {
    if (access) localStorage.setItem(ACCESS_KEY, access)
    if (refresh) localStorage.setItem(REFRESH_KEY, refresh)
  },
  clear() {
    localStorage.removeItem(ACCESS_KEY)
    localStorage.removeItem(REFRESH_KEY)
  },
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api',
  timeout: 20000,
})

api.interceptors.request.use((config) => {
  const token = tokens.access
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// A single refresh in flight, shared by every request that hits a 401 at once.
let refreshing = null

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    const status = error.response?.status
    const isRefreshCall = original?.url?.includes('auth/token/refresh')

    if (status !== 401 || original?._retried || isRefreshCall || !tokens.refresh) {
      return Promise.reject(error)
    }

    original._retried = true
    refreshing =
      refreshing ||
      api
        .post('auth/token/refresh/', { refresh: tokens.refresh })
        .then(({ data }) => {
          tokens.set({ access: data.access, refresh: data.refresh })
          return data.access
        })
        .catch((refreshError) => {
          tokens.clear()
          window.dispatchEvent(new CustomEvent('escaque:signed-out'))
          throw refreshError
        })
        .finally(() => {
          refreshing = null
        })

    const access = await refreshing
    original.headers.Authorization = `Bearer ${access}`
    return api(original)
  },
)

/** Turn an axios failure into a sentence a person can act on. */
export function errorMessage(error, fallback = 'No se ha podido completar la acción.') {
  const data = error?.response?.data
  if (!data) {
    return error?.code === 'ECONNABORTED'
      ? 'El servidor ha tardado demasiado en responder.'
      : 'No hay conexión con el servidor.'
  }
  if (typeof data === 'string') return data
  if (data.detail) return data.detail
  const first = Object.values(data)[0]
  if (Array.isArray(first)) return first[0]
  if (typeof first === 'string') return first
  return fallback
}
