import dayjs from 'dayjs'
import 'dayjs/locale/fa'
import 'dayjs/locale/en'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.extend(relativeTime)

export function setupDayjs(locale: string) {
  dayjs.locale(locale === 'fa' ? 'fa' : 'en')
}

export function formatDate(date: string | Date, format = 'YYYY-MM-DD'): string {
  return dayjs(date).format(format)
}

export function formatDateTime(date: string | Date, format = 'YYYY-MM-DD HH:mm'): string {
  return dayjs(date).format(format)
}

export function parseDate(dateString: string): Date {
  return dayjs(dateString).toDate()
}

export function isValidDate(date: string | Date): boolean {
  return dayjs(date).isValid()
}

export function getRelativeTime(date: string | Date): string {
  return dayjs(date).fromNow()
}
