<template>
  <n-space vertical :size="24">
    <n-space align="start" :size="12">
      <n-h2>{{ t('moderation.kyc.title') }}</n-h2>
      <n-tag :type="pendingCount > 0 ? 'error' : 'success'">
        {{ pendingCount }} {{ t('moderation.pending_items') }}
      </n-tag>
    </n-space>

    <n-data-table
      :columns="columns"
      :data="store.kycQueue"
      :loading="store.loading"
      :pagination="pagination"
      :row-key="(row: any) => row.id"
      @update:page="onPageChange"
    />
  </n-space>
</template>

<script setup lang="ts">
import { ref, h, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useModerationStore } from '@/features/verification/stores/moderationStore'
import { NButton, NTag, NSpace, NAvatar } from 'naive-ui'
import KycStatusBadge from '@/features/verification/components/KycStatusBadge.vue'
import { useToast } from 'vue-toastification'
import dayjs from 'dayjs'

const { t } = useI18n()
const store = useModerationStore()
const toast = useToast()

const pagination = ref({ page: 1, pageSize: 10 })

const pendingCount = ref(0)

const columns = ref([
  {
    title: t('kyc.user_info'),
    key: 'user',
    width: 250,
    render(row: any) {
      return h(
        NSpace,
        { align: 'center', size: 12 },
        () => [
          h(NAvatar, { size: 32, round: true, src: row.user?.avatar }),
          h(
            'span',
            {},
            row.user?.full_name || row.user?.username || '-'
          ),
        ]
      )
    },
  },
  {
    title: t('kyc.national_id'),
    key: 'national_id',
    width: 150,
    render(row: any) {
      return row.national_id || '-'
    },
  },
  {
    title: t('kyc.status'),
    key: 'status',
    width: 150,
    render(row: any) {
      return h(KycStatusBadge, { status: row.status })
    },
  },
  {
    title: t('kyc.submitted_at'),
    key: 'submitted_at',
    width: 180,
    render(row: any) {
      try {
        return dayjs(row.created_at).format('YYYY/MM/DD HH:mm')
      } catch {
        return row.created_at
      }
    },
  },
  {
    title: t('kyc.actions'),
    key: 'actions',
    width: 200,
    render(row: any) {
      return h(
        NSpace,
        {},
        () => [
          h(
            NButton,
            {
              size: 'small',
              type: 'primary',
              onClick: () => handleApprove(row.id),
            },
            () => t('kyc.approve')
          ),
          h(
            NButton,
            {
              size: 'small',
              type: 'error',
              onClick: () => handleReject(row.id),
            },
            () => t('kyc.reject')
          ),
        ]
      )
    },
  },
])

function onPageChange(page: number) {
  pagination.value.page = page
}

async function handleApprove(id: string) {
  try {
    await store.approveKyc(id)
    toast.success(t('kyc.approved'))
    await loadQueue()
  } catch (error: any) {
    toast.error(error.message || t('common.error'))
  }
}

async function handleReject(id: string) {
  try {
    const code = prompt(t('kyc.enter_rejection_code')) || 'KYC_101'
    const note = prompt(t('kyc.enter_rejection_note')) || ''
    await store.rejectKyc(id, code, note)
    toast.success(t('kyc.rejected'))
    await loadQueue()
  } catch (error: any) {
    toast.error(error.message || t('common.error'))
  }
}

async function loadQueue() {
  try {
    const data = await store.getKycQueue()
    const queue = Array.isArray(data) ? data : data.results || []
    store.kycQueue = queue
    pendingCount.value = queue.filter((v: any) => v.status === 'pending').length
  } catch (error: any) {
    toast.error(error.message || t('common.error'))
  }
}

onMounted(() => {
  loadQueue()
})
</script>