import axios from 'axios'
import { appConfig } from '@/config/app'

export const apiClient = axios.create({
  baseURL: appConfig.apiBaseUrl,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Set auth token from sessionStorage when available
const token = sessionStorage.getItem('auth_token')
if (token) {
  apiClient.defaults.headers.common['Authorization'] = `Token ${token}`
}

export default apiClient
