<script setup>
import { computed, onMounted, ref } from 'vue'

import AutoBoard from '@/components/AutoBoard.vue'
import { api } from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { useProgressStore } from '@/stores/progress'

const auth = useAuthStore()
const progress = useProgressStore()

const sections = ref([])
const loading = ref(true)
const loadError = ref('')

const summary = computed(() => progress.summary)
const pending = computed(() => summary.value?.needs_review ?? 0)

/** Per-opening counts, keyed by slug, so a card can show its own progress. */
const byOpening = computed(() => {
  const map = {}
  ;(summary.value?.by_opening || []).forEach((row) => (map[row.slug] = row))
  return map
})

onMounted(async () => {
  try {
    const [{ data }] = await Promise.all([api.get('sections/'), progress.load(true)])
    sections.value = data
  } catch {
    loadError.value = 'No se ha podido cargar el contenido. Revisa la conexión y vuelve a intentarlo.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="home">
    <!-- Hero. The first thing on screen is what this user has left to do. -->
    <section class="hero">
      <div class="shell">
        <p class="eyebrow">
          {{ auth.name }} · {{ summary?.exercises_total ?? '—' }} ejercicios en el repertorio
        </p>
        <h1 class="hero__title">Estudia<br />la posición</h1>

        <div v-if="summary" class="tally">
          <div class="tally__cell">
            <span class="tally__value mono">{{ summary.solved }}</span>
            <span class="tally__label">Resueltos</span>
          </div>
          <div class="tally__cell">
            <span class="tally__value tally__value--rust mono">{{ summary.failed }}</span>
            <span class="tally__label">Fallidos</span>
          </div>
          <div class="tally__cell">
            <span class="tally__value mono">{{ summary.unseen }}</span>
            <span class="tally__label">Sin hacer</span>
          </div>
        </div>

        <div class="hero__actions">
          <RouterLink :to="{ name: 'train' }" class="btn btn--primary">
            {{ pending ? `Repasar ${pending} fallidos` : 'Empezar a entrenar' }}
          </RouterLink>
          <RouterLink v-if="summary?.attempts_total" :to="{ name: 'progress' }" class="btn">
            Ver progreso
          </RouterLink>
        </div>
      </div>
    </section>

    <p v-if="loadError" class="shell home__error" role="alert">{{ loadError }}</p>

    <div v-if="loading" class="shell home__loading" role="status">Cargando el repertorio…</div>

    <!-- Sections. Each opening introduces itself by playing its own moves. -->
    <section v-for="section in sections" :key="section.slug" class="band">
      <div class="shell">
        <header class="band__head">
          <p class="eyebrow">{{ section.openings.length }} en esta sección</p>
          <h2>{{ section.name }}</h2>
          <p class="band__tagline">{{ section.tagline }}</p>
        </header>

        <ul class="cards">
          <li v-for="opening in section.openings" :key="opening.slug" class="card">
            <RouterLink :to="{ name: 'opening', params: { slug: opening.slug } }" class="card__link">
              <div class="card__board">
                <AutoBoard
                  :moves-san="opening.moves_san"
                  :orientation="opening.colour"
                  :interval-ms="850"
                  :hold-ms="2800"
                />
              </div>

              <div class="card__body">
                <p class="eyebrow">{{ opening.eco_range }}</p>
                <h3 class="card__name">{{ opening.name }}</h3>
                <p class="card__tagline">{{ opening.tagline }}</p>

                <div class="card__meta mono">
                  <span>{{ opening.variation_count }} variantes</span>
                  <span aria-hidden="true">·</span>
                  <span>{{ opening.exercise_count }} ejercicios</span>
                </div>

                <div v-if="byOpening[opening.slug]" class="meter" role="img"
                  :aria-label="`${byOpening[opening.slug].solved} de ${byOpening[opening.slug].total} ejercicios resueltos`">
                  <span
                    class="meter__fill meter__fill--solved"
                    :style="{ width: `${(byOpening[opening.slug].solved / byOpening[opening.slug].total) * 100}%` }"
                  ></span>
                  <span
                    class="meter__fill meter__fill--failed"
                    :style="{ width: `${(byOpening[opening.slug].failed / byOpening[opening.slug].total) * 100}%` }"
                  ></span>
                </div>
              </div>
            </RouterLink>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero {
  padding: var(--gap-6) 0 var(--gap-5);
  border-bottom: 1px solid var(--line-soft);
  background: linear-gradient(180deg, var(--ink-900), var(--ink-800));
}

.hero__title {
  margin: var(--gap-2) 0 var(--gap-5);
}

/* Counts set like a score sheet, not like a dashboard widget. */
.tally {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
}

.tally__cell {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  padding: var(--gap-3) 0;
}

.tally__cell + .tally__cell {
  border-left: 1px solid var(--line-soft);
  padding-left: var(--gap-3);
}

.tally__value {
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1;
  color: var(--brass);
}

.tally__value--rust {
  color: var(--rust);
}

.tally__label {
  font-family: var(--font-mono);
  font-size: 0.625rem;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--bone-faint);
}

.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--gap-2);
  margin-top: var(--gap-4);
}

.home__error {
  margin: var(--gap-5) auto;
  padding: var(--gap-3);
  border-left: 2px solid var(--rust);
  background: var(--rust-dim);
  color: #e8bdb1;
}

.home__loading {
  padding: var(--gap-6) var(--gap-4);
  color: var(--bone-faint);
}

.band {
  padding: var(--gap-6) 0 var(--gap-4);
}

.band + .band {
  border-top: 1px solid var(--line-soft);
}

.band__head {
  margin-bottom: var(--gap-5);
}

.band__head h2 {
  margin: var(--gap-2) 0 var(--gap-2);
}

.band__tagline {
  margin: 0;
  color: var(--bone-dim);
  font-size: 0.9375rem;
  max-width: 34rem;
}

.cards {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: var(--gap-4);
}

.card {
  border: 1px solid var(--line-soft);
  border-radius: var(--radius);
  background: var(--ink-700);
  transition: border-color 0.18s ease;
}

.card:hover {
  border-color: var(--brass-dim);
}

.card__link {
  display: grid;
  grid-template-columns: 6.5rem 1fr;
  gap: var(--gap-4);
  padding: var(--gap-4);
  align-items: start;
}

.card__name {
  margin: var(--gap-1) 0 var(--gap-2);
}

.card__tagline {
  margin: 0 0 var(--gap-3);
  font-size: 0.875rem;
  color: var(--bone-dim);
  line-height: 1.45;
}

.card__meta {
  display: flex;
  gap: var(--gap-2);
  font-size: 0.6875rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--bone-faint);
}

/* Two-colour bar: solved and failed against the total. */
.meter {
  display: flex;
  height: 3px;
  margin-top: var(--gap-3);
  background: var(--ink-600);
  overflow: hidden;
}

.meter__fill--solved {
  background: var(--sage);
}

.meter__fill--failed {
  background: var(--rust);
}

@media (min-width: 34rem) {
  .card__link {
    grid-template-columns: 9rem 1fr;
    gap: var(--gap-5);
  }
}

@media (min-width: 62rem) {
  .cards {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .card__link {
    grid-template-columns: 8rem 1fr;
  }
}
</style>
