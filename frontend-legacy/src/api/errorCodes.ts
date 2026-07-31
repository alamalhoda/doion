/**
 * Domain-specific API error codes aligned with MASTER_API_CONTRACT.md.
 *
 * Envelope codes emitted by custom_exception_handler:
 * VALIDATION_ERROR | AUTHENTICATION_ERROR | PERMISSION_ERROR | NOT_FOUND_ERROR | SERVER_ERROR | MOD_306
 *
 * Spec-only labels (AUTH_*, LST_* as envelope codes) are not listed here.
 * KYC_101–104 may appear as free-form rejection_code payloads, not envelope codes.
 */
export interface DomainErrorInfo {
  message: string
  persianMessage: string
  englishMessage: string
}

export const DOMAIN_ERROR_CODES: Record<string, DomainErrorInfo> = {
  VALIDATION_ERROR: {
    message: 'error.validation_error',
    persianMessage: 'خطای اعتبارسنجی',
    englishMessage: 'Validation failed',
  },
  AUTHENTICATION_ERROR: {
    message: 'error.authentication_error',
    persianMessage: 'احراز هویت ناموفق',
    englishMessage: 'Authentication failed',
  },
  PERMISSION_ERROR: {
    message: 'error.permission_error',
    persianMessage: 'دسترسی مجاز نیست',
    englishMessage: 'Permission denied',
  },
  NOT_FOUND_ERROR: {
    message: 'error.not_found_error',
    persianMessage: 'یافت نشد',
    englishMessage: 'Not found',
  },
  SERVER_ERROR: {
    message: 'error.server_error',
    persianMessage: 'خطای سرور',
    englishMessage: 'An unexpected error occurred',
  },
  MOD_306: {
    message: 'error.mod_306_resubmit_limit',
    persianMessage: 'سقف ارسال مجدد آگهی پر شده است',
    englishMessage: 'Maximum resubmission limit exceeded',
  },
  // Free-form KYC rejection payload codes (not envelope codes)
  KYC_101: {
    message: 'error.kyc_101_unreadable_document',
    persianMessage: 'تصویر مدرک ناخوانا',
    englishMessage: 'Unreadable document image',
  },
  KYC_102: {
    message: 'error.kyc_102_mismatched_info',
    persianMessage: 'اطلاعات مغایرت دارد',
    englishMessage: 'Information mismatch',
  },
  KYC_103: {
    message: 'error.kyc_103_incomplete_documents',
    persianMessage: 'مدارک ناقص',
    englishMessage: 'Incomplete documents',
  },
  KYC_104: {
    message: 'error.kyc_104_already_registered',
    persianMessage: 'هویت قبلاً ثبت شده',
    englishMessage: 'Identity already registered',
  },
}

export type DomainErrorCode = keyof typeof DOMAIN_ERROR_CODES
