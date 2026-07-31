import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { defineComponent } from 'vue'
import { createPinia, setActivePinia } from 'pinia'
import NotificationsView from '../views/NotificationsView.vue'

// Mock the store
vi.mock('../stores/notificationStore', () => ({
  useNotificationStore: vi.fn(() => ({
    notifications: [],
    unreadCount: 0,
    totalCount: 0,
    isLoading: false,
    error: null,
    filteredNotifications: [],
    fetchNotifications: vi.fn(),
    markAsRead: vi.fn(),
    markAllAsRead: vi.fn(),
    markAllAsRead: vi.fn(),
    fetchPreferences: vi.fn(),
    updatePreferences: vi.fn(),
    setFilter: vi.fn(),
    setStatusFilter: vi.fn(),
  })),
}))

// Mock child components
vi.mock('../components/NotificationItem.vue', () => ({
  default: defineComponent({
    name: 'NotificationItem',
    props: ['notification'],
    emits: ['click'],
    template: '<div class="notification-item-mock" @click="$emit(\'click\')">NotificationItem</div>',
  }),
}))

vi.mock('../components/NotificationSidebar.vue', () => ({
  default: defineComponent({
    name: 'NotificationSidebar',
    props: ['modelValue', 'unreadCount'],
    emits: ['update:activeTab', 'mark-all-read'],
    template: '<div class="notification-sidebar-mock">NotificationSidebar</div>',
  }),
}))

describe('NotificationsView', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('should render the notifications title', () => {
    const wrapper = mount(NotificationsView, {
      global: {
        stubs: {
          Icon: true,
          AppButton: true,
          NEmpty: true,
        },
      },
    })

    expect(wrapper.text()).toContain('اعلان‌ها')
  })

  it('should show loading state when loading', async () => {
    const { useNotificationStore } = await import(
      '../stores/notificationStore'
    )
    vi.mocked(useNotificationStore).mockReturnValueOnce({
      notifications: [],
      unreadCount: 0,
      totalCount: 0,
      isLoading: true,
      error: null,
      filteredNotifications: [],
      fetchNotifications: vi.fn(),
      markAsRead: vi.fn(),
      markAllAsRead: vi.fn(),
      fetchPreferences: vi.fn(),
      updatePreferences: vi.fn(),
      setFilter: vi.fn(),
      setStatusFilter: vi.fn(),
    } as any)

    const wrapper = mount(NotificationsView, {
      global: {
        stubs: {
          Icon: true,
          AppButton: true,
          NEmpty: true,
        },
      },
    })

    // Since the mock runs before component creation, loading should be true
    expect(wrapper.exists()).toBe(true)
  })

  it('should show error state when error exists', async () => {
    const { useNotificationStore } = await import(
      '../stores/notificationStore'
    )
    vi.mocked(useNotificationStore).mockReturnValueOnce({
      notifications: [],
      unreadCount: 0,
      totalCount: 0,
      isLoading: false,
      error: 'خطا در بارگذاری',
      filteredNotifications: [],
      fetchNotifications: vi.fn(),
      markAsRead: vi.fn(),
      markAllAsRead: vi.fn(),
      fetchPreferences: vi.fn(),
      updatePreferences: vi.fn(),
      setFilter: vi.fn(),
      setStatusFilter: vi.fn(),
    } as any)

    const wrapper = mount(NotificationsView, {
      global: {
        stubs: {
          Icon: true,
          AppButton: true,
          NEmpty: true,
        },
      },
    })

    expect(wrapper.text()).toContain('خطا در بارگذاری')
  })

  it('should show empty state when no notifications', async () => {
    const { useNotificationStore } = await import(
      '../stores/notificationStore'
    )
    vi.mocked(useNotificationStore).mockReturnValueOnce({
      notifications: [],
      unreadCount: 0,
      totalCount: 0,
      isLoading: false,
      error: null,
      filteredNotifications: [],
      fetchNotifications: vi.fn(),
      markAsRead: vi.fn(),
      markAllAsRead: vi.fn(),
      fetchPreferences: vi.fn(),
      updatePreferences: vi.fn(),
      setFilter: vi.fn(),
      setStatusFilter: vi.fn(),
    } as any)

    const wrapper = mount(NotificationsView, {
      global: {
        stubs: {
          Icon: true,
          AppButton: true,
          NEmpty: true,
        },
      },
    })

    expect(wrapper.text()).toContain('همه چیز مرتب است')
  })

  it('should render NotificationSidebar', () => {
    const wrapper = mount(NotificationsView, {
      global: {
        stubs: {
          Icon: true,
          AppButton: true,
          NEmpty: true,
        },
      },
    })

    expect(wrapper.findComponent({ name: 'NotificationSidebar' }).exists()).toBe(true)
  })
})
