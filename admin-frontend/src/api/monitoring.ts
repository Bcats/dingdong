/**
 * 监控相关API
 */
import { get } from '@/utils/request'

export interface SystemMetrics {
  total_messages: number
  success_messages: number
  failed_messages: number
  success_rate: number
  pending_messages: number
  hourly_stats: Array<{
    hour: string
    total: number
    success: number
    failed: number
  }>
}

/**
 * 获取系统指标
 */
export function getSystemMetrics(hours: number = 24, startDate?: string, endDate?: string) {
  const params: any = { hours }
  if (startDate && endDate) {
    params.start_date = startDate
    params.end_date = endDate
  }
  return get<{ code: number; message: string; data: SystemMetrics }>(
    `/v1/monitoring/metrics`,
    { params }
  )
}

/**
 * 获取详细健康检查
 */
export function getDetailedHealth() {
  return get<{ code: number; message: string; data: any }>('/v1/monitoring/health/detailed')
}

