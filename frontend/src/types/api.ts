// Union types
export type CompanyStatus = 'active' | 'inactive';
export type VatStatus = 'active' | 'inactive' | 'exempt';
export type SubscriptionTier = 'free' | 'pro' | 'enterprise';
export type ProviderStatus = 'fresh' | 'cached' | 'rate_limited' | 'error' | 'unknown';

export interface ApiResponse<T = unknown> {
  data: T;
  message?: string;
  success: boolean;
}

export interface User {
  id: string;
  email: string;
  name?: string;
  subscription_tier: SubscriptionTier;
  api_calls_used: number;
  api_calls_limit: number;
  created_at: string;
}

export interface ApiKey {
  id: string;
  name: string;
  key: string;
  last_used?: string;
  created_at: string;
  is_active: boolean;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export interface SubscriptionInfo {
  tier: SubscriptionTier;
  usage: number;
  limit: number;
}

export interface CheckoutSession {
  checkout_url: string;
}
