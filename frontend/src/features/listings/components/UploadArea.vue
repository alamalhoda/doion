<template>
  <div class="upload-area" @dragover.prevent @drop.prevent @drop="onDrop">
    <input
      type="file"
      :accept="accept"
      class="upload-input"
      @change="onChange"
    >
    <div class="upload-zone">
      <div class="upload-icon">
        <slot name="icon">
          <svg viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="17 8 12 3 7 8" />
            <line x1="12" y1="3" x2="12" y2="15" />
          </svg>
        </slot>
      </div>
      <p class="upload-label">{{ label }}</p>
      <p class="upload-hint">{{ hint }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">

const props = withDefaults(defineProps<{
  accept?: string
  maxSize?: number
  multiple?: boolean
  label?: string
  hint?: string
}>(), {
  accept: 'image/*,.pdf',
  maxSize: 5 * 1024 * 1024,
  multiple: false,
  label: 'فایل را در اینجا رها کنید یا کلیک کنید',
  hint: 'فرمت‌های مجاز: JPG، PNG، PDF — حداکثر ۵ مگابایت',
})

const emit = defineEmits<{
  (e: 'change', files: FileList): void
  (e: 'error', message: string): void
}>()

function validateFile(file: File): string | null {
  if (file.size > props.maxSize) {
    return 'حجم فایل بیشتر از ۵ مگابایت است'
  }
  return null
}

function onChange(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length) {
    handleFiles(target.files)
  }
}

function onDrop(e: DragEvent) {
  if (e.dataTransfer?.files.length) {
    handleFiles(e.dataTransfer.files)
  }
}

function handleFiles(fileList: FileList) {
  for (const file of Array.from(fileList)) {
    const err = validateFile(file)
    if (err) {
      emit('error', err)
      return
    }
  }
  emit('change', fileList)
}
</script>

<script lang="ts">
export default {
  inheritAttrs: false,
}
</script>

<style scoped>
.upload-area {
  border: 2px dashed var(--border);
  border-radius: var(--radius);
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-fast);
  background: var(--surface);
}

.upload-area:hover {
  border-color: var(--navy-light);
  background: rgba(26, 61, 107, 0.03);
}

.upload-input {
  position: absolute;
  width: 0;
  height: 0;
  opacity: 0;
  overflow: hidden;
}

.upload-zone {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.upload-icon {
  color: var(--text3);
  margin-bottom: 0.25rem;
}

.upload-label {
  font-size: var(--font-size-base);
  color: var(--text2);
  margin: 0;
  font-weight: var(--font-weight-medium);
}

.upload-hint {
  font-size: var(--font-size-xs);
  color: var(--text3);
  margin: 0;
}
</style>
