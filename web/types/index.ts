export interface User {
  id: number;
  email: string;
  username?: string;
  first_name?: string;
  last_name?: string;
  telegram_id?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  last_login?: string;
  timezone?: string;
  language?: string;
}

export interface Subscription {
  id: number;
  user_id: number;
  name: string;
  description?: string;
  amount: number;
  currency: string;
  frequency: 'monthly' | 'yearly';
  next_billing_date: string;
  is_active: boolean;
  provider?: string;
  logo_url?: string;
  website_url?: string;
  created_at: string;
  updated_at: string;
  cancelled_at?: string;
}

export interface Analytics {
  id: number;
  user_id: number;
  total_monthly_spend: number;
  total_yearly_spend: number;
  active_subscriptions: number;
  cancelled_subscriptions: number;
  period_start: string;
  period_end: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  username?: string;
  first_name?: string;
  last_name?: string;
}

export interface SubscriptionRequest {
  name: string;
  description?: string;
  amount: number;
  currency: string;
  frequency: 'monthly' | 'yearly';
  next_billing_date: string;
  provider?: string;
  logo_url?: string;
  website_url?: string;
}
