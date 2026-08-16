<script setup>
/**
 * A board that plays its own line.
 *
 * This is the recurring gesture of the site: an opening is introduced by the
 * moves that define it, not by a description of them. It starts when it scrolls
 * into view — phones have no hover — and it holds the final position for a beat
 * before looping.
 *
 * With prefers-reduced-motion the line is not animated at all: the final
 * position is shown straight away, which is the same information without the
 * movement.
 */
import { Chess } from 'chess.js'
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

import ChessBoard from '@/components/ChessBoard.vue'
import { toSpanish } from '@/lib/notation'

const props = defineProps({
  movesSan: { type: Array, default: () => [] },
  orientation: { type: String, default: 'white' },
  intervalMs: { type: Number, default: 900 },
  holdMs: { type: Number, default: 2600 },
  loop: { type: Boolean, default: true },
  showLine: { type: Boolean, default: false },
})

const frames = computed(() => {
  const game = new Chess()
  const list = [{ fen: game.fen(), lastMove: [], san: '' }]
  for (const san of props.movesSan) {
    try {
      const move = game.move(san)
      if (!move) break
      list.push({ fen: game.fen(), lastMove: [move.from, move.to], san: move.san })
    } catch {
      break
    }
  }
  return list
})

const index = ref(0)
const container = ref(null)
const reduceMotion =
  typeof window !== 'undefined' &&
  window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

const current = computed(() => frames.value[Math.min(index.value, frames.value.length - 1)])
const playedSan = computed(() =>
  frames.value
    .slice(1, index.value + 1)
    .map((frame) => frame.san),
)

let timer = null
let observer = null

function stop() {
  if (timer) {
    clearTimeout(timer)
    timer = null
  }
}

function scheduleNext() {
  stop()
  const atEnd = index.value >= frames.value.length - 1
  if (atEnd && !props.loop) return
  const delay = atEnd ? props.holdMs : props.intervalMs
  timer = setTimeout(() => {
    index.value = atEnd ? 0 : index.value + 1
    scheduleNext()
  }, delay)
}

function start() {
  if (reduceMotion) {
    index.value = frames.value.length - 1
    return
  }
  scheduleNext()
}

onMounted(() => {
  if (reduceMotion || !('IntersectionObserver' in window)) {
    start()
    return
  }
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => (entry.isIntersecting ? start() : stop()))
    },
    { threshold: 0.35 },
  )
  observer.observe(container.value)
})

onBeforeUnmount(() => {
  stop()
  observer?.disconnect()
})

watch(
  () => props.movesSan,
  () => {
    index.value = 0
    if (!reduceMotion) scheduleNext()
  },
  { deep: true },
)
</script>

<template>
  <div ref="container" class="auto-board">
    <ChessBoard
      :fen="current.fen"
      :orientation="orientation"
      :last-move="current.lastMove"
      :show-coordinates="false"
    />
    <p v-if="showLine" class="auto-board__line mono">
      <span v-for="(san, i) in playedSan" :key="i">
        <template v-if="i % 2 === 0">{{ i / 2 + 1 }}.</template>{{ toSpanish(san) }}&nbsp;
      </span>
      <span v-if="!playedSan.length" class="auto-board__idle">posición inicial</span>
    </p>
  </div>
</template>

<style scoped>
.auto-board {
  display: flex;
  flex-direction: column;
  gap: var(--gap-2);
}

.auto-board__line {
  font-size: 0.75rem;
  color: var(--bone-dim);
  margin: 0;
  min-height: 1.2rem;
  line-height: 1.4;
}

.auto-board__idle {
  color: var(--bone-faint);
  font-style: italic;
}
</style>
