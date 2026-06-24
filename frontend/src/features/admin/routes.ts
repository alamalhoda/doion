import type { RouteRecordRaw } from 'vue-router'
import { ROUTES } from '@/constants/routes'
import AdminLayout from '@/layouts/AdminLayout.vue'
import ModerationQueueView from './views/ModerationQueueView.vue'

export const adminRoutes: RouteRecordRaw[] = [
  {
    path: ROUTES.ADMIN_MODERATION_QUEUE,
    component: AdminLayout,
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        component: ModerationQueueView,
      },
    ],
  },
]
