export interface ApiError {
  code: string
  message: string
  fieldErrors?: Record<string, string[]>
  status?: number
  raw?: unknown
}

export interface NormalizedError extends ApiError {
  code:
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
