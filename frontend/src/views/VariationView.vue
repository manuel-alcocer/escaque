<script setup>
import { computed, onMounted, ref, watch } from 'vue'

import { api, errorMessage } from '@/api/client'
import AutoBoard from '@/components/AutoBoard.vue'
import ChessBoard from '@/components/ChessBoard.vue'
import MarkdownBlock from '@/components/MarkdownBlock.vue'
import MoveSheet from '@/components/MoveSheet.vue'
import { toInlineLine } from '@/lib/notation'

const props = defineProps({
  openingSlug: { type: String, required: true },
  slug: { type: String, required: true },
})

const variation = ref(null)
const loading = ref(true)
const loadError = ref('')

const KIND_LABELS = {
  idea: 'Idea clave',
  plan: 'Plan típico',
  structure: 'Estructura',
  trap: 'Celada',
  warning: 'Error habitual',
  game: 'Partida modelo',
}

const progressLabel = computed(() => {
  if (!variation.value) return ''
  const { exercise_count: total, solved_count: solved, failed_count: failed } = variation.value
  if (!total) return 'Sin ejercicios'
  if (failed) return `${solved}/${total} resueltos · ${failed} fallidos`
  return `${solved}/${total} resueltos`
})

async function load() {
  loading.value = true
  loadError.value = ''
  try {
    const { data } = await api.get(`variations/${props.slug}/`, {
      params: { opening: props.openingSlug },
    })
    variation.value = data
  } catch (error) {
    loadError.value = errorMessage(error, 'No se ha encontrado esta variante.')
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => [props.openingSlug, props.slug], load)
</script>

<template>
  <div v-if="loading" class="shell state" role="status">Cargando…</div>
  <div v-else-if="loadError" class="shell state state--error" role="alert">{{ loadError }}</div>

  <article v-else class="variation">
    <nav class="shell crumb">
      <RouterLink :to="{ name: 'opening', params: { slug: variation.opening_slug } }" class="crumb__link">
        ← {{ variation.opening_name }}
      </RouterLink>
    </nav>

    <header class="shell head">
      <p class="eyebrow">{{ variation.eco || 'Sin código ECO' }}</p>
      <h1 class="head__title">{{ variation.name }}</h1>
      <p class="head__tagline">{{ variation.tagline }}</p>
    </header>

    <section class="shell board-block">
      <div class="board-block__board">
        <AutoBoard
          :moves-san="variation.moves_san"
          :orientation="variation.opening_colour"
          :interval-ms="820"
        />
      </div>
      <div class="board-block__sheet">
        <p class="eyebrow eyebrow--quiet">Línea completa</p>
        <MoveSheet :moves-san="variation.moves_san" />
      </div>
    </section>

    <section v-if="variation.idea" class="shell idea">
      <p class="eyebrow">La idea</p>
      <p class="idea__text">{{ variation.idea }}</p>
    </section>

    <section v-if="variation.description" class="shell section">
      <MarkdownBlock :source="variation.description" />
    </section>

    <section v-if="variation.theory_blocks.length" class="shell section">
      <ul class="blocks">
        <li v-for="block in variation.theory_blocks" :key="block.id" class="block">
          <p class="eyebrow">{{ KIND_LABELS[block.kind] || block.kind }}</p>
          <h2 class="block__title">{{ block.title }}</h2>

          <div class="block__grid">
            <div v-if="block.fen" class="block__board">
              <ChessBoard
                :fen="block.fen"
                :orientation="block.orientation"
                :highlight="block.highlight_squares"
              />
              <p v-if="block.moves_san.length" class="block__line mono">
                {{ toInlineLine(block.moves_san) }}
              </p>
            </div>
            <MarkdownBlock class="block__text" :source="block.body" />
          </div>
        </li>
      </ul>
    </section>

    <div class="cta">
      <div class="shell cta__inner">
        <p class="cta__status mono">{{ progressLabel }}</p>
        <RouterLink
          v-if="variation.exercise_count"
          :to="{ name: 'train', query: { variation: variation.slug, opening: variation.opening_slug } }"
          class="btn btn--primary btn--block"
        >
          Entrenar esta variante
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

.crumb {
  padding-top: var(--gap-4);
}

.crumb__link {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.06em;
  color: var(--bone-dim);
}

.crumb__link:hover {
  color: var(--brass);
}

.head {
  padding-top: var(--gap-4);
}

.head__title {
  font-size: clamp(1.75rem, 8vw, 2.75rem);
  margin: var(--gap-2) 0 var(--gap-3);
}

.head__tagline {
  margin: 0;
  color: var(--bone-dim);
  font-size: 1.0625rem;
  max-width: 34rem;
}

.board-block {
  padding-top: var(--gap-5);
  display: grid;
  gap: var(--gap-4);
}

.board-block__board {
  max-width: 22rem;
  width: 100%;
}

.idea {
  margin-top: var(--gap-6);
  border-left: 2px solid var(--brass);
  padding-top: var(--gap-1);
  padding-bottom: var(--gap-1);
}

.idea__text {
  margin: var(--gap-2) 0 0;
  font-size: 1.0625rem;
  font-style: italic;
  color: var(--bone);
  max-width: 34rem;
}

.section {
  padding-top: var(--gap-6);
}

.blocks {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: var(--gap-6);
}

.block {
  border-top: 1px solid var(--line-soft);
  padding-top: var(--gap-4);
}

.block__title {
  font-size: clamp(1.1rem, 4.5vw, 1.35rem);
  margin: var(--gap-2) 0 var(--gap-4);
}

.block__grid {
  display: grid;
  gap: var(--gap-4);
}

.block__board {
  max-width: 20rem;
  width: 100%;
}

.block__line {
  margin: var(--gap-2) 0 0;
  font-size: 0.6875rem;
  color: var(--bone-faint);
  line-height: 1.5;
}

.cta {
  position: sticky;
  bottom: 0;
  margin-top: var(--gap-6);
  padding: var(--gap-3) 0 calc(var(--gap-3) + var(--safe-bottom));
  background: linear-gradient(180deg, rgba(22, 17, 15, 0), var(--ink-800) 40%);
}

.cta__status {
  font-size: 0.6875rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--bone-faint);
  margin: 0 0 var(--gap-2);
}

@media (min-width: 48rem) {
  .board-block {
    grid-template-columns: 22rem 1fr;
    align-items: start;
    gap: var(--gap-6);
  }

  .block__grid {
    grid-template-columns: 20rem 1fr;
    align-items: start;
    gap: var(--gap-5);
  }

  .cta {
    position: static;
    background: none;
    padding-bottom: var(--gap-7);
  }

  .cta .btn {
    width: auto;
  }
}
</style>
