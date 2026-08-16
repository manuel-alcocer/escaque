import { createPinia } from 'pinia'
import { createApp } from 'vue'

import App from './App.vue'
import { router } from './router'
import './assets/design.css'
import './assets/board.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')

// The API client fires this when a refresh token is finally rejected.
window.addEventListener('escaque:signed-out', () => {
  if (router.currentRoute.value.name !== 'login') {
    router.push({ name: 'login' })
  }
})
