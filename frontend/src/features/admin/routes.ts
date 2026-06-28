import type { RouteRecordRaw } from 'vue-router'
import { ROUTES } from '@/constants/routes'
import AdminLayout from '@/layouts/AdminLayout.vue'

const ModerationQueueView = () => import('./views/ModerationQueueView.vue')
const ModerationDetailView = () => import('./views/ModerationDetailView.vue')

export const adminRoutes: RouteRecordRaw[] = [
  {
    path: ROUTES.ADMIN_MODERATION_QUEUE,
    component: AdminLayout,
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        name: 'admin-moderation-queue',
        component: ModerationQueueView,
      },
      {
        path: ':id',
        name: 'admin-moderation-detail',
        component: ModerationDetailView,
        props: true,
      },
    ],
  },
]
