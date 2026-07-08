/**
 * Domain-specific API error codes with i18n-ready message keys.
 *
 * Each entry provides:
 * - `message`        : i18n key used by the backend/API contract
 * - `persianMessage` : fallback Persian text (used when i18n key is missing or for direct reference)
 * - `englishMessage` : fallback English text
 */
export interface DomainErrorInfo {
  message: string
  persianMessage: string
  englishMessage: string
}

export const DOMAIN_ERROR_CODES: Record<string, DomainErrorInfo> = {
  AUTH_001: {
    message: 'error.auth_001_invalid_code',
    persianMessage: 'کد تأیید نامعتبر',
    englishMessage: 'Invalid verification code',
  },
  AUTH_002: {
    message: 'error.auth_002_expired_code',
    persianMessage: 'کد تأیید منقضی شده',
    englishMessage: 'Verification code expired',
  },
  AUTH_003: {
    message: 'error.auth_003_rate_limit',
    persianMessage: 'تعداد تلاش بیش از حد',
    englishMessage: 'Too many attempts',
  },
  AUTH_004: {
    message: 'error.auth_004_token_expired',
    persianMessage: 'توکن منقضی شده',
    englishMessage: 'Token expired',
  },
  AUTH_005: {
    message: 'error.auth_005_account_suspended',
    persianMessage: 'حساب معلق است',
    englishMessage: 'Account suspended',
  },
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
  LST_201: {
    message: 'error.lst_201_amount_must_be_positive',
    persianMessage: 'مبلغ باید بیشتر از صفر باشد',
    englishMessage: 'Amount must be greater than zero',
  },
  LST_202: {
    message: 'error.lst_202_due_date_in_future',
    persianMessage: 'سررسید باید در آینده باشد',
    englishMessage: 'Due date must be in the future',
  },
  LST_203: {
    message: 'error.lst_203_sayad_code_length',
    persianMessage: 'کد صیاد باید ۱۶ رقم باشد',
    englishMessage: 'Sayad code must be 16 digits',
  },
  LST_204: {
    message: 'error.lst_204_duplicate_listing',
    persianMessage: 'این چک قبلاً ثبت شده',
    englishMessage: 'This cheque has already been registered',
  },
  LST_205: {
    message: 'error.lst_205_daily_limit',
    persianMessage: 'سقف ثبت آگهی روزانه',
    englishMessage: 'Daily listing limit reached',
  },
  LST_206: {
    message: 'error.lst_206_cheque_image_required',
    persianMessage: 'حداقل یک تصویر از چک الزامی است',
    englishMessage: 'At least one cheque image is required',
  },
  MOD_301: {
    message: 'error.mod_301_incomplete_info',
    persianMessage: 'اطلاعات چک ناقص',
    englishMessage: 'Incomplete cheque information',
  },
  MOD_302: {
    message: 'error.mod_302_unreadable_image',
    persianMessage: 'تصویر چک ناخوانا',
    englishMessage: 'Unreadable cheque image',
  },
  MOD_303: {
    message: 'error.mod_303_mismatch',
    persianMessage: 'عدم تطابق اطلاعات',
    englishMessage: 'Information mismatch',
  },
  MOD_304: {
    message: 'error.mod_304_invalid_content',
    persianMessage: 'محتوای غیرمجاز',
    englishMessage: 'Invalid content',
  },
  MOD_305: {
    message: 'error.mod_305_incomplete_issuer_docs',
    persianMessage: 'مدارک صادرکننده ناقص',
    englishMessage: 'Incomplete issuer documents',
  },
}

export type DomainErrorCode = keyof typeof DOMAIN_ERROR_CODES
