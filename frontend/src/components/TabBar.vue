<script setup>
/**
 * Bottom navigation for phones, which is where this app is mostly used.
 * Hidden from 48rem up, where the header nav takes over.
 */
const destinations = [
  { name: 'home', label: 'Aprender', glyph: '♟' },
  { name: 'train', label: 'Entrenar', glyph: '♞' },
  { name: 'progress', label: 'Progreso', glyph: '♜' },
  { name: 'account', label: 'Cuenta', glyph: '♚' },
]
</script>

<template>
  <nav class="tabbar" aria-label="Navegación principal">
    <RouterLink
      v-for="destination in destinations"
      :key="destination.name"
      :to="{ name: destination.name }"
      class="tabbar__item"
    >
      <span class="tabbar__glyph" aria-hidden="true">{{ destination.glyph }}</span>
      <span class="tabbar__label">{{ destination.label }}</span>
    </RouterLink>
  </nav>
</template>

<style scoped>
.tabbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 30;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  background: rgba(20, 16, 14, 0.96);
  backdrop-filter: blur(10px);
  border-top: 1px solid var(--line-soft);
  padding-bottom: var(--safe-bottom);
}

.tabbar__item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.1rem;
  height: var(--tabbar);
  color: var(--bone-faint);
  transition: color 0.15s ease;
  touch-action: manipulation;
}

.tabbar__glyph {
  font-size: 1.05rem;
  line-height: 1;
}

.tabbar__label {
  font-family: var(--font-display);
  font-variation-settings: 'wdth' 100;
  font-size: 0.625rem;
  font-weight: 600;
  letter-spacing: 0.09em;
  text-transform: uppercase;
}

.tabbar__item.router-link-active {
  color: var(--brass);
}

@media (min-width: 48rem) {
  .tabbar {
    display: none;
  }
}
</style>
