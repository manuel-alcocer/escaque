import { defineStore } from 'pinia'
import { ref } from 'vue'

import { api } from '@/api/client'

/** Shared summary so the dashboard and the header do not both fetch it. */
export const useProgressStore = defineStore('progress', () => {
  const summary = ref(null)
  const loading = ref(false)
  const engine = ref({ available: null, name: '' })

  async function load(force = false) {
    if (summary.value && !force) return summary.value
    loading.value = true
    try {
      const { data } = await api.get('progress/summary/')
      summary.value = data
      return data
    } finally {
      loading.value = false
    }
  }

  /** The engine is optional, so a failure here is information, not an error. */
  async function checkEngine() {
    try {
      const { data } = await api.get('engine/status/')
      engine.value = { available: Boolean(data.available), name: data.engine || '' }
    } catch {
      engine.value = { available: false, name: '' }
    }
    return engine.value
  }

  function invalidate() {
    summary.value = null
  }

  return { summary, loading, engine, load, checkEngine, invalidate }
})
