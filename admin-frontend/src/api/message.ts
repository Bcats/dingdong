/**
 * 消息相关API
 */
import { get, post, del } from '@/utils/request'

export interface MessageQuery {
  channel?: string
  status?: string
  to?: string
  request_id?: string
  start_time?: string
  end_time?: string
  page?: number
  page_size?: number
}

export interface Message {
  id: number
  channel: string
  status: string
  to: string
  subject: string
  content: string
  retry_count: number
  max_retry: number
  created_at: string
  sent_at?: string
  error_message?: string
}

export interface MessageListResponse {
  code: number
  message: string
  data: {
    items: Message[]
    pagination: {
      page: number
      page_size: number
      total: number
      total_pages: number
    }
  }
}

export interface MessageDetailResponse {
  code: number
  message: string
  data: Message
}

/**
 * 获取消息列表
 */
export function getMessageList(params: MessageQuery) {
  return get<MessageListResponse>('/v1/messages', { params })
}

/**
 * 获取消息详情
 */
export function getMessageDetail(id: number) {
  return get<MessageDetailResponse>(`/v1/messages/${id}`)
}

/**
 * 重试消息
 */
export function retryMessage(id: number) {
  return post<{ code: number; message: string }>(`/v1/messages/${id}/retry`, {})
}

/**
 * 删除消息
 */
export function deleteMessage(id: number) {
  return del<{ code: number; message: string }>(`/v1/messages/${id}`)
}

