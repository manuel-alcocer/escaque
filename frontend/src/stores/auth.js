import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

import { api, errorMessage, tokens } from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loading = ref(false)
  const error = ref('')

  const isSignedIn = computed(() => Boolean(user.value))
  const name = computed(() => user.value?.name || '')

  async function signIn(username, password) {
    loading.value = true
    error.value = ''
    try {
      const { data } = await api.post('auth/token/', { username, password })
      tokens.set(data)
      await loadUser()
      return true
    } catch (failure) {
      const status = failure?.response?.status
      error.value =
        status === 401
          ? 'Usuario o contraseña incorrectos.'
          : errorMessage(failure, 'No se ha podido iniciar sesión.')
      tokens.clear()
      user.value = null
      return false
    } finally {
      loading.value = false
    }
  }

  async function loadUser() {
    if (!tokens.access) {
      user.value = null
      return null
    }
    const { data } = await api.get('auth/me/')
    user.value = data
    return data
  }

  /** Called on boot: restores the session if the stored token still works. */
  async function restore() {
    if (!tokens.access) return false
    try {
      await loadUser()
      return true
    } catch {
      tokens.clear()
      user.value = null
      return false
    }
  }

  function signOut() {
    tokens.clear()
    user.value = null
  }

  return { user, loading, error, isSignedIn, name, signIn, loadUser, restore, signOut }
})
