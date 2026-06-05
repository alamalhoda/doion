// Task feature shell for Phase 1+
// TODO: Implement task management CRUD operations

export interface Task {
  id: number
  title: string
  description: string
  created_at: string
  updated_at: string
}

export interface CreateTaskRequest {
  title: string
  description?: string
}
