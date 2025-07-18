import axios, { HttpStatusCode, AxiosInstance } from 'axios';
import {
  ApiResponse,
  User,
  ApiKey,
  AuthResponse,
  SubscriptionInfo,
  CheckoutSession,
  SubscriptionTier,
} from '@/types/api';

class ApiClient {
  private client: AxiosInstance;
  private authToken: string | null = null;

  constructor(baseURL: string = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        if (!this.authToken) {
          this.loadAuthFromStorage();
        }
        if (this.authToken) {
          config.headers.Authorization = `Bearer ${this.authToken}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === HttpStatusCode.Unauthorized) {
          // Don't redirect if this is a login/register request (expected 401)
          const isAuthRequest = error.config?.url?.includes('/auth/login') ||
                               error.config?.url?.includes('/auth/register');

          if (!isAuthRequest) {
            this.clearAuth();
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  setAuth(token: string) {
    this.authToken = token;
    localStorage.setItem('auth_token', token);
  }

  clearAuth() {
    this.authToken = null;
    localStorage.removeItem('auth_token');
  }

  loadAuthFromStorage() {
    const token = localStorage.getItem('auth_token');
    if (token) {
      this.authToken = token;
    }
  }

  // Authentication endpoints
  async login(email: string, password: string): Promise<ApiResponse<AuthResponse>> {
    const response = await this.client.post('/api/v1/auth/login', { email, password });
    return response.data;
  }

  async register(email: string, password: string, name: string): Promise<ApiResponse<AuthResponse>> {
    const response = await this.client.post('/api/v1/auth/register', { email, password, name });
    return response.data;
  }

  async forgotPassword(email: string): Promise<ApiResponse> {
    const response = await this.client.post('/api/v1/auth/forgot-password', { email });
    return response.data;
  }

  async resetPassword(token: string, password: string): Promise<ApiResponse> {
    const response = await this.client.post('/api/v1/auth/reset-password', { token, password });
    return response.data;
  }

  async changePassword(currentPassword: string, newPassword: string): Promise<ApiResponse> {
    const response = await this.client.post('/api/v1/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword
    });
    return response.data;
  }

  // User endpoints
  async getProfile(): Promise<ApiResponse<User>> {
    const response = await this.client.get('/api/v1/auth/me');
    return response.data;
  }

  async updateProfile(data: Partial<User>): Promise<ApiResponse<User>> {
    const response = await this.client.put('/api/v1/user/profile', data);
    return response.data;
  }

  // API Keys endpoints
  async getApiKeys(): Promise<ApiResponse<ApiKey[]>> {
    const response = await this.client.get('/api/v1/user/api-keys');
    return response.data;
  }

  async createApiKey(name: string): Promise<ApiResponse<ApiKey>> {
    const response = await this.client.post('/api/v1/user/api-keys', { name });
    return response.data;
  }

  async deleteApiKey(id: string): Promise<ApiResponse> {
    const response = await this.client.delete(`/api/v1/user/api-keys/${id}`);
    return response.data;
  }

  // Subscription endpoints
  async getSubscription(): Promise<ApiResponse<SubscriptionInfo>> {
    const response = await this.client.get('/api/v1/user/subscription');
    return response.data;
  }

  async createCheckoutSession(tier: Exclude<SubscriptionTier, 'free'>): Promise<ApiResponse<CheckoutSession>> {
    const response = await this.client.post('/api/v1/billing/checkout', { tier });
    return response.data;
  }
}

export const apiClient = new ApiClient();
