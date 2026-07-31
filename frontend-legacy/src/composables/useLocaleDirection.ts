import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

export function useLocaleDirection() {
  const { locale } = useI18n()

  const direction = computed(() => (locale.value === 'fa' ? 'rtl' : 'ltr'))

  const isRTL = computed(() => direction.value === 'rtl')

  return {
    direction,
    isRTL,
  }
}
