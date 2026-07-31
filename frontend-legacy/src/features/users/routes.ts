import type { RouteRecordRaw } from 'vue-router'
import { ROUTES } from '@/constants/routes'
import UserLayout from '@/layouts/UserLayout.vue'
import ProfileView from './views/ProfileView.vue'

export const userRoutes: RouteRecordRaw[] = [
  {
    path: '/app/profile',
    component: UserLayout,
    meta: { requiresUser: true },
    children: [
      {
        path: '',
        component: ProfileView,
      },
    ],
  },
]
