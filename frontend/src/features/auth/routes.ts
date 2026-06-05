import type { RouteRecordRaw } from 'vue-router'
import { ROUTES } from '@/constants/routes'
import AuthLayout from '@/layouts/AuthLayout.vue'
import LoginView from './views/LoginView.vue'

export const authRoutes: RouteRecordRaw[] = [
  {
    path: ROUTES.LOGIN,
    component: AuthLayout,
    children: [
      {
        path: '',
        component: LoginView,
      },
    ],
  },
]
