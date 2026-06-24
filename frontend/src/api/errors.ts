import type { NormalizedError } from './types'

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
    const response = error.response as { status: number; data?: Record<string, unknown> }
    const status = response.status

    const data = response.data || {}

    // Check for new backend envelope format: {error:{code,message,details}}
    if (data.error && typeof data.error === 'object') {
      const errorEnvelope = data.error as { code?: string; message?: string; details?: Record<string, unknown> }
      const normalized: NormalizedError = {
        code: (errorEnvelope.code as NormalizedError['code']) || 'UNKNOWN',
        message: errorEnvelope.message || 'error.unknown',
        status,
        raw: error,
      }
      // Handle fieldErrors in details if present
      if (errorEnvelope.details && typeof errorEnvelope.details === 'object') {
        const fieldErrors: Record<string, string[]> = {}
        Object.entries(errorEnvelope.details).forEach(([key, value]) => {
          if (Array.isArray(value)) {
            fieldErrors[key] = value as string[]
          } else if (typeof value === 'string') {
            fieldErrors[key] = [value]
          }
        })
        if (Object.keys(fieldErrors).length > 0) {
          normalized.fieldErrors = fieldErrors
        }
      }
      return normalized
    }

    // Validation error (422)
    if (status === 422 || (status === 400 && data?.non_field_errors === undefined)) {
      const fieldErrors: Record<string, string[]> = {}

      Object.entries(data).forEach(([key, value]) => {
        if (key === 'error') return // Skip error envelope key
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
      message: typeof data.detail === 'string' ? data.detail : 'error.unknown',
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
  response: { results?: T[]; data?: T[]; count?: number; next?: string | null; previous?: string | null },
): { items: T[]; total: number; next: string | null; previous: string | null } {
  return {
    items: response.results || response.data || [],
    total: response.count || 0,
    next: response.next || null,
    previous: response.previous || null,
  }
}
