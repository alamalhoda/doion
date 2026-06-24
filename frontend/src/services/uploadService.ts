import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'

export class UploadService {
  static async uploadFile(file: File): Promise<{ url: string }> {
    try {
      const formData = new FormData()
      formData.append('file', file)

      // TODO: Replace with actual upload endpoint
      const response = await apiClient.post<{ url: string }>('/api/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      return { url: response.data.url }
    } catch (error) {
      throw normalizeApiError(error)
    }
  }
}
