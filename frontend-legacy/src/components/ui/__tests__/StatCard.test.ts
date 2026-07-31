import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import StatCard from '../StatCard.vue'

describe('StatCard', () => {
  it('renders title and value', () => {
    const wrapper = mount(StatCard, { props: { title: 'Published', value: 5 } })
    expect(wrapper.text()).toContain('Published')
    expect(wrapper.text()).toContain('5')
  })

  it('applies the variant modifier class', () => {
    const wrapper = mount(StatCard, {
      props: { title: 'X', value: 1, variant: 'success' },
    })
    expect(wrapper.find('.stat-card--success').exists()).toBe(true)
  })

  it('applies the trend modifier class', () => {
    const wrapper = mount(StatCard, {
      props: { title: 'X', value: 1, trend: 'up' },
    })
    expect(wrapper.find('.stat-card--trend-up').exists()).toBe(true)
  })

  it('renders the icon slot when provided', () => {
    const wrapper = mount(StatCard, {
      props: { title: 'X', value: 1, icon: '🔥' },
    })
    expect(wrapper.find('.stat-card__icon').exists()).toBe(true)
    expect(wrapper.text()).toContain('🔥')
  })
})
