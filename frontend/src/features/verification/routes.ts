import type { RouteRecordRaw } from 'vue-router'
import { ROUTES } from '@/constants/routes'
import UserLayout from '@/layouts/UserLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import KycStep1View from './views/KycStep1View.vue'
import KycStep2View from './views/KycStep2View.vue'
import KycStatusView from './views/KycStatusView.vue'
import ModerationKycView from './views/ModerationKycView.vue'

export const verificationRoutes: RouteRecordRaw[] = [
  {
    path: ROUTES.VERIFICATION_KYC_START,
    component: UserLayout,
    meta: { requiresUser: true },
    children: [
      {
        path: '',
        component: KycStep1View,
        name: 'kyc-step-1',
      },
      {
        path: 'step-2',
        component: KycStep2View,
        name: 'kyc-step-2',
      },
    ],
  },
  {
    path: ROUTES.VERIFICATION_KYC_STATUS,
    component: UserLayout,
    meta: { requiresUser: true },
    children: [
      {
        path: '',
        component: KycStatusView,
        name: 'kyc-status',
      },
    ],
  },
  {
    path: ROUTES.VERIFICATION_MODERATION_QUEUE,
    component: AdminLayout,
    meta: { requiresUser: true, requiresAdmin: true },
    children: [
      {
        path: '',
        component: ModerationKycView,
        name: 'moderation-kyc',
      },
    ],
  },
]