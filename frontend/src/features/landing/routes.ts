import type { RouteRecordRaw } from 'vue-router'
import LandingView from './views/LandingView.vue'
import { ROUTES } from '@/constants/routes'

export const landingRoutes: RouteRecordRaw[] = [
  {
    path: ROUTES.LANDING,
    component: LandingView,
    meta: { public: true },
  },
]