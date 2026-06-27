import type { RouteRecordRaw } from 'vue-router'
import { ROUTES } from '@/constants/routes'
import AdminLayout from '@/layouts/AdminLayout.vue'
import UserLayout from '@/layouts/UserLayout.vue'
import AdminDashboardView from './views/AdminDashboardView.vue'
import UserDashboardView from './views/UserDashboardView.vue'

export const dashboardRoutes: RouteRecordRaw[] = [
  {
    path: ROUTES.ADMIN_DASHBOARD,
    component: AdminLayout,
    meta: { requiresAdmin: true },
    children: [
      {
        path: '',
        component: AdminDashboardView,
      },
    ],
  },
  {
    path: ROUTES.USER_DASHBOARD,
    component: UserLayout,
    meta: { requiresUser: true },
    children: [
      {
        path: '',
        component: UserDashboardView,
      },
    ],
  },
]
