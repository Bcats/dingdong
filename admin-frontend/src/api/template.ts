/**
 * 模板相关API
 */
import { get, post, put, del } from '@/utils/request'

export interface Template {
  id: number
  code: string
  name: string
  type: string
  subject_template: string
  content_template: string
  variables?: Record<string, any>
  is_active: boolean
  version: number
  created_at: string
  updated_at: string
}

export interface TemplateHistory {
  id: number
  template_id: number
  version: number
  subject_template: string
  content_template: string
  created_at: string
  created_by: string
}

/**
 * 获取模板列表
 */
export function getTemplateList(params?: { type?: string; is_active?: boolean }) {
  return get<{ code: number; message: string; data: Template[] }>('/v1/templates', { params })
}

/**
 * 获取模板详情
 */
export function getTemplateDetail(id: number) {
  return get<{ code: number; message: string; data: Template }>(`/v1/templates/${id}`)
}

/**
 * 创建模板
 */
export function createTemplate(data: Partial<Template>) {
  return post<{ code: number; message: string; data: Template }>('/v1/templates', data)
}

/**
 * 更新模板
 */
export function updateTemplate(id: number, data: Partial<Template>) {
  return put<{ code: number; message: string; data: Template }>(`/v1/templates/${id}`, data)
}

/**
 * 删除模板
 */
export function deleteTemplate(id: number) {
  return del<{ code: number; message: string }>(`/v1/templates/${id}`)
}

/**
 * 获取模板历史
 */
export function getTemplateHistory(id: number) {
  return get<{ code: number; message: string; data: TemplateHistory[] }>(
    `/v1/templates/${id}/history`
  )
}

/**
 * 回滚模板
 */
export function rollbackTemplate(id: number, version: number) {
  return post<{ code: number; message: string; data: Template }>(`/v1/templates/${id}/rollback`, {
    target_version: version,
  })
}

