/**
 * 邮箱账户相关API
 */
import { get, post, put, del } from '@/utils/request'

export interface EmailAccount {
  id: number
  email: string
  display_name?: string
  smtp_host: string
  smtp_port: number
  smtp_username: string
  use_tls: boolean
  daily_limit: number
  daily_sent_count: number
  last_reset_at: string
  priority: number
  is_active: boolean
  failure_count: number
  last_failure_at?: string
  remark?: string
  is_available: boolean
  created_at: string
  updated_at: string
}

export interface EmailAccountCreate {
  email: string
  display_name?: string
  smtp_host: string
  smtp_port: number
  smtp_username: string
  smtp_password: string
  use_tls: boolean
  daily_limit: number
  priority: number
  is_active: boolean
  remark?: string
}

export interface EmailAccountUpdate {
  display_name?: string
  smtp_host?: string
  smtp_port?: number
  smtp_username?: string
  smtp_password?: string
  use_tls?: boolean
  daily_limit?: number
  priority?: number
  is_active?: boolean
  remark?: string
}

/**
 * 获取邮箱账户列表
 */
export function getEmailAccountList(params?: { is_active?: boolean }) {
  return get<{ code: number; message: string; data: EmailAccount[] }>(
    '/v1/admin/email-accounts',
    { params }
  )
}

/**
 * 获取邮箱账户详情
 */
export function getEmailAccountDetail(id: number) {
  return get<{ code: number; message: string; data: EmailAccount }>(
    `/v1/admin/email-accounts/${id}`
  )
}

/**
 * 创建邮箱账户
 */
export function createEmailAccount(data: EmailAccountCreate) {
  return post<{ code: number; message: string; data: EmailAccount }>(
    '/v1/admin/email-accounts',
    data
  )
}

/**
 * 更新邮箱账户
 */
export function updateEmailAccount(id: number, data: EmailAccountUpdate) {
  return put<{ code: number; message: string; data: EmailAccount }>(
    `/v1/admin/email-accounts/${id}`,
    data
  )
}

/**
 * 删除邮箱账户
 */
export function deleteEmailAccount(id: number) {
  return del<{ code: number; message: string }>(`/v1/admin/email-accounts/${id}`)
}

/**
 * 测试邮箱连接
 */
export function testEmailAccount(id: number, test_email?: string) {
  return post<{
    code: number
    message: string
    data: {
      success: boolean
      message: string
      error?: string
      duration_ms?: number
    }
  }>(`/v1/admin/email-accounts/${id}/test`, { test_email })
}

