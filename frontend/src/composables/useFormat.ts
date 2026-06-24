export function useFormat() {
  function formatCurrency(value: number, currency = 'IRR'): string {
    return new Intl.NumberFormat('fa-IR', {
      style: 'currency',
      currency,
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }

  function formatPersianNumber(value: number | string): string {
    const numStr = String(value).replace(/[0-9]/g, (d) => String.fromCharCode(d.charCodeAt(0) + 1728))
    return numStr
  }

  function formatNumber(value: number, locale = 'fa-IR'): string {
    return new Intl.NumberFormat(locale).format(value)
  }

  return {
    formatCurrency,
    formatPersianNumber,
    formatNumber,
  }
}