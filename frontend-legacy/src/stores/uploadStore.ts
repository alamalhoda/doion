import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUploadStore = defineStore('upload', () => {
  const error = ref<string | null>(null)

  function setError(message: string) {
    error.value = message
  }

  function clearError() {
    error.value = null
  }

  return {
    error,
    setError,
    clearError,
  }
})