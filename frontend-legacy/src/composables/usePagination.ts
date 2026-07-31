import { ref, computed } from 'vue'

interface PaginationState {
  page: number
  pageSize: number
  total: number
}

export function usePagination(initialPageSize = 10) {
  const state = ref<PaginationState>({
    page: 1,
    pageSize: initialPageSize,
    total: 0,
  })

  const totalPages = computed(() => Math.ceil(state.value.total / state.value.pageSize))

  const hasNextPage = computed(() => state.value.page < totalPages.value)

  const hasPreviousPage = computed(() => state.value.page > 1)

  function goToPage(page: number) {
    if (page >= 1 && page <= totalPages.value) {
      state.value.page = page
    }
  }

  function nextPage() {
    if (hasNextPage.value) {
      state.value.page++
    }
  }

  function previousPage() {
    if (hasPreviousPage.value) {
      state.value.page--
    }
  }

  function setTotal(total: number) {
    state.value.total = total
  }

  function setPageSize(size: number) {
    state.value.pageSize = size
    state.value.page = 1
  }

  function reset() {
    state.value.page = 1
    state.value.total = 0
  }

  return {
    page: computed(() => state.value.page),
    pageSize: computed(() => state.value.pageSize),
    total: computed(() => state.value.total),
    totalPages,
    hasNextPage,
    hasPreviousPage,
    goToPage,
    nextPage,
    previousPage,
    setTotal,
    setPageSize,
    reset,
  }
}
