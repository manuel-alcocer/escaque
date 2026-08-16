<script setup>
import { onMounted, ref, watch } from 'vue'

import { api, errorMessage } from '@/api/client'
import AutoBoard from '@/components/AutoBoard.vue'

const props = defineProps({ slug: { type: String, required: true } })

const section = ref(null)
const loading = ref(true)
const loadError = ref('')

async function load() {
  loading.value = true
  loadError.value = ''
  try {
    const { data } = await api.get(`sections/${props.slug}/`)
    section.value = data
  } catch (error) {
    loadError.value = errorMessage(error, 'No se ha encontrado esta sección.')
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => props.slug, load)
</script>

<template>
  <div v-if="loading" class="shell state" role="status">Cargando…</div>
  <div v-else-if="loadError" class="shell state" role="alert">{{ loadError }}</div>

  <div v-else class="shell page">
    <header class="page__head">
      <p class="eyebrow">{{ section.openings.length }} aperturas</p>
      <h1>{{ section.name }}</h1>
      <p class="page__lede">{{ section.description || section.tagline }}</p>
    </header>

    <ul class="list">
      <li v-for="opening in section.openings" :key="opening.slug" class="list__item">
        <RouterLink :to="{ name: 'opening', params: { slug: opening.slug } }" class="list__link">
          <div class="list__board">
            <AutoBoard :moves-san="opening.moves_san" :orientation="opening.colour" />
          </div>
          <div>
            <p class="eyebrow">{{ opening.eco_range }}</p>
            <h2 class="list__name">{{ opening.name }}</h2>
            <p class="list__tagline">{{ opening.tagline }}</p>
          </div>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.state {
  padding: var(--gap-6) var(--gap-4);
  color: var(--bone-faint);
}

.page {
  padding-top: var(--gap-5);
}

.page__head {
  margin-bottom: var(--gap-5);
}

.page__head h1 {
  margin: var(--gap-2) 0 var(--gap-3);
}

.page__lede {
  color: var(--bone-dim);
  max-width: 36rem;
  margin: 0;
}

.list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: var(--gap-4);
}

.list__link {
  display: grid;
  grid-template-columns: 6rem 1fr;
  gap: var(--gap-4);
  padding: var(--gap-3);
  border: 1px solid var(--line-soft);
  border-radius: var(--radius);
  background: var(--ink-700);
}

.list__link:hover {
  border-color: var(--brass-dim);
}

.list__name {
  font-size: 1.1rem;
  margin: var(--gap-1) 0 var(--gap-2);
}

.list__tagline {
  margin: 0;
  font-size: 0.875rem;
  color: var(--bone-dim);
}

@media (min-width: 48rem) {
  .list {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
