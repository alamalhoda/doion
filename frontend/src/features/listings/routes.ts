import type { RouteRecordRaw } from 'vue-router'
import { ROUTES } from '@/constants/routes'
import UserLayout from '@/layouts/UserLayout.vue'
import CreateListingView from './views/CreateListingView.vue'
import ListingsListView from './views/ListingsListView.vue'
import ListingDetailView from './views/ListingDetailView.vue'

export const listingRoutes: RouteRecordRaw[] = [
  {
    path: ROUTES.USER_CREATE_LISTING,
    component: UserLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        component: CreateListingView,
      },
    ],
  },
  {
    path: ROUTES.USER_LISTINGS,
    component: UserLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        component: ListingsListView,
      },
    ],
  },
  {
    path: ROUTES.USER_LISTING_DETAIL,
    component: UserLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        component: ListingDetailView,
        props: true,
      },
    ],
  },
]