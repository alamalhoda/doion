import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import NotificationItem from '../components/NotificationItem.vue'
import type { Notification } from '../types/notification'

const mockNotification = (overrides: Partial<Notification> = {}): Notification =>
  ({
    id: 'test-id',
    type: 'match_created',
    channel: 'in_app',
    status: 'pending',
    title: 'Test Title',
    message: 'Test Message',
    related_object_type: 'listing',
    related_object_id: 'listing-1',
    created_at: '2024-01-15T10:00:00Z',
    ...overrides,
  }) as Notification

describe('NotificationItem', () => {
  it('renders correctly with basic notification', () => {
    const notification = mockNotification()
    const wrapper = mount(NotificationItem, {
      props: { notification },
      global: {
        plugins: [createPinia()],
      },
    })

    expect(wrapper.find('.notification-item').exists()).toBe(true)
    expect(wrapper.text()).toContain('Test Title')
    expect(wrapper.text()).toContain('Test Message')
  })

  it('applies unread styling for pending status', () => {
    const notification = mockNotification({ status: 'pending' })
    const wrapper = mount(NotificationItem, {
      props: { notification },
      global: {
        plugins: [createPinia()],
      },
    })

    expect(wrapper.find('.notification-item.unread').exists()).toBe(true)
  })

  it('does not apply unread styling for read status', () => {
    const notification = mockNotification({ status: 'read' })
    const wrapper = mount(NotificationItem, {
      props: { notification },
      global: {
        plugins: [createPinia()],
      },
    })

    expect(wrapper.find('.notification-item.unread').exists()).toBe(false)
  })

  it('shows mark read button for unread notifications', () => {
    const notification = mockNotification({ status: 'pending' })
    const wrapper = mount(NotificationItem, {
      props: { notification },
      global: {
        plugins: [createPinia()],
      },
    })

    expect(wrapper.find('button').exists()).toBe(true)
  })

  it('hides mark read button for read notifications', () => {
    const notification = mockNotification({ status: 'read' })
    const wrapper = mount(NotificationItem, {
      props: { notification },
      global: {
        plugins: [createPinia()],
      },
    })

    expect(wrapper.find('button').exists()).toBe(false)
  })

  it('emits mark-read when button clicked', async () => {
    const notification = mockNotification({ status: 'pending' })
    const wrapper = mount(NotificationItem, {
      props: { notification },
      global: {
        plugins: [createPinia()],
      },
    })

    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('mark-read')).toBeTruthy()
  })

  it('handles click event', async () => {
    const notification = mockNotification()
    const wrapper = mount(NotificationItem, {
      props: { notification },
      global: {
        plugins: [createPinia()],
      },
    })

    await wrapper.find('.notification-item').trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })

  it('renders listing_published notification type', () => {
    const notification = mockNotification({ type: 'listing_published' })
    const wrapper = mount(NotificationItem, {
      props: { notification },
      global: {
        plugins: [createPinia()],
      },
    })

    expect(wrapper.text()).toContain('Test Title')
  })

  it('renders match_accepted notification type', () => {
    const notification = mockNotification({ type: 'match_accepted' })
    const wrapper = mount(NotificationItem, {
      props: { notification },
      global: {
        plugins: [createPinia()],
      },
    })

    expect(wrapper.text()).toContain('Test Title')
  })

  it('renders kyc_approved notification type', () => {
    const notification = mockNotification({ type: 'kyc_approved' })
    const wrapper = mount(NotificationItem, {
      props: { notification },
      global: {
        plugins: [createPinia()],
      },
    })

    expect(wrapper.text()).toContain('Test Title')
  })

  it('renders settlement_confirmed notification type', () => {
    const notification = mockNotification({ type: 'settlement_confirmed' })
    const wrapper = mount(NotificationItem, {
      props: { notification },
      global: {
        plugins: [createPinia()],
      },
    })

    expect(wrapper.text()).toContain('Test Title')
  })
})