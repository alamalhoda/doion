import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './plugins/pinia'
import i18n, { setupI18n } from './plugins/i18n'
import setupNaiveUI from './plugins/naive-ui'
import { setupDayjs } from './utils/date'
import { setupInterceptors } from './api/interceptors'
import { useAuthStore } from './features/auth/stores/authStore'

// Styles
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
await authStore.restoreAuth()

app.mount('#app')
