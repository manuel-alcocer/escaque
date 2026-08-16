<script setup>
import AutoBoard from '@/components/AutoBoard.vue'

// Légal's mate: a short, famous line, and a page that goes nowhere.
const LEGAL = ['e4', 'e5', 'Nf3', 'd6', 'Bc4', 'Bg4', 'Nc3', 'g6', 'Nxe5', 'Bxd1', 'Bxf7+', 'Ke7', 'Nd5#']
</script>

<template>
  <div class="shell missing">
    <div class="missing__board">
      <AutoBoard :moves-san="LEGAL" :interval-ms="700" :hold-ms="3200" />
    </div>
    <div>
      <p class="eyebrow">Mate de Légal · 1750</p>
      <h1 class="missing__title">Sin salida</h1>
      <p class="missing__text">
        Esta página no existe. La posición de al lado tampoco tiene escapatoria, pero
        al menos es instructiva.
      </p>
      <RouterLink :to="{ name: 'home' }" class="btn btn--primary">Volver al repertorio</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.missing {
  padding: var(--gap-6) var(--gap-4);
  display: grid;
  gap: var(--gap-5);
  align-items: center;
}

.missing__board {
  max-width: 16rem;
}

.missing__title {
  margin: var(--gap-2) 0 var(--gap-3);
}

.missing__text {
  color: var(--bone-dim);
  max-width: 28rem;
}

@media (min-width: 42rem) {
  .missing {
    grid-template-columns: 18rem 1fr;
    gap: var(--gap-6);
  }

  .missing__board {
    max-width: none;
  }
}
</style>
