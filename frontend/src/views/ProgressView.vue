<script setup>
/**
 * The tracking screen. The product rule is that an exercise not solved correctly
 * is recorded as failed, so failures are the headline here, not a footnote.
 */
import { computed, onMounted, ref } from 'vue'

import { api } from '@/api/client'
import { formatDuration, STATUS_LABELS } from '@/lib/notation'
import { useProgressStore } from '@/stores/progress'

const progress = useProgressStore()
const attempts = ref([])
const loadingAttempts = ref(true)

const summary = computed(() => progress.summary)

const accuracyLabel = computed(() => {
  const value = summary.value?.accuracy
  return value === null || value === undefined ? '—' : `${Math.round(value * 100)}%`
})

function percentage(part, total) {
  return total ? `${(part / total) * 100}%` : '0%'
}

function formatDate(value) {
  return new Date(value).toLocaleString('es-ES', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(async () => {
  await progress.load(true)
  try {
    const { data } = await api.get('attempts/', { params: { limit: 30 } })
    attempts.value = data.results || data
  } finally {
    loadingAttempts.value = false
  }
})
</script>

<template>
  <div class="shell page">
    <header class="page__head">
      <p class="eyebrow">Tu registro</p>
      <h1>Progreso</h1>
    </header>

    <section v-if="summary" class="totals">
      <div class="totals__row">
        <span class="totals__value mono">{{ summary.attempts_total }}</span>
        <span class="totals__label">Intentos</span>
      </div>
      <div class="totals__row">
        <span class="totals__value mono">{{ accuracyLabel }}</span>
        <span class="totals__label">Acierto</span>
      </div>
      <div class="totals__row">
        <span class="totals__value totals__value--rust mono">{{ summary.needs_review }}</span>
        <span class="totals__label">Por repasar</span>
      </div>
    </section>

    <p v-if="summary?.needs_review" class="callout">
      Tienes {{ summary.needs_review }} ejercicios marcados como fallidos. Siguen marcados
      hasta que los resuelvas bien.
      <RouterLink :to="{ name: 'train', query: { status: 'review' } }" class="callout__link">
        Repasarlos ahora →
      </RouterLink>
    </p>

    <section v-if="summary" class="block">
      <h2 class="block__title">Por apertura</h2>
      <ul class="openings">
        <li v-for="row in summary.by_opening" :key="row.slug" class="opening">
          <div class="opening__head">
            <RouterLink :to="{ name: 'opening', params: { slug: row.slug } }" class="opening__name">
              {{ row.name }}
            </RouterLink>
            <span class="opening__eco mono">{{ row.eco_range }}</span>
          </div>

          <div class="bar" role="img" :aria-label="`${row.solved} resueltos, ${row.failed} fallidos, de ${row.total}`">
            <span class="bar__fill bar__fill--solved" :style="{ width: percentage(row.solved, row.total) }"></span>
            <span class="bar__fill bar__fill--failed" :style="{ width: percentage(row.failed, row.total) }"></span>
          </div>

          <p class="opening__counts mono">
            <span class="count count--solved">{{ row.solved }} resueltos</span>
            <span class="count count--failed">{{ row.failed }} fallidos</span>
            <span class="count">{{ row.unseen }} sin hacer</span>
          </p>
        </li>
      </ul>
    </section>

    <section class="block">
      <h2 class="block__title">Últimos intentos</h2>

      <p v-if="loadingAttempts" class="empty" role="status">Cargando…</p>
      <p v-else-if="!attempts.length" class="empty">
        Todavía no has intentado ningún ejercicio. Empieza por la apertura que más juegues.
      </p>

      <ul v-else class="attempts">
        <li v-for="attempt in attempts" :key="attempt.id" class="attempt">
          <span class="attempt__status" :class="`attempt__status--${attempt.status}`">
            {{ STATUS_LABELS[attempt.status] }}
          </span>
          <div class="attempt__body">
            <p class="attempt__prompt">{{ attempt.prompt }}</p>
            <p class="attempt__meta mono">
              {{ attempt.opening_name }} · {{ attempt.variation_name }}
            </p>
          </div>
          <div class="attempt__side mono">
            <span>{{ formatDuration(attempt.duration_ms) }}</span>
            <span class="attempt__date">{{ formatDate(attempt.created_at) }}</span>
          </div>
        </li>
      </ul>
    </section>
  </div>
</template>

<style scoped>
.page {
  padding-top: var(--gap-5);
}

.page__head h1 {
  margin-top: var(--gap-2);
}

.totals {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
  margin: var(--gap-5) 0;
}

.totals__row {
  display: flex;
  flex-direction: column;
  padding: var(--gap-3) 0;
}

.totals__row + .totals__row {
  border-left: 1px solid var(--line-soft);
  padding-left: var(--gap-3);
}

.totals__value {
  font-size: 1.6rem;
  font-weight: 700;
  line-height: 1;
  color: var(--brass);
}

.totals__value--rust {
  color: var(--rust);
}

.totals__label {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--bone-faint);
  margin-top: 0.2rem;
}

.callout {
  margin: 0 0 var(--gap-6);
  padding: var(--gap-3);
  background: var(--rust-dim);
  border-left: 2px solid var(--rust);
  font-size: 0.9375rem;
  line-height: 1.5;
}

.callout__link {
  display: inline-block;
  margin-top: var(--gap-2);
  color: var(--brass-bright);
  font-family: var(--font-mono);
  font-size: 0.8125rem;
}

.block {
  margin-bottom: var(--gap-6);
}

.block__title {
  font-size: 1.15rem;
  margin-bottom: var(--gap-4);
}

.openings {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: var(--gap-4);
}

.opening__head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: var(--gap-2);
}

.opening__name {
  font-family: var(--font-display);
  font-variation-settings: 'wdth' 106;
  font-weight: 600;
  font-size: 0.9375rem;
}

.opening__name:hover {
  color: var(--brass);
}

.opening__eco {
  font-size: 0.625rem;
  letter-spacing: 0.1em;
  color: var(--bone-faint);
}

.bar {
  display: flex;
  height: 4px;
  margin: var(--gap-2) 0;
  background: var(--ink-600);
  overflow: hidden;
}

.bar__fill--solved {
  background: var(--sage);
}

.bar__fill--failed {
  background: var(--rust);
}

.opening__counts {
  display: flex;
  flex-wrap: wrap;
  gap: var(--gap-3);
  margin: 0;
  font-size: 0.625rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--bone-faint);
}

.count--solved {
  color: var(--sage);
}

.count--failed {
  color: var(--rust);
}

.attempts {
  list-style: none;
  margin: 0;
  padding: 0;
}

.attempt {
  display: grid;
  grid-template-columns: 4.5rem 1fr;
  gap: var(--gap-3);
  padding: var(--gap-3) 0;
  border-bottom: 1px solid var(--line-soft);
}

.attempt__status {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding-top: 0.15rem;
}

.attempt__status--solved {
  color: var(--sage);
}

.attempt__status--failed {
  color: var(--rust);
}

.attempt__prompt {
  margin: 0;
  font-size: 0.9375rem;
  line-height: 1.4;
}

.attempt__meta {
  margin: var(--gap-1) 0 0;
  font-size: 0.6875rem;
  color: var(--bone-faint);
}

.attempt__side {
  display: none;
  flex-direction: column;
  align-items: flex-end;
  font-size: 0.6875rem;
  color: var(--bone-faint);
}

.empty {
  color: var(--bone-faint);
  font-size: 0.9375rem;
}

@media (min-width: 40rem) {
  .attempt {
    grid-template-columns: 4.5rem 1fr 8rem;
  }

  .attempt__side {
    display: flex;
  }
}
</style>
