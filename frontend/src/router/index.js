import { createRouter, createWebHistory } from 'vue-router'

import { tokens } from '@/api/client'

const routes = [
  {
    path: '/entrar',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: { public: true, chrome: false },
  },
  { path: '/', name: 'home', component: () => import('@/views/HomeView.vue') },
  {
    path: '/seccion/:slug',
    name: 'section',
    component: () => import('@/views/SectionView.vue'),
    props: true,
  },
  {
    path: '/apertura/:slug',
    name: 'opening',
    component: () => import('@/views/OpeningView.vue'),
    props: true,
  },
  {
    path: '/apertura/:openingSlug/:slug',
    name: 'variation',
    component: () => import('@/views/VariationView.vue'),
    props: true,
  },
  {
    path: '/entrenar',
    name: 'train',
    component: () => import('@/views/TrainerView.vue'),
    // The board owns the whole screen on a phone; the tab bar would steal it.
    meta: { chrome: false },
  },
  { path: '/progreso', name: 'progress', component: () => import('@/views/ProgressView.vue') },
  { path: '/cuenta', name: 'account', component: () => import('@/views/AccountView.vue') },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('@/views/NotFoundView.vue') },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, saved) {
    return saved || { top: 0 }
  },
})

router.beforeEach((to) => {
  if (to.meta.public) return true
  if (!tokens.access) {
    return { name: 'login', query: to.fullPath === '/' ? {} : { next: to.fullPath } }
  }
  return true
})
