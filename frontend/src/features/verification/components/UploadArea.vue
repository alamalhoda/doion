<template>
  <div class="upload-area" @dragover.prevent @drop.prevent @drop="onDrop">
    <n-upload
      :action="uploadUrl"
      :headers="headers"
      :multiple="false"
      :show-file-list="false"
      :accept="accept"
      :max="1"
      :on-exceed="handleExceed"
      :on-success="handleSuccess"
      :on-error="handleError"
    >
      <div class="upload-zone">
        <n-icon :size="40">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
        </n-icon>
        <n-p>{{ dragLabel }}</n-p>
      </div>
    </n-upload>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useUploadStore } from '@/stores/uploadStore'
import { useFileUpload } from '@/composables/useFileUpload'

const emit = defineEmits<{
  (e: 'uploaded', payload: { type: string; file: File }): void
}>()

const props = defineProps<{
  accept: string
  maxSize: number
  documentType: string
}>()

const uploadStore = useUploadStore()
const uploadApiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const { files, error: uploadError, addFiles, clear } = useFileUpload({
  accept: props.accept,
  maxSize: props.maxSize,
  multiple: false,
})

const uploadUrl = `${uploadApiBase}/api/v1/documents/upload/`
const headers = computed(() => ({
  Authorization: `Bearer ${localStorage.getItem('access_token')}`,
}))

const dragLabel = computed(() => `${props.documentType} در اینجا رها کنید یا کلیک کنید`)

function onDrop(e: DragEvent) {
  if (e.dataTransfer?.files.length) {
    addFiles(e.dataTransfer.files)
  }
}

function handleExceed(files: File[]) {
  uploadStore.setError('حداکثر یک فایل مجاز است')
}

function handleSuccess(_file: File, response: any) {
  emit('uploaded', { type: props.documentType, file: _file })
}

function handleError(_error: Error) {
  uploadStore.setError(_error.message)
}
</script>

<style scoped>
.upload-area {
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s;
}
.upload-area:hover {
  border-color: #18a058;
}
</style>