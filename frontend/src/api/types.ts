export interface ApiError {
  code: string
  message: string
  fieldErrors?: Record<string, string[]>
  status?: number
  raw?: unknown
}

import type { DomainErrorCode } from './errorCodes'

export interface NormalizedError extends ApiError {
  code:
    | DomainErrorCode
    | 'VALIDATION_ERROR'
    | 'AUTHENTICATION_ERROR'
    | 'PERMISSION_ERROR'
    | 'NOT_FOUND_ERROR'
    | 'SERVER_ERROR'
    | 'MOD_306'
    | 'NETWORK_ERROR'
    | 'UNKNOWN'
}

export interface ListResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
  unread_count?: number
}

export interface PaginationParams {
  page?: number
  /** Only supported on GET /compliance/audit/ (max 100). Most lists ignore this. */
  page_size?: number
  ordering?: string
}
