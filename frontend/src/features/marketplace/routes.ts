import type { RouteRecordRaw } from 'vue-router'
import { ROUTES } from '@/constants/routes'
import UserLayout from '@/layouts/UserLayout.vue'
import MarketplaceView from './views/MarketplaceView.vue'

export const marketplaceRoutes: RouteRecordRaw[] = [
  {
    path: ROUTES.MARKETPLACE,
    component: UserLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        component: MarketplaceView,
      },
    ],
  },
]
