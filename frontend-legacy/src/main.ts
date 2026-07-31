import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './plugins/pinia'
import i18n, { setupI18n } from './plugins/i18n'
import setupNaiveUI from './plugins/naive-ui'
import { setupDayjs } from './utils/date'
import { setupInterceptors } from './api/interceptors'
import { useAuthStore } from './features/auth/stores/authStore'

// Styles — import order: tokens → theme → rtl → global
import './styles/tokens.css'
import './styles/themes/light.css'
import './styles/rtl.css'
import './styles/global.css'

const app = createApp(App)

// Setup plugins
app.use(pinia)
app.use(router)
setupI18n(app)
setupNaiveUI(app)

// Setup utilities
const locale = i18n.global.locale.value
setupDayjs(locale)

const authStore = useAuthStore()

// Setup API interceptors with auth store
setupInterceptors(authStore)

// Restore auth state before mount
console.log('[main] Starting restoreAuth...')
void authStore.restoreAuth().then(() => {
  console.log('[main] restoreAuth complete:', {
    isAuthenticated: authStore.isAuthenticated,
    user: authStore.user ? { username: authStore.user.username, role: authStore.user.role } : null,
  })
  app.mount('#app')
})
