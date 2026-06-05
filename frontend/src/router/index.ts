import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { setupRouterGuards } from './guards'
import { authRoutes } from '@/features/auth/routes'
import { dashboardRoutes } from '@/features/dashboard/routes'
import NotFoundView from '@/views/NotFoundView.vue'
import { ROUTES } from '@/constants/routes'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: ROUTES.LOGIN,
  },
  ...authRoutes,
  ...dashboardRoutes,
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
