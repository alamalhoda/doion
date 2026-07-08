import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useErrorHandler } from '../useErrorHandler'
import { DOMAIN_ERROR_CODES } from '@/api/errorCodes'

const showToast = vi.fn()

vi.mock('@/composables/useToast', () => ({
  useToast: () => ({
    showToast,
    success: vi.fn(),
    error: vi.fn(),
    info: vi.fn(),
    warning: vi.fn(),
  }),
}))

describe('useErrorHandler', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    document.documentElement.lang = 'en'
  })

  it('maps a domain code to its english message in the en locale', () => {
    const { getErrorMessage } = useErrorHandler()
    expect(getErrorMessage({ code: 'AUTH_001', message: '' })).toBe(
      DOMAIN_ERROR_CODES.AUTH_001.englishMessage,
    )
  })

  it('maps a domain code to its persian message in the fa locale', () => {
    document.documentElement.lang = 'fa'
    const { getErrorMessage } = useErrorHandler()
    expect(getErrorMessage({ code: 'LST_201', message: '' })).toBe(
      DOMAIN_ERROR_CODES.LST_201.persianMessage,
    )
  })

  it('falls back to the raw message for an unknown code', () => {
    const { getErrorMessage } = useErrorHandler()
    expect(getErrorMessage({ code: 'UNKNOWN_X', message: 'Custom msg' })).toBe(
      'Custom msg',
    )
  })

  it('uses the fallbackMessage option when the message is empty', () => {
    const { getErrorMessage } = useErrorHandler()
    expect(
      getErrorMessage({ code: 'UNKNOWN_X', message: '' }, { fallbackMessage: 'oops' }),
    ).toBe('oops')
  })

  it('handleError surfaces an error toast with the mapped message', () => {
    document.documentElement.lang = 'fa'
    const { handleError } = useErrorHandler()
    handleError({ code: 'KYC_101', message: '' })
    expect(showToast).toHaveBeenCalledWith(
      DOMAIN_ERROR_CODES.KYC_101.persianMessage,
      'error',
      expect.any(Number),
    )
  })
})
