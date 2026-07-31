export function useFormat() {
  function toNumber(value: number | string | null | undefined): number {
    if (value == null || value === '') return 0
    const n = typeof value === 'number' ? value : Number(value)
    return Number.isFinite(n) ? n : 0
  }

  function formatCurrency(value: number | string, currency = 'IRR'): string {
    return new Intl.NumberFormat('fa-IR', {
      style: 'currency',
      currency,
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(toNumber(value))
  }

  function formatPersianNumber(value: number | string): string {
    const numStr = String(value).replace(/[0-9]/g, (d) => String.fromCharCode(d.charCodeAt(0) + 1728))
    return numStr
  }

  function formatNumber(value: number | string, locale = 'fa-IR'): string {
    return new Intl.NumberFormat(locale).format(toNumber(value))
  }

  return {
    formatCurrency,
    formatPersianNumber,
    formatNumber,
  }
}