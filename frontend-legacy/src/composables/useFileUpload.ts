import { ref, readonly } from 'vue'

export interface FileUploadOptions {
  accept?: string
  maxSize?: number
  multiple?: boolean
}

export function useFileUpload(options: FileUploadOptions = {}) {
  const { accept, maxSize = 5 * 1024 * 1024, multiple = false } = options
  const files = ref<File[]>([])
  const error = ref<string | null>(null)

  function validateFile(file: File): string | null {
    if (maxSize && file.size > maxSize) {
      return `error.file_too_large`
    }
    if (accept && !file.type.match(accept)) {
      return `error.invalid_file_type`
    }
    return null
  }

  function addFiles(newFiles: FileList | File[]) {
    error.value = null
    const fileArray = Array.from(newFiles)

    for (const file of fileArray) {
      const validationError = validateFile(file)
      if (validationError) {
        error.value = validationError
        return
      }
    }

    if (multiple) {
      files.value = [...files.value, ...fileArray]
    } else {
      files.value = [fileArray[0]]
    }
  }

  function removeFile(index: number) {
    files.value.splice(index, 1)
  }

  function clear() {
    files.value = []
    error.value = null
  }

  return {
    files: readonly(files),
    error: readonly(error),
    addFiles,
    removeFile,
    clear,
  }
}