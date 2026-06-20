import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { setupRouterGuards } from './guards'
import { authRoutes } from '@/features/auth/routes'
import { dashboardRoutes } from '@/features/dashboard/routes'
import { listingRoutes } from '@/features/listings/routes'
import { marketplaceRoutes } from '@/features/marketplace/routes'
import { matchRoutes } from '@/features/matches/routes'
import { notificationRoutes } from '@/features/notifications/routes'
import { workflowRoutes } from '@/features/workflow/routes'
import NotFoundView from '@/views/NotFoundView.vue'
import { ROUTES } from '@/constants/routes'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: ROUTES.LOGIN,
  },
  ...authRoutes,
  ...dashboardRoutes,
  ...listingRoutes,
  ...marketplaceRoutes,
  ...matchRoutes,
  ...notificationRoutes,
  ...workflowRoutes,
  {
    path: ROUTES.NOT_FOUND,
    component: NotFoundView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

setupRouterGuards(router)

export default router
