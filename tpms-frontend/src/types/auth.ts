export interface User {
  id: number
  username: string
  email?: string
  role: 'guest' | 'editor' | 'admin' | 'superadmin'
  telegram_id?: number
  telegram_username?: string
  created_at: string
  updated_at: string
}

export interface LoginForm {
  username: string
  password: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface AuthResponse {
  user: User
  tokens: TokenResponse
}



