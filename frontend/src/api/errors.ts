import type { NormalizedError, ApiError } from './types'

export function normalizeApiError(error: unknown): NormalizedError {
  // Network error
  if (!error || typeof error !== 'object') {
    return {
      code: 'UNKNOWN',
      message: 'error.unknown',
      raw: error,
    }
  }

  // Axios error
  if ('response' in error && error.response) {
    const response = error.response as any
    const status = response.status

    // Validation error (422)
    if (status === 422 || (status === 400 && response.data?.non_field_errors === undefined)) {
      const fieldErrors: Record<string, string[]> = {}
      const data = response.data || {}

      Object.entries(data).forEach(([key, value]) => {
        if (Array.isArray(value)) {
          fieldErrors[key] = value as string[]
        } else if (typeof value === 'string') {
          fieldErrors[key] = [value]
        }
      })

      return {
        code: 'VALIDATION_ERROR',
        message: 'error.validation_error',
        fieldErrors,
        status,
        raw: error,
      }
    }

    // Unauthenticated (401)
    if (status === 401) {
      return {
        code: 'UNAUTHENTICATED',
        message: 'error.unauthenticated',
        status,
        raw: error,
      }
    }

    // Forbidden (403)
    if (status === 403) {
      return {
        code: 'FORBIDDEN',
        message: 'error.forbidden',
        status,
        raw: error,
      }
    }

    // Other HTTP errors
    return {
      code: 'UNKNOWN',
      message: response.data?.detail || 'error.unknown',
      status,
      raw: error,
    }
  }

  // Network error (no response)
  if ('message' in error && error.message === 'Network Error') {
    return {
      code: 'NETWORK_ERROR',
      message: 'error.network_error',
      raw: error,
    }
  }

  return {
    code: 'UNKNOWN',
    message: 'error.unknown',
    raw: error,
  }
}

export function normalizeListResponse<T>(
  response: any,
): { items: T[]; total: number; next: string | null; previous: string | null } {
  return {
    items: response.results || response.data || [],
    total: response.count || 0,
    next: response.next || null,
    previous: response.previous || null,
  }
}
