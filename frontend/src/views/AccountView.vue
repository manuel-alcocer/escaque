<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import { api, errorMessage } from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { useProgressStore } from '@/stores/progress'

const auth = useAuthStore()
const progress = useProgressStore()
const router = useRouter()

const saving = ref(false)
const saved = ref(false)
const saveError = ref('')

const displayName = ref(auth.user?.display_name || '')
const rating = ref(auth.user?.rating_estimate || 1200)
const orientation = ref(auth.user?.board_orientation_hint || 'auto')

const engineLabel = computed(() => {
  if (progress.engine.available === null) return 'Sin comprobar'
  return progress.engine.available ? progress.engine.name || 'Disponible' : 'No responde'
})

async function save() {
  saving.value = true
  saved.value = false
  saveError.value = ''
  try {
    const { data } = await api.patch('auth/me/', {
      display_name: displayName.value,
      rating_estimate: rating.value,
      board_orientation_hint: orientation.value,
    })
    auth.user = data
    saved.value = true
  } catch (error) {
    saveError.value = errorMessage(error, 'No se han podido guardar los cambios.')
  } finally {
    saving.value = false
  }
}

function signOut() {
  auth.signOut()
  progress.invalidate()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="shell page">
    <header class="page__head">
      <p class="eyebrow">{{ auth.user?.username }}</p>
      <h1>Cuenta</h1>
    </header>

    <form class="form" @submit.prevent="save">
      <label class="field">
        <span class="field__label">Nombre visible</span>
        <input v-model="displayName" type="text" class="field__input" maxlength="80" />
      </label>

      <label class="field">
        <span class="field__label">Nivel aproximado (Elo)</span>
        <input v-model.number="rating" type="number" min="400" max="3000" step="50" class="field__input" />
        <span class="field__help">Ordena los ejercicios por dificultad. No hace falta que sea exacto.</span>
      </label>

      <label class="field">
        <span class="field__label">Orientación del tablero</span>
        <select v-model="orientation" class="field__input">
          <option value="auto">Según el ejercicio</option>
          <option value="white">Siempre desde las blancas</option>
          <option value="black">Siempre desde las negras</option>
        </select>
      </label>

      <p v-if="saveError" class="form__error" role="alert">{{ saveError }}</p>
      <p v-else-if="saved" class="form__ok" role="status">Cambios guardados.</p>

      <button type="submit" class="btn btn--primary" :disabled="saving">
        {{ saving ? 'Guardando…' : 'Guardar cambios' }}
      </button>
    </form>

    <section class="info">
      <h2 class="info__title">Motor de análisis</h2>
      <p class="info__row">
        <span class="mono">{{ engineLabel }}</span>
        <button type="button" class="btn btn--quiet" @click="progress.checkEngine()">Comprobar</button>
      </p>
      <p class="info__note">
        Stockfish corre en su propio contenedor. Si no responde, los ejercicios siguen
        funcionando: sólo se pierde el análisis de la posición.
      </p>
    </section>

    <section class="info">
      <h2 class="info__title">Acceso</h2>
      <p class="info__note">
        Las cuentas se crean desde el servidor con
        <code class="mono">python manage.py createuser</code>. El acceso con Google está
        preparado en el modelo de datos y se activará más adelante.
      </p>
      <button type="button" class="btn" @click="signOut">Cerrar sesión</button>
    </section>
  </div>
</template>

<style scoped>
.page {
  padding-top: var(--gap-5);
  max-width: 34rem;
}

.page__head h1 {
  margin-top: var(--gap-2);
}

.form {
  display: flex;
  flex-direction: column;
  gap: var(--gap-4);
  margin: var(--gap-5) 0 var(--gap-6);
}

.field {
  display: flex;
  flex-direction: column;
  gap: var(--gap-1);
}

.field__label {
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--bone-faint);
}

.field__input {
  height: 2.875rem;
  padding: 0 var(--gap-3);
  background: var(--ink-700);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  color: var(--bone);
  font-family: var(--font-mono);
  font-size: 1rem;
}

.field__input:focus {
  border-color: var(--brass);
  outline: none;
}

.field__help {
  font-size: 0.8125rem;
  color: var(--bone-faint);
}

.form__error {
  margin: 0;
  padding: var(--gap-2) var(--gap-3);
  background: var(--rust-dim);
  border-left: 2px solid var(--rust);
  font-size: 0.875rem;
}

.form__ok {
  margin: 0;
  color: var(--sage);
  font-size: 0.875rem;
}

.info {
  border-top: 1px solid var(--line-soft);
  padding: var(--gap-4) 0;
}

.info__title {
  font-size: 1rem;
  margin-bottom: var(--gap-3);
}

.info__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--gap-3);
  margin: 0 0 var(--gap-2);
  font-size: 0.875rem;
}

.info__note {
  margin: 0 0 var(--gap-3);
  font-size: 0.875rem;
  color: var(--bone-faint);
  line-height: 1.55;
}
</style>
