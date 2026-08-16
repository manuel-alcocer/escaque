<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import AppHeader from '@/components/AppHeader.vue'
import TabBar from '@/components/TabBar.vue'
import { useAuthStore } from '@/stores/auth'
import { useProgressStore } from '@/stores/progress'

const route = useRoute()
const auth = useAuthStore()
const progress = useProgressStore()
const booted = ref(false)

// Routes that own the whole screen (login, the exercise runner) opt out of chrome.
const showChrome = computed(() => route.meta.chrome !== false && auth.isSignedIn)

onMounted(async () => {
  const restored = await auth.restore()
  if (restored) progress.checkEngine()
  booted.value = true
})
</script>

<template>
  <div class="app" :class="{ 'app--chrome': showChrome }">
    <AppHeader v-if="showChrome" />

    <main class="app__main">
      <RouterView v-if="booted" v-slot="{ Component }">
        <component :is="Component" />
      </RouterView>
      <div v-else class="app__boot" role="status">
        <p class="eyebrow">Escaque</p>
        <p class="app__boot-text">Cargando…</p>
      </div>
    </main>

    <TabBar v-if="showChrome" />
  </div>
</template>

<style scoped>
.app {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
}

.app__main {
  flex: 1;
}

/* Room for the fixed bottom bar plus the phone's home indicator. */
.app--chrome .app__main {
  padding-bottom: calc(var(--tabbar) + var(--safe-bottom) + var(--gap-5));
}

@media (min-width: 48rem) {
  .app--chrome .app__main {
    padding-bottom: var(--gap-7);
  }
}

.app__boot {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--gap-2);
  min-height: 60dvh;
}

.app__boot-text {
  color: var(--bone-faint);
  margin: 0;
}
</style>
