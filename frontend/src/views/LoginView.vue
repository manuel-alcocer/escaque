<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import AutoBoard from '@/components/AutoBoard.vue'
import { useAuthStore } from '@/stores/auth'
import { useProgressStore } from '@/stores/progress'

const auth = useAuthStore()
const progress = useProgressStore()
const router = useRouter()
const route = useRoute()

const username = ref('')
const password = ref('')

// The Ruy Lopez, played on loop: three moves that state what the site is about.
const RUY_LOPEZ = ['e4', 'e5', 'Nf3', 'Nc6', 'Bb5']

async function submit() {
  const ok = await auth.signIn(username.value.trim(), password.value)
  if (!ok) return
  progress.checkEngine()
  router.push(route.query.next || { name: 'home' })
}
</script>

<template>
  <div class="entry">
    <section class="entry__stage">
      <div class="entry__board">
        <AutoBoard :moves-san="RUY_LOPEZ" :interval-ms="1000" :hold-ms="2400" />
      </div>
      <div class="entry__caption">
        <p class="eyebrow">C60 · Ruy López · 1561</p>
        <p class="entry__caption-text">
          3.Ab5 no amenaza nada. Ésa es la idea.
        </p>
      </div>
    </section>

    <section class="entry__panel">
      <header class="entry__head">
        <p class="brandline">Escaque</p>
        <h1 class="entry__title">Teoría<br />y ejercicios</h1>
        <p class="entry__lede">
          Apertura Española, Defensa India de Rey y Caro-Kann. Cada variante con su
          plan, y muchos ejercicios sobre el tablero.
        </p>
      </header>

      <form class="entry__form" @submit.prevent="submit">
        <label class="field">
          <span class="field__label">Usuario</span>
          <input
            v-model="username"
            type="text"
            name="username"
            autocomplete="username"
            autocapitalize="none"
            autocorrect="off"
            spellcheck="false"
            required
            class="field__input"
          />
        </label>

        <label class="field">
          <span class="field__label">Contraseña</span>
          <input
            v-model="password"
            type="password"
            name="password"
            autocomplete="current-password"
            required
            class="field__input"
          />
        </label>

        <p v-if="auth.error" class="entry__error" role="alert">{{ auth.error }}</p>

        <button type="submit" class="btn btn--primary btn--block" :disabled="auth.loading">
          {{ auth.loading ? 'Entrando…' : 'Entrar' }}
        </button>
      </form>

      <p class="entry__note">
        Las cuentas se crean desde el servidor con
        <code class="mono">manage.py createuser</code>. El acceso con Google llegará
        más adelante.
      </p>
    </section>
  </div>
</template>

<style scoped>
.entry {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  background: var(--ink-800);
}

/* Phone: the board comes first and takes the top of the screen, so the app
 * shows what it is before it asks for anything. */
.entry__stage {
  padding: var(--gap-5) var(--gap-4) var(--gap-4);
  background: var(--ink-900);
  border-bottom: 1px solid var(--line-soft);
}

.entry__board {
  max-width: 17rem;
  margin: 0 auto;
}

.entry__caption {
  margin-top: var(--gap-3);
  text-align: center;
}

.entry__caption-text {
  margin: var(--gap-1) 0 0;
  font-size: 0.9375rem;
  font-style: italic;
  color: var(--bone-dim);
}

.entry__panel {
  flex: 1;
  padding: var(--gap-5) var(--gap-4) var(--gap-6);
  display: flex;
  flex-direction: column;
  gap: var(--gap-5);
  max-width: 26rem;
  width: 100%;
  margin: 0 auto;
}

.brandline {
  font-family: var(--font-display);
  font-variation-settings: 'wdth' 122;
  font-weight: 700;
  font-size: 0.75rem;
  letter-spacing: 0.36em;
  text-transform: uppercase;
  color: var(--brass);
  margin: 0 0 var(--gap-3);
}

.entry__title {
  font-size: clamp(2.25rem, 12vw, 3rem);
}

.entry__lede {
  margin: var(--gap-3) 0 0;
  color: var(--bone-dim);
  font-size: 1rem;
}

.entry__form {
  display: flex;
  flex-direction: column;
  gap: var(--gap-3);
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
  font-size: 1rem; /* 16px keeps iOS from zooming on focus. */
}

.field__input:focus {
  border-color: var(--brass);
  outline: none;
}

.entry__error {
  margin: 0;
  padding: var(--gap-2) var(--gap-3);
  background: var(--rust-dim);
  border-left: 2px solid var(--rust);
  color: #e8bdb1;
  font-size: 0.875rem;
}

.entry__note {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--bone-faint);
  line-height: 1.5;
}

.entry__note code {
  font-size: 0.75rem;
  color: var(--bone-dim);
}

/* Desktop: two columns, board on the left, form on the right. */
@media (min-width: 56rem) {
  .entry {
    flex-direction: row;
    align-items: stretch;
  }

  .entry__stage {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-bottom: 0;
    border-right: 1px solid var(--line-soft);
    padding: var(--gap-7);
  }

  .entry__board {
    max-width: 24rem;
  }

  .entry__panel {
    flex: 1;
    justify-content: center;
    padding: var(--gap-7) var(--gap-6);
    max-width: 32rem;
    margin: 0;
  }
}
</style>
