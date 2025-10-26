/**
 * 认证相关API
 */
import { post } from '@/utils/request'

export interface LoginParams {
  username: string
  password: string
}

export interface UserInfo {
  id: number
  username: string
  nickname?: string
  email?: string
  is_superuser: boolean
  last_login_at?: string
}

export interface LoginResponse {
  code: number
  message: string
  data: {
    access_token: string
    token_type: string
    expires_in: number
    user_info: UserInfo
  }
}

/**
 * 管理员登录
 */
export function login(data: LoginParams) {
  return post<LoginResponse>('/v1/admin/auth/login', data)
}

