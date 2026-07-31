<template>
  <div
    class="upload-area"
    @dragover.prevent
    @drop.prevent="onDrop"
  >
    <input
      ref="inputRef"
      type="file"
      class="upload-input"
      :accept="accept"
      @change="onChange"
    >
    <button
      type="button"
      class="upload-zone"
      @click="inputRef?.click()"
    >
      <n-icon :size="40">
        <svg
          viewBox="0 0 24 24"
          fill="currentColor"
        ><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" /></svg>
      </n-icon>
      <n-p>{{ dragLabel }}</n-p>
      <n-p
        v-if="selectedName"
        depth="3"
      >
        {{ selectedName }}
      </n-p>
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useUploadStore } from '@/stores/uploadStore'

const emit = defineEmits<{
  (e: 'uploaded', payload: { type: string; file: File }): void
}>()

const props = defineProps<{
  accept: string
  maxSize: number
  documentType: string
}>()

const uploadStore = useUploadStore()
const inputRef = ref<HTMLInputElement | null>(null)
const selectedName = ref('')

const dragLabel = computed(() => `${props.documentType} را انتخاب کنید یا اینجا رها کنید`)

function takeFile(file: File | undefined) {
  if (!file) return
  if (file.size > props.maxSize) {
    uploadStore.setError('حجم فایل بیش از حد مجاز است')
    return
  }
  selectedName.value = file.name
  emit('uploaded', { type: props.documentType, file })
}

function onChange(e: Event) {
  const input = e.target as HTMLInputElement
  takeFile(input.files?.[0])
}

function onDrop(e: DragEvent) {
  takeFile(e.dataTransfer?.files?.[0])
}
</script>

<style scoped>
.upload-area {
  width: 100%;
}
.upload-input {
  display: none;
}
.upload-zone {
  width: 100%;
  border: 2px dashed var(--border, #d1d5db);
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  background: transparent;
  cursor: pointer;
}
</style>
