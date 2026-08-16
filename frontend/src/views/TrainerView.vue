<script setup>
/**
 * The exercise runner.
 *
 * The board is the screen. Everything else is a thin strip above it (what to do)
 * and a fixed bar below it (what you can do about it), so on a phone the whole
 * interaction happens without scrolling and within thumb reach.
 *
 * Correctness is never decided here. Every move goes to the server, which knows
 * the line; this view only plays back what it is told and shows the verdict.
 */
import { Chess } from 'chess.js'
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { api, errorMessage } from '@/api/client'
import ChessBoard from '@/components/ChessBoard.vue'
import EnginePanel from '@/components/EnginePanel.vue'
import MoveSheet from '@/components/MoveSheet.vue'
import { renderInline } from '@/lib/markdown'
import { DIFFICULTY_LABELS, KIND_LABELS, toSpanish } from '@/lib/notation'
import { useProgressStore } from '@/stores/progress'

const route = useRoute()
const router = useRouter()
const progress = useProgressStore()

const queue = ref([])
const index = ref(0)
const loading = ref(true)
const loadError = ref('')
const submitting = ref(false)

const game = ref(null)
const fen = ref('')
const lastMove = ref([])
const playedSan = ref([])
const userMoves = ref([])

const outcome = ref(null) // null | 'solved' | 'failed'
const feedback = ref(null)
const hint = ref('')
const hintsUsed = ref(0)
const showEngine = ref(false)
let startedAt = 0

const exercise = computed(() => queue.value[index.value] || null)
const remaining = computed(() => Math.max(queue.value.length - index.value - 1, 0))
const finished = computed(() => outcome.value !== null)

const scope = computed(() => {
  const { opening, variation, kind } = route.query
  return { opening, variation_slug: variation, kind }
})

const scopeLabel = computed(() => {
  if (!exercise.value) return 'Entrenamiento'
  return route.query.variation ? exercise.value.variation_name : exercise.value.opening_name
})

async function loadQueue() {
  loading.value = true
  loadError.value = ''
  try {
    const { data } = await api.get('exercises/queue/', {
      params: { ...scope.value, limit: 24 },
    })
    queue.value = data.results
    index.value = 0
    if (queue.value.length) setUp()
  } catch (error) {
    loadError.value = errorMessage(error, 'No se han podido cargar los ejercicios.')
  } finally {
    loading.value = false
  }
}

/** Reset every per-exercise piece of state. Called on load and on "retry". */
function setUp() {
  const current = exercise.value
  if (!current) return
  game.value = new Chess(current.fen)
  fen.value = current.fen
  lastMove.value = []
  playedSan.value = []
  userMoves.value = []
  outcome.value = null
  feedback.value = null
  hint.value = ''
  hintsUsed.value = 0
  showEngine.value = false
  startedAt = Date.now()
}

async function onMove({ from, to, promotion }) {
  if (finished.value || submitting.value) return

  let move
  try {
    move = game.value.move({ from, to, promotion: promotion || 'q' })
  } catch {
    return
  }
  if (!move) return

  // Show the user's move immediately; the verdict arrives a moment later.
  fen.value = game.value.fen()
  lastMove.value = [move.from, move.to]
  playedSan.value = [...playedSan.value, move.san]
  userMoves.value = [...userMoves.value, move.from + move.to + (move.promotion || '')]

  await submit()
}

async function submit(extra = {}) {
  submitting.value = true
  try {
    const { data } = await api.post(`exercises/${exercise.value.id}/attempt/`, {
      moves: userMoves.value,
      duration_ms: Date.now() - startedAt,
      hints_used: hintsUsed.value,
      ...extra,
    })
    applyResult(data)
  } catch (error) {
    feedback.value = { tone: 'error', text: errorMessage(error, 'No se ha podido comprobar la jugada.') }
    // Roll the board back so the position always matches what the server knows.
    undoLastUserMove()
  } finally {
    submitting.value = false
  }
}

function undoLastUserMove() {
  if (!userMoves.value.length) return
  game.value.undo()
  fen.value = game.value.fen()
  playedSan.value = playedSan.value.slice(0, -1)
  userMoves.value = userMoves.value.slice(0, -1)
  const history = game.value.history({ verbose: true })
  lastMove.value = history.length ? [history.at(-1).from, history.at(-1).to] : []
}

function applyResult(data) {
  const result = data.result

  if (result.status === 'in_progress') {
    if (result.reply_uci) playOpponent(result.reply_uci)
    feedback.value = { tone: 'good', text: 'Correcto. Sigue la línea.' }
    return
  }

  outcome.value = result.status
  progress.invalidate()

  if (result.status === 'solved') {
    feedback.value = {
      tone: 'solved',
      text: result.truncated ? 'Correcto. Has elegido una alternativa válida.' : 'Resuelto.',
      explanation: data.explanation,
    }
  } else {
    feedback.value = {
      tone: 'failed',
      text: `La jugada era ${toSpanish(result.expected_san)}.`,
      explanation: data.explanation,
    }
    showSolution(data.solution)
  }
}

/** Play the opponent's scripted reply with a short pause, so it reads as a move. */
function playOpponent(uci) {
  setTimeout(() => {
    try {
      const move = game.value.move({
        from: uci.slice(0, 2),
        to: uci.slice(2, 4),
        promotion: uci.slice(4) || undefined,
      })
      if (!move) return
      fen.value = game.value.fen()
      lastMove.value = [move.from, move.to]
      playedSan.value = [...playedSan.value, move.san]
    } catch {
      // A reply we cannot play means the position drifted; the server is the
      // authority, so leave the board where it is.
    }
  }, 320)
}

/** After a failure, rewind and replay the correct line on the board. */
function showSolution(solution) {
  if (!solution?.length) return
  const replay = new Chess(exercise.value.fen)
  const line = []
  solution.forEach((ply) => {
    try {
      const move = replay.move({
        from: ply.uci.slice(0, 2),
        to: ply.uci.slice(2, 4),
        promotion: ply.uci.slice(4) || undefined,
      })
      if (move) line.push(move)
    } catch {
      /* stop at the first move that does not fit */
    }
  })
  if (!line.length) return

  game.value = replay
  fen.value = replay.fen()
  lastMove.value = [line.at(-1).from, line.at(-1).to]
  playedSan.value = line.map((move) => move.san)
}

async function askHint() {
  if (hint.value) return
  try {
    const { data } = await api.get(`exercises/${exercise.value.id}/hint/`)
    hint.value = data.hint
    hintsUsed.value += 1
  } catch {
    hint.value = 'Este ejercicio no tiene pista.'
  }
}

async function giveUp() {
  if (finished.value) return
  await submit({ give_up: true })
}

function next() {
  if (index.value < queue.value.length - 1) {
    index.value += 1
    setUp()
  } else {
    loadQueue()
  }
}

function retry() {
  setUp()
}

function leave() {
  router.back()
}

/** Keyboard shortcuts for desktop: space advances, H asks for a hint. */
function onKey(event) {
  if (event.target.matches('input, textarea')) return
  if (event.code === 'Space' && finished.value) {
    event.preventDefault()
    next()
  }
  if (event.key === 'h' && !finished.value) askHint()
}

onMounted(() => {
  loadQueue()
  window.addEventListener('keydown', onKey)
})

onBeforeUnmount(() => window.removeEventListener('keydown', onKey))

watch(() => route.query, loadQueue)
</script>

<template>
  <div class="trainer">
    <header class="trainer__bar">
      <button type="button" class="trainer__back" @click="leave" aria-label="Volver">←</button>
      <p class="trainer__scope mono">
        <span v-if="exercise" class="trainer__eco">{{ exercise.eco || '—' }}</span>
        {{ scopeLabel }}
      </p>
      <p class="trainer__count mono">
        <span v-if="exercise">{{ index + 1 }}/{{ queue.length }}</span>
      </p>
    </header>

    <div v-if="loading" class="trainer__state" role="status">Preparando ejercicios…</div>

    <div v-else-if="loadError" class="trainer__state trainer__state--error" role="alert">
      <p>{{ loadError }}</p>
      <button type="button" class="btn" @click="loadQueue">Reintentar</button>
    </div>

    <div v-else-if="!exercise" class="trainer__state">
      <p class="eyebrow">Nada pendiente</p>
      <p>No quedan ejercicios con estos filtros. Prueba con otra apertura.</p>
      <RouterLink :to="{ name: 'home' }" class="btn">Volver al repertorio</RouterLink>
    </div>

    <template v-else>
      <div class="trainer__body">
      <div class="trainer__prompt">
        <p class="trainer__kind mono">
          {{ KIND_LABELS[exercise.kind] }} · {{ DIFFICULTY_LABELS[exercise.difficulty] }}
          <span v-if="exercise.status === 'failed'" class="chip chip--failed">Fallado antes</span>
        </p>
        <p class="trainer__task">{{ exercise.prompt }}</p>
      </div>

      <div class="trainer__board">
        <ChessBoard
          :fen="fen"
          :orientation="exercise.orientation"
          :last-move="lastMove"
          :interactive="!finished && !submitting"
          @move="onMove"
        />
      </div>

      <!-- Verdict band. Colour carries the meaning, text carries the detail. -->
      <div
        v-if="feedback"
        class="verdict"
        :class="`verdict--${feedback.tone}`"
        role="status"
        aria-live="polite"
      >
        <p class="verdict__headline">{{ feedback.text }}</p>
        <p v-if="feedback.explanation" class="verdict__detail" v-html="renderInline(feedback.explanation)"></p>
      </div>

      <p v-if="hint && !finished" class="hint">{{ hint }}</p>

      <section class="trainer__sheet">
        <p class="eyebrow eyebrow--quiet">
          {{ finished && outcome === 'failed' ? 'La línea correcta' : 'Tu partida' }}
        </p>
        <MoveSheet
          :moves-san="playedSan"
          :start-ply="exercise.side_to_move === 'white' ? 0 : 1"
          empty-text="Mueve una pieza para empezar."
        />
      </section>

      <section v-if="finished" class="trainer__analysis">
        <button
          v-if="!showEngine && progress.engine.available !== false"
          type="button"
          class="btn btn--quiet btn--block"
          @click="showEngine = true"
        >
          Analizar con Stockfish
        </button>
        <EnginePanel v-if="showEngine" :fen="fen" />
      </section>
      </div>

      <!-- Fixed action bar, inside the safe area. -->
      <div class="actions">
        <template v-if="!finished">
          <button type="button" class="btn" :disabled="Boolean(hint)" @click="askHint">
            {{ hint ? 'Pista dada' : 'Pista' }}
          </button>
          <button type="button" class="btn" :disabled="submitting" @click="giveUp">
            Ver solución
          </button>
        </template>
        <template v-else>
          <button v-if="outcome === 'failed'" type="button" class="btn" @click="retry">
            Repetir
          </button>
          <button type="button" class="btn btn--primary actions__grow" @click="next">
            {{ remaining ? `Siguiente (${remaining})` : 'Cargar más' }}
          </button>
        </template>
      </div>
    </template>
  </div>
</template>

<style scoped>
.trainer {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  padding-bottom: calc(4.25rem + var(--safe-bottom));
}

.trainer__bar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: grid;
  grid-template-columns: 2.5rem 1fr auto;
  align-items: center;
  gap: var(--gap-2);
  height: 3rem;
  padding-right: var(--gap-4);
  background: rgba(20, 16, 14, 0.95);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--line-soft);
}

.trainer__back {
  height: 3rem;
  font-size: 1.1rem;
  color: var(--bone-dim);
}

.trainer__scope {
  margin: 0;
  font-size: 0.75rem;
  color: var(--bone-dim);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.trainer__eco {
  color: var(--brass);
  font-weight: 600;
  margin-right: var(--gap-2);
}

.trainer__count {
  margin: 0;
  font-size: 0.75rem;
  color: var(--bone-faint);
}

.trainer__state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--gap-3);
  text-align: center;
  flex: 1;
  padding: var(--gap-6) var(--gap-4);
  color: var(--bone-dim);
}

.trainer__state--error {
  color: #e8bdb1;
}

/* The board is square, so on a tall phone it is capped by width and there is
 * height to spare. Centring the whole block uses that space instead of leaving
 * a hole under the move sheet. */
.trainer__body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.trainer__prompt {
  padding: var(--gap-3) var(--gap-4) var(--gap-2);
}

.trainer__kind {
  display: flex;
  align-items: center;
  gap: var(--gap-2);
  margin: 0 0 var(--gap-2);
  font-size: 0.625rem;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--bone-faint);
}

.trainer__task {
  margin: 0;
  font-size: 1.0625rem;
  line-height: 1.4;
  color: var(--bone);
  text-wrap: pretty;
}

/* The board is capped by viewport height too, so the action bar is always
 * visible on a phone without scrolling. */
.trainer__board {
  width: 100%;
  max-width: min(100%, 58dvh);
  margin: var(--gap-2) auto var(--gap-3);
  padding: 0 var(--gap-2);
}

.verdict {
  margin: 0 var(--gap-4) var(--gap-3);
  padding: var(--gap-3);
  border-left: 2px solid var(--line);
  background: var(--ink-700);
}

.verdict--good {
  border-left-color: var(--brass);
}

.verdict--solved {
  border-left-color: var(--sage);
  background: var(--sage-dim);
}

.verdict--failed {
  border-left-color: var(--rust);
  background: var(--rust-dim);
}

.verdict--error {
  border-left-color: var(--rust);
}

.verdict__headline {
  margin: 0;
  font-family: var(--font-display);
  font-variation-settings: 'wdth' 106;
  font-weight: 600;
  font-size: 0.9375rem;
  letter-spacing: 0.02em;
}

.verdict__detail {
  margin: var(--gap-2) 0 0;
  font-size: 0.9375rem;
  line-height: 1.5;
  color: #ddd2c2;
}

.verdict__detail :deep(strong) {
  color: var(--bone);
}

.hint {
  margin: 0 var(--gap-4) var(--gap-3);
  padding: var(--gap-2) var(--gap-3);
  border: 1px dashed var(--brass-dim);
  border-radius: var(--radius);
  font-size: 0.875rem;
  font-style: italic;
  color: var(--brass-bright);
}

.trainer__sheet {
  padding: 0 var(--gap-4) var(--gap-4);
}

.trainer__sheet .eyebrow {
  margin-bottom: var(--gap-2);
}

.trainer__analysis {
  padding: 0 var(--gap-4) var(--gap-5);
}

.actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 20;
  display: flex;
  gap: var(--gap-2);
  padding: var(--gap-3) var(--gap-4) calc(var(--gap-3) + var(--safe-bottom));
  background: rgba(20, 16, 14, 0.97);
  backdrop-filter: blur(10px);
  border-top: 1px solid var(--line-soft);
}

.actions .btn {
  flex: 1;
}

.actions__grow {
  flex: 2;
}

@media (min-width: 48rem) {
  .trainer {
    max-width: 44rem;
    margin: 0 auto;
    padding-bottom: var(--gap-7);
  }

  .trainer__board {
    max-width: min(100%, 32rem);
  }

  .actions {
    position: static;
    background: none;
    border-top: 0;
    padding: 0 var(--gap-4) var(--gap-6);
  }
}
</style>
