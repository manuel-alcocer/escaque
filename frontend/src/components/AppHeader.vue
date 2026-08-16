<script setup>
import { computed } from 'vue'

import { useProgressStore } from '@/stores/progress'

const progress = useProgressStore()

const engineLabel = computed(() => {
  if (progress.engine.available === null) return 'Motor'
  return progress.engine.available ? 'Motor activo' : 'Motor apagado'
})
</script>

<template>
  <header class="header">
    <div class="header__inner shell">
      <RouterLink :to="{ name: 'home' }" class="brand" aria-label="Escaque, inicio">
        <span class="brand__mark" aria-hidden="true"></span>
        <span class="brand__word">Escaque</span>
      </RouterLink>

      <nav class="header__nav" aria-label="Secciones">
        <RouterLink :to="{ name: 'home' }" class="header__link">Aprender</RouterLink>
        <RouterLink :to="{ name: 'train' }" class="header__link">Entrenar</RouterLink>
        <RouterLink :to="{ name: 'progress' }" class="header__link">Progreso</RouterLink>
        <RouterLink :to="{ name: 'account' }" class="header__link">Cuenta</RouterLink>
      </nav>

      <p class="header__engine mono" :class="{ 'header__engine--off': progress.engine.available === false }">
        <span class="header__dot" aria-hidden="true"></span>
        <span>{{ engineLabel }}</span>
      </p>
    </div>
  </header>
</template>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 20;
  background: rgba(22, 17, 15, 0.93);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--line-soft);
}

.header__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--gap-4);
  height: 3.25rem;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: var(--gap-2);
}

/* The mark is one square of a board — the word means exactly that. */
.brand__mark {
  width: 0.7rem;
  height: 0.7rem;
  background: var(--brass);
  display: block;
}

.brand__word {
  font-family: var(--font-display);
  font-variation-settings: 'wdth' 120;
  font-weight: 700;
  font-size: 0.95rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
}

.header__nav {
  display: none;
  gap: var(--gap-5);
}

.header__link {
  font-family: var(--font-display);
  font-variation-settings: 'wdth' 105;
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--bone-dim);
  padding: 0.25rem 0;
  border-bottom: 1px solid transparent;
}

.header__link:hover {
  color: var(--bone);
}

.header__link.router-link-active {
  color: var(--brass);
  border-bottom-color: var(--brass);
}

.header__engine {
  display: inline-flex;
  align-items: center;
  gap: var(--gap-2);
  font-size: 0.625rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--bone-faint);
  margin: 0;
}

.header__dot {
  width: 0.375rem;
  height: 0.375rem;
  border-radius: 50%;
  background: var(--sage);
}

.header__engine--off .header__dot {
  background: var(--bone-faint);
}

/* On a phone the header is just the brand and the engine light; navigation
 * lives at the bottom, within reach. */
@media (max-width: 47.99rem) {
  .header__engine span:last-child {
    display: none;
  }
}

@media (min-width: 48rem) {
  .header__nav {
    display: flex;
  }
}
</style>
