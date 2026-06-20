import type { RouteRecordRaw } from 'vue-router'
import { ROUTES } from '@/constants/routes'
import UserLayout from '@/layouts/UserLayout.vue'
import NotificationsView from './views/NotificationsView.vue'

export const notificationRoutes: RouteRecordRaw[] = [
  {
    path: ROUTES.USER_NOTIFICATIONS,
    component: UserLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        component: NotificationsView,
      },
    ],
  },
]
