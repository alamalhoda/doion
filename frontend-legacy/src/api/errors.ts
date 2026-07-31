import type { NormalizedError } from './types'

export function normalizeApiError(error: unknown): NormalizedError {
  if (!error || typeof error !== 'object') {
    return {
      code: 'UNKNOWN',
      message: 'error.unknown',
      raw: error,
    }
  }

  if ('response' in error && error.response) {
    const response = error.response as { status: number; data?: Record<string, unknown> }
    const status = response.status
    const data = response.data || {}

    // Contract envelope: { error: { code, message, details? } }
    if (data.error && typeof data.error === 'object') {
      const errorEnvelope = data.error as {
        code?: string
        message?: string
        details?: Record<string, unknown> | Array<{ field?: string; code?: string; message?: string }>
      }
      const normalized: NormalizedError = {
        code: (errorEnvelope.code as NormalizedError['code']) || 'UNKNOWN',
        message: errorEnvelope.message || 'error.unknown',
        status,
        raw: error,
      }

      if (errorEnvelope.details) {
        const fieldErrors: Record<string, string[]> = {}
        if (Array.isArray(errorEnvelope.details)) {
          errorEnvelope.details.forEach((detail) => {
            const key = detail.field || 'non_field_errors'
            const msg = detail.message || detail.code || 'Invalid'
            if (!fieldErrors[key]) fieldErrors[key] = []
            fieldErrors[key].push(msg)
          })
        } else if (typeof errorEnvelope.details === 'object') {
          Object.entries(errorEnvelope.details).forEach(([key, value]) => {
            if (Array.isArray(value)) {
              fieldErrors[key] = value.map(String)
            } else if (typeof value === 'string') {
              fieldErrors[key] = [value]
            }
          })
        }
        if (Object.keys(fieldErrors).length > 0) {
          normalized.fieldErrors = fieldErrors
        }
      }
      return normalized
    }

    // Legacy DRF flat field errors
    if (status === 400 || status === 422) {
      const fieldErrors: Record<string, string[]> = {}
      Object.entries(data).forEach(([key, value]) => {
        if (key === 'error') return
        if (Array.isArray(value)) {
          fieldErrors[key] = value as string[]
        } else if (typeof value === 'string') {
          fieldErrors[key] = [value]
        }
      })
      return {
        code: 'VALIDATION_ERROR',
        message: 'error.validation_error',
        fieldErrors: Object.keys(fieldErrors).length ? fieldErrors : undefined,
        status,
        raw: error,
      }
    }

    if (status === 401) {
      return {
        code: 'AUTHENTICATION_ERROR',
        message: 'error.unauthenticated',
        status,
        raw: error,
      }
    }

    if (status === 403) {
      return {
        code: 'PERMISSION_ERROR',
        message: 'error.forbidden',
        status,
        raw: error,
      }
    }

    if (status === 404) {
      return {
        code: 'NOT_FOUND_ERROR',
        message: typeof data.detail === 'string' ? data.detail : 'error.not_found',
        status,
        raw: error,
      }
    }

    return {
      code: 'SERVER_ERROR',
      message: typeof data.detail === 'string' ? data.detail : 'error.unknown',
      status,
      raw: error,
    }
  }

  if ('message' in error && error.message === 'Network Error') {
    return {
      code: 'NETWORK_ERROR',
      message: 'error.network_error',
      raw: error,
    }
  }

  // Already-normalized error
  if ('code' in error && 'message' in error) {
    return error as NormalizedError
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
