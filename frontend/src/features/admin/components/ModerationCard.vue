<template>
  <Card
    title="آگهی در انتظار بررسی"
    hoverable
    class="moderation-card"
  >
    <template #footer>
      <div class="moderation-actions">
        <Button
          variant="teal"
          size="sm"
          @click="approve"
        >
          تأیید
        </Button>
        <Button
          variant="danger"
          size="sm"
          @click="reject"
        >
          رد
        </Button>
      </div>
    </template>

    <div class="moderation-meta">
      <div class="moderation-row">
        <span class="moderation-label">صادرکننده:</span>
        <span class="moderation-value">{{ item.issuer || '' }}</span>
      </div>
      <div class="moderation-row">
        <span class="moderation-label">بانک:</span>
        <span class="moderation-value">{{ item.bank || '' }}</span>
      </div>
      <div class="moderation-row">
        <span class="moderation-label">مبلغ:</span>
        <span class="moderation-value moderation-value--amount">{{ formatCurrency(item.amount ?? 0) }} ریال</span>
      </div>
      <div class="moderation-row">
        <span class="moderation-label">سررسید:</span>
        <span class="moderation-value">{{ item.dueDate || '' }}</span>
      </div>
      <div class="moderation-row">
        <span class="moderation-label">ریسک:</span>
        <span class="moderation-value">{{ item.risk || '' }}</span>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import Card from '@/components/Card.vue'
import Button from '@/components/ui/Button.vue'

interface ModerationItem {
  id: string | number
  issuer?: string
  bank?: string
  amount?: number
  dueDate?: string
  risk?: string
}

const props = withDefaults(
  defineProps<{
    item: ModerationItem
  }>(),
  {}
)

const emit = defineEmits<{
  (e: 'approve', id: string | number): void
  (e: 'reject', id: string | number): void
}>()

const formatCurrency = (value: number) => value.toLocaleString('fa-IR')

const approve = () => emit('approve', props.item.id)
const reject = () => emit('reject', props.item.id)
</script>

<style scoped>
.moderation-card {
  margin-bottom: 1rem;
}

.moderation-meta {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.moderation-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: var(--font-size-base);
}

.moderation-label {
  color: var(--text3);
  font-weight: var(--font-weight-normal);
  min-width: 5rem;
}

.moderation-value {
  color: var(--text1);
  font-weight: var(--font-weight-medium);
}

.moderation-value--amount {
  color: var(--navy);
  font-weight: var(--font-weight-semibold);
}

.moderation-actions {
  display: flex;
  gap: 0.5rem;
}
</style>
