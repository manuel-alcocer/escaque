<script setup>
import { computed, onMounted, ref, watch } from 'vue'

import { api, errorMessage } from '@/api/client'
import AutoBoard from '@/components/AutoBoard.vue'
import MarkdownBlock from '@/components/MarkdownBlock.vue'
import { toInlineLine } from '@/lib/notation'

const props = defineProps({ slug: { type: String, required: true } })

const opening = ref(null)
const loading = ref(true)
const loadError = ref('')

/** Sub-variations are nested under their parent so the list reads as a tree. */
const tree = computed(() => {
  const variations = opening.value?.variations || []
  const children = new Map()
  variations.forEach((variation) => {
    if (variation.parent) {
      const list = children.get(variation.parent) || []
      list.push(variation)
      children.set(variation.parent, list)
    }
  })
  return variations
    .filter((variation) => !variation.parent)
    .map((variation) => ({ ...variation, children: children.get(variation.id) || [] }))
})

async function load() {
  loading.value = true
  loadError.value = ''
  try {
    const { data } = await api.get(`openings/${props.slug}/`)
    opening.value = data
  } catch (error) {
    loadError.value = errorMessage(error, 'No se ha encontrado esta apertura.')
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => props.slug, load)
</script>

<template>
  <div v-if="loading" class="shell state" role="status">Cargando…</div>
  <div v-else-if="loadError" class="shell state state--error" role="alert">{{ loadError }}</div>

  <article v-else class="opening">
    <header class="masthead">
      <div class="shell masthead__inner">
        <div class="masthead__text">
          <p class="eyebrow">
            {{ opening.eco_range }} ·
            {{ opening.colour === 'white' ? 'Juegan las blancas' : 'Juegan las negras' }}
          </p>
          <h1>{{ opening.name }}</h1>
          <p v-if="opening.alternative_names.length" class="masthead__alias">
            También llamada {{ opening.alternative_names.join(', ') }}
          </p>
          <p class="masthead__line mono">{{ toInlineLine(opening.moves_san) }}</p>
          <p class="masthead__summary">{{ opening.summary }}</p>
          <p v-if="opening.first_played" class="masthead__origin">{{ opening.first_played }}</p>
        </div>

        <div class="masthead__board">
          <AutoBoard
            :moves-san="opening.moves_san"
            :orientation="opening.colour"
            :interval-ms="950"
            show-line
          />
        </div>
      </div>
    </header>

    <section class="shell section">
      <MarkdownBlock :source="opening.description" />
    </section>

    <section class="shell section">
      <header class="section__head">
        <p class="eyebrow">{{ opening.variation_count }} variantes · {{ opening.exercise_count }} ejercicios</p>
        <h2>Variantes</h2>
      </header>

      <ul class="lines">
        <li v-for="variation in tree" :key="variation.id" class="lines__group">
          <RouterLink
            :to="{ name: 'variation', params: { openingSlug: opening.slug, slug: variation.slug } }"
            class="line"
          >
            <div class="line__head">
              <span class="line__eco mono">{{ variation.eco || '—' }}</span>
              <h3 class="line__name">{{ variation.name }}</h3>
              <span v-if="variation.is_main_line" class="chip chip--brass">Principal</span>
            </div>
            <p class="line__moves mono">{{ toInlineLine(variation.moves_san, 0, 12) }}</p>
            <p class="line__tagline">{{ variation.tagline }}</p>
            <div class="line__stats mono">
              <span>{{ variation.exercise_count }} ejercicios</span>
              <span v-if="variation.solved_count" class="line__stat--solved">
                {{ variation.solved_count }} resueltos
              </span>
              <span v-if="variation.failed_count" class="line__stat--failed">
                {{ variation.failed_count }} fallidos
              </span>
            </div>
          </RouterLink>

          <ul v-if="variation.children.length" class="lines__children">
            <li v-for="child in variation.children" :key="child.id">
              <RouterLink
                :to="{ name: 'variation', params: { openingSlug: opening.slug, slug: child.slug } }"
                class="line line--child"
              >
                <div class="line__head">
                  <span class="line__eco mono">{{ child.eco || '—' }}</span>
                  <h3 class="line__name">{{ child.name }}</h3>
                </div>
                <p class="line__tagline">{{ child.tagline }}</p>
                <div class="line__stats mono">
                  <span>{{ child.exercise_count }} ejercicios</span>
                  <span v-if="child.solved_count" class="line__stat--solved">
                    {{ child.solved_count }} resueltos
                  </span>
                  <span v-if="child.failed_count" class="line__stat--failed">
                    {{ child.failed_count }} fallidos
                  </span>
                </div>
              </RouterLink>
            </li>
          </ul>
        </li>
      </ul>
    </section>

    <!-- Sticky call to action: on a phone this is the reason you opened the page. -->
    <div class="cta">
      <div class="shell">
        <RouterLink
          :to="{ name: 'train', query: { opening: opening.slug } }"
          class="btn btn--primary btn--block"
        >
          Entrenar {{ opening.name }}
        </RouterLink>
      </div>
    </div>
  </article>
</template>

<style scoped>
.state {
  padding: var(--gap-6) var(--gap-4);
  color: var(--bone-faint);
}

.state--error {
  color: #e8bdb1;
}

.masthead {
  padding: var(--gap-5) 0;
  background: linear-gradient(180deg, var(--ink-900), var(--ink-800));
  border-bottom: 1px solid var(--line-soft);
}

.masthead__inner {
  display: grid;
  gap: var(--gap-5);
}

.masthead__alias {
  margin: var(--gap-2) 0 0;
  font-style: italic;
  color: var(--bone-faint);
  font-size: 0.875rem;
}

.masthead__line {
  margin: var(--gap-3) 0;
  font-size: 0.875rem;
  color: var(--brass);
  letter-spacing: 0.02em;
}

.masthead__summary {
  margin: 0;
  color: var(--bone-dim);
  font-size: 1rem;
  max-width: 36rem;
}

.masthead__origin {
  margin: var(--gap-3) 0 0;
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--bone-faint);
}

.masthead__board {
  max-width: 18rem;
}

.section {
  padding: var(--gap-6) var(--gap-4);
}

.section__head {
  margin-bottom: var(--gap-4);
}

.section__head h2 {
  margin-top: var(--gap-2);
}

.lines {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: var(--gap-3);
}

.lines__children {
  list-style: none;
  margin: var(--gap-2) 0 0 var(--gap-4);
  padding: 0 0 0 var(--gap-3);
  border-left: 1px solid var(--line);
  display: grid;
  gap: var(--gap-2);
}

.line {
  display: block;
  padding: var(--gap-3);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius);
  background: var(--ink-700);
  transition: border-color 0.18s ease;
}

.line:hover {
  border-color: var(--brass-dim);
}

.line--child {
  background: transparent;
}

.line__head {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: var(--gap-2);
}

/* The ECO code is a real classification, so it earns its place as the label. */
.line__eco {
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: var(--brass);
  min-width: 3.5rem;
}

.line__name {
  font-size: 1rem;
  margin: 0;
}

.line__moves {
  margin: var(--gap-2) 0 0;
  font-size: 0.75rem;
  color: var(--bone-faint);
}

.line__tagline {
  margin: var(--gap-2) 0 0;
  font-size: 0.875rem;
  color: var(--bone-dim);
  line-height: 1.45;
}

.line__stats {
  display: flex;
  flex-wrap: wrap;
  gap: var(--gap-3);
  margin-top: var(--gap-3);
  font-size: 0.6875rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--bone-faint);
}

.line__stat--solved {
  color: var(--sage);
}

.line__stat--failed {
  color: var(--rust);
}

.cta {
  position: sticky;
  bottom: 0;
  padding: var(--gap-3) 0 calc(var(--gap-3) + var(--safe-bottom));
  background: linear-gradient(180deg, rgba(22, 17, 15, 0), var(--ink-800) 35%);
}

@media (min-width: 48rem) {
  .masthead__inner {
    grid-template-columns: 1fr 18rem;
    align-items: center;
  }

  .masthead__board {
    max-width: none;
  }

  .cta {
    position: static;
    padding: 0 0 var(--gap-7);
  }

  .cta .btn {
    width: auto;
  }
}
</style>
