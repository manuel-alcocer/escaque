<script setup>
/**
 * Interactive board.
 *
 * Legality is computed here with chess.js so the user can only ever attempt a
 * real move — but whether that move is *correct* is decided by the server. This
 * component reports moves and shows what it is told; it never judges an answer.
 */
import { Chessground } from 'chessground'
import { Chess } from 'chess.js'
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = defineProps({
  fen: { type: String, required: true },
  orientation: { type: String, default: 'white' },
  interactive: { type: Boolean, default: false },
  lastMove: { type: Array, default: () => [] },
  highlight: { type: Array, default: () => [] },
  flat: { type: Boolean, default: false },
  showCoordinates: { type: Boolean, default: true },
})

const emit = defineEmits(['move'])

const element = ref(null)
const promotion = ref(null)
let board = null

const FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

const coordinates = computed(() => {
  if (!props.showCoordinates) return []
  const flipped = props.orientation === 'black'
  const marks = []
  FILES.forEach((file, index) => {
    const column = flipped ? 7 - index : index
    marks.push({
      key: `f${file}`,
      text: file,
      style: { left: `${column * 12.5 + 0.6}%`, bottom: '1.5%' },
    })
  })
  for (let rank = 1; rank <= 8; rank += 1) {
    const row = flipped ? rank - 1 : 8 - rank
    marks.push({
      key: `r${rank}`,
      text: String(rank),
      style: { top: `${row * 12.5 + 1}%`, right: '1%' },
    })
  }
  return marks
})

function legalDestinations(fen) {
  const dests = new Map()
  try {
    const game = new Chess(fen)
    game.moves({ verbose: true }).forEach((move) => {
      const list = dests.get(move.from) || []
      list.push(move.to)
      dests.set(move.from, list)
    })
  } catch {
    // A malformed FEN just means no legal moves to offer.
  }
  return dests
}

function turnColour(fen) {
  return fen.split(' ')[1] === 'b' ? 'black' : 'white'
}

function isPromotion(from, to) {
  try {
    const game = new Chess(props.fen)
    return game
      .moves({ verbose: true })
      .some((move) => move.from === from && move.to === to && move.promotion)
  } catch {
    return false
  }
}

function handleMove(from, to) {
  if (isPromotion(from, to)) {
    promotion.value = { from, to, colour: turnColour(props.fen) }
    return
  }
  emit('move', { from, to, promotion: '' })
}

function choosePromotion(piece) {
  const pending = promotion.value
  promotion.value = null
  if (pending) emit('move', { from: pending.from, to: pending.to, promotion: piece })
}

/** Theory diagrams mark squares; chessground takes them as a class map. */
function highlightMap() {
  return new Map(props.highlight.map((square) => [square, 'highlight-square']))
}

function config() {
  const colour = turnColour(props.fen)
  return {
    fen: props.fen,
    orientation: props.orientation,
    turnColor: colour,
    coordinates: false, // Drawn in our own type below.
    viewOnly: !props.interactive,
    lastMove: props.lastMove.length ? props.lastMove : undefined,
    highlight: { lastMove: true, check: true, custom: highlightMap() },
    animation: { enabled: true, duration: 180 },
    movable: {
      free: false,
      color: props.interactive ? colour : undefined,
      dests: props.interactive ? legalDestinations(props.fen) : new Map(),
      showDests: true,
      events: { after: handleMove },
    },
    draggable: { enabled: props.interactive, showGhost: true },
    selectable: { enabled: props.interactive },
    drawable: { enabled: false, visible: true },
  }
}

onMounted(() => {
  board = Chessground(element.value, config())
})

onBeforeUnmount(() => {
  board?.destroy()
  board = null
})

watch(
  () => [props.fen, props.orientation, props.interactive, props.lastMove, props.highlight],
  (now, before) => {
    if (!board) return
    board.set(config())

    // Chessground binds the board's pointer listeners inside redrawAll(), and
    // bails out early when the board is viewOnly. Its set() calls redrawAll()
    // for an orientation change *before* applying the rest of the config, so a
    // board that was viewOnly and is now interactive gets redrawn while still
    // marked viewOnly and ends up with no listeners at all — silently dead.
    //
    // This is the exercise runner's normal flow: an exercise ends (viewOnly),
    // and the next one arrives interactive and often from the other side.
    // Redrawing once more, after the new config is in, rebinds them.
    const becameInteractive = now[2] && !before?.[2]
    if (becameInteractive) board.redrawAll()
  },
  { deep: true },
)

defineExpose({
  redraw: () => board?.redrawAll(),
})
</script>

<template>
  <div class="board-frame" :class="{ 'board-frame--flat': flat }">
    <div ref="element" class="board-mount"></div>

    <div v-if="showCoordinates" class="board-coords" aria-hidden="true">
      <span v-for="mark in coordinates" :key="mark.key" :style="mark.style">{{ mark.text }}</span>
    </div>

    <div v-if="promotion" class="promotion" role="dialog" aria-label="Elige pieza de promoción">
      <p class="eyebrow">Corona</p>
      <div class="promotion__options">
        <button
          v-for="option in [
            { code: 'q', label: 'Dama' },
            { code: 'r', label: 'Torre' },
            { code: 'b', label: 'Alfil' },
            { code: 'n', label: 'Caballo' },
          ]"
          :key="option.code"
          type="button"
          class="btn"
          @click="choosePromotion(option.code)"
        >
          {{ option.label }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.board-mount {
  width: 100%;
  height: 100%;
}

.promotion {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--gap-3);
  background: rgba(14, 11, 10, 0.92);
  padding: var(--gap-4);
}

.promotion__options {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--gap-2);
  width: 100%;
  max-width: 16rem;
}
</style>
