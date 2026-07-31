import type { RouteRecordRaw } from 'vue-router'
import { ROUTES } from '@/constants/routes'
import WorkflowPrototypeView from './views/WorkflowPrototypeView.vue'

export const workflowRoutes: RouteRecordRaw[] = [
  {
    path: ROUTES.WORKFLOW_PROTOTYPE,
    component: WorkflowPrototypeView,
    meta: { public: true },
  },
]
