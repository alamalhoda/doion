import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Skeleton from '../Skeleton.vue'

describe('Skeleton', () => {
  it('renders a single line by default', () => {
    const wrapper = mount(Skeleton)
    expect(wrapper.findAll('.skeleton__line')).toHaveLength(1)
  })

  it('renders the given number of lines', () => {
    const wrapper = mount(Skeleton, { props: { lines: 4 } })
    expect(wrapper.findAll('.skeleton__line')).toHaveLength(4)
  })

  it('applies a numeric width via style', () => {
    const wrapper = mount(Skeleton, { props: { width: 200 } })
    expect(wrapper.attributes('style')).toContain('200px')
  })
})
