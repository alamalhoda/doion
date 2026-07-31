import { useToast } from './useToast'
import { normalizeApiError } from '@/api/errors'
import { DOMAIN_ERROR_CODES, type DomainErrorCode } from '@/api/errorCodes'
import type { NormalizedError } from '@/api/types'
import type { Ref } from 'vue'

export interface ErrorHandlerOptions {
  fallbackMessage?: string
  toastDuration?: number
}

export function useErrorHandler() {
  const toast = useToast()

  function getErrorMessage(error: unknown, options?: ErrorHandlerOptions): string {
    const fallback = options?.fallbackMessage || 'error.unknown'

    let normalized: NormalizedError
    if (error && typeof error === 'object' && 'code' in error && 'message' in error) {
      normalized = error as NormalizedError
    } else {
      normalized = normalizeApiError(error)
    }

    const code = normalized.code as string
    const domainCode = DOMAIN_ERROR_CODES[code]

    if (domainCode) {
      const locale = document.documentElement.lang || 'en'
      return locale === 'fa' ? domainCode.persianMessage : domainCode.englishMessage
    }

    return normalized.message || fallback
  }

  function handleError(error: unknown, options?: ErrorHandlerOptions): void {
    const message = getErrorMessage(error, options)
    toast.showToast(message, 'error', options?.toastDuration ?? 4000)
  }

  return {
    getErrorMessage,
    handleError,
  }
}
