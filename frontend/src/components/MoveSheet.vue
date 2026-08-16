<script setup>
/**
 * The score sheet: numbered rows, one line per move pair, in Spanish notation.
 * Moves are clickable when the parent passes a handler, so the user can walk
 * back through a line after an exercise ends.
 */
import { computed } from 'vue'

import { toMovePairs } from '@/lib/notation'

const props = defineProps({
  movesSan: { type: Array, default: () => [] },
  startPly: { type: Number, default: 0 },
  activeIndex: { type: Number, default: -1 },
  selectable: { type: Boolean, default: false },
  emptyText: { type: String, default: 'Sin jugadas todavía.' },
})

const emit = defineEmits(['select'])

const rows = computed(() => toMovePairs(props.movesSan, props.startPly))

function pick(index) {
  if (props.selectable && index !== null) emit('select', index)
}
</script>

<template>
  <div class="sheet">
    <p v-if="!rows.length" class="sheet__empty">{{ emptyText }}</p>
    <ol v-else class="sheet__list mono">
      <li v-for="row in rows" :key="row.number" class="sheet__row">
        <span class="sheet__number">{{ row.number }}</span>
        <component
          :is="selectable && row.whiteIndex !== null ? 'button' : 'span'"
          class="sheet__move"
          :class="{ 'sheet__move--active': activeIndex === row.whiteIndex && row.whiteIndex !== null }"
          :type="selectable && row.whiteIndex !== null ? 'button' : undefined"
          @click="pick(row.whiteIndex)"
        >
          {{ row.white || '…' }}
        </component>
        <component
          :is="selectable && row.blackIndex !== null ? 'button' : 'span'"
          class="sheet__move"
          :class="{ 'sheet__move--active': activeIndex === row.blackIndex && row.blackIndex !== null }"
          :type="selectable && row.blackIndex !== null ? 'button' : undefined"
          @click="pick(row.blackIndex)"
        >
          {{ row.black }}
        </component>
      </li>
    </ol>
  </div>
</template>

<style scoped>
.sheet__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  /* Two pairs per row on a phone, four once there is space. */
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0 var(--gap-4);
  font-size: 0.8125rem;
}

.sheet__row {
  display: grid;
  grid-template-columns: 1.6rem 1fr 1fr;
  align-items: baseline;
  gap: var(--gap-1);
  padding: 0.15rem 0;
  border-bottom: 1px solid var(--line-soft);
}

.sheet__number {
  color: var(--bone-faint);
  font-size: 0.6875rem;
  text-align: right;
  padding-right: 0.25rem;
}

.sheet__move {
  text-align: left;
  padding: 0.1rem 0.25rem;
  border-radius: 2px;
  color: var(--bone);
  background: none;
  border: none;
  font: inherit;
}

button.sheet__move {
  cursor: pointer;
}

button.sheet__move:hover {
  background: var(--ink-600);
  color: var(--brass-bright);
}

.sheet__move--active {
  background: var(--brass-dim);
  color: var(--bone);
}

.sheet__empty {
  color: var(--bone-faint);
  font-size: 0.875rem;
  font-style: italic;
  margin: 0;
}

@media (min-width: 30rem) {
  .sheet__list {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (min-width: 48rem) {
  .sheet__list {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}
</style>
