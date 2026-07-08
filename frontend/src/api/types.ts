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
    | 'FORBIDDEN'
    | 'UNAUTHENTICATED'
    | 'NETWORK_ERROR'
    | 'UNKNOWN'
}

export interface ListResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface PaginationParams {
  page?: number
  page_size?: number
  ordering?: string
}
