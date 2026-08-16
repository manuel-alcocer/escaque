<script setup>
/**
 * Stockfish analysis for a finished exercise.
 *
 * The engine lives in its own container and is optional: if it is not answering,
 * this panel says so plainly and everything else on the page keeps working.
 */
import { onMounted, ref, watch } from 'vue'

import { api } from '@/api/client'
import { formatScore, toSpanish } from '@/lib/notation'
import { useProgressStore } from '@/stores/progress'

const props = defineProps({
  fen: { type: String, required: true },
  movetime: { type: Number, default: 900 },
  multipv: { type: Number, default: 3 },
})

const progress = useProgressStore()
const analysis = ref(null)
const loading = ref(false)
const unavailable = ref(false)

async function analyse() {
  loading.value = true
  unavailable.value = false
  try {
    const { data } = await api.post('engine/analyse/', {
      fen: props.fen,
      movetime: props.movetime,
      multipv: props.multipv,
    })
    analysis.value = data
    progress.engine.available = true
  } catch (error) {
    unavailable.value = true
    if (error?.response?.status === 503) progress.engine.available = false
  } finally {
    loading.value = false
  }
}

/** Score is always shown from White's point of view, as engines report it. */
function lineLabel(line) {
  return formatScore(line.score_cp, line.mate_in)
}

function lineMoves(line) {
  return line.moves_san.slice(0, 6).map(toSpanish).join(' ')
}

onMounted(analyse)
watch(() => props.fen, analyse)
</script>

<template>
  <section class="engine panel">
    <header class="engine__head">
      <p class="eyebrow">Análisis</p>
      <p v-if="analysis" class="engine__meta mono">
        {{ analysis.engine }} · profundidad {{ analysis.depth }}
      </p>
    </header>

    <p v-if="loading" class="engine__state" role="status">Pensando…</p>

    <div v-else-if="unavailable" class="engine__state engine__state--off">
      <p>El motor no responde. El entrenamiento funciona igual; sólo falta el análisis.</p>
      <button type="button" class="btn btn--quiet" @click="analyse">Reintentar</button>
    </div>

    <ol v-else-if="analysis?.lines.length" class="engine__lines">
      <li v-for="line in analysis.lines" :key="line.rank" class="engine__line">
        <span class="engine__score mono" :class="{ 'engine__score--best': line.rank === 1 }">
          {{ lineLabel(line) }}
        </span>
        <span class="engine__moves mono">{{ lineMoves(line) }}</span>
      </li>
    </ol>

    <p v-else class="engine__state">No hay jugadas que analizar en esta posición.</p>
  </section>
</template>

<style scoped>
.engine {
  padding: var(--gap-3);
}

.engine__head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: var(--gap-2);
  margin-bottom: var(--gap-3);
}

.engine__meta {
  margin: 0;
  font-size: 0.625rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--bone-faint);
}

.engine__state {
  margin: 0;
  font-size: 0.875rem;
  color: var(--bone-dim);
}

.engine__state--off {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--gap-2);
}

.engine__lines {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: var(--gap-2);
}

.engine__line {
  display: grid;
  grid-template-columns: 3.5rem 1fr;
  gap: var(--gap-3);
  align-items: baseline;
  font-size: 0.8125rem;
}

.engine__score {
  font-weight: 700;
  color: var(--bone-dim);
  text-align: right;
}

.engine__score--best {
  color: var(--brass);
}

.engine__moves {
  color: var(--bone-dim);
  line-height: 1.45;
  overflow-wrap: anywhere;
}
</style>
