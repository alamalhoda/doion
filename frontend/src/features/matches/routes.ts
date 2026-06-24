import type { RouteRecordRaw } from 'vue-router'
import { ROUTES } from '@/constants/routes'
import UserLayout from '@/layouts/UserLayout.vue'
import MatchesListView from './views/MatchesListView.vue'
import MatchDetailView from './views/MatchDetailView.vue'

export const matchRoutes: RouteRecordRaw[] = [
  {
    path: ROUTES.USER_MATCHES,
    component: UserLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        component: MatchesListView,
      },
      {
        path: ':id',
        component: MatchDetailView,
      },
    ],
  },
]
