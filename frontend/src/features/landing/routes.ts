import type { RouteRecordRaw } from 'vue-router'
import LandingView from './views/LandingView.vue'

export const landingRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    component: LandingView,
    meta: { public: true },
  },
]