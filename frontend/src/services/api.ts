import axios from 'axios';
import type {
  Affiliate,
  Contribution,
  AffiliateSummary,
  PaginatedResponse,
  CreateAffiliateRequest,
  CreateContributionRequest,
  UpdateStatusRequest,
} from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Affiliates
export const affiliatesApi = {
  getAll: async (params?: {
    page?: number;
    status?: string;
    full_name?: string;
    document_number?: string;
  }): Promise<PaginatedResponse<Affiliate>> => {
    const { data } = await apiClient.get('/affiliates/', { params });
    return data;
  },

  getById: async (id: number): Promise<Affiliate> => {
    const { data } = await apiClient.get(`/affiliates/${id}/`);
    return data;
  },

  create: async (affiliate: CreateAffiliateRequest): Promise<Affiliate> => {
    const { data } = await apiClient.post('/affiliates/', affiliate);
    return data;
  },

  update: async (id: number, affiliate: Partial<CreateAffiliateRequest>): Promise<Affiliate> => {
    const { data } = await apiClient.put(`/affiliates/${id}/`, affiliate);
    return data;
  },

  updateStatus: async (id: number, status: UpdateStatusRequest): Promise<Affiliate> => {
    const { data } = await apiClient.patch(`/affiliates/${id}/status/`, status);
    return data;
  },

  getSummary: async (id: number): Promise<AffiliateSummary> => {
    const { data } = await apiClient.get(`/affiliates/${id}/summary/`);
    return data;
  },
};

// Contributions
export const contributionsApi = {
  getByAffiliate: async (affiliateId: number): Promise<PaginatedResponse<Contribution>> => {
    const { data } = await apiClient.get(`/affiliates/${affiliateId}/contributions/`);
    return data;
  },

  create: async (
    affiliateId: number,
    contribution: CreateContributionRequest
  ): Promise<Contribution> => {
    const { data } = await apiClient.post(`/affiliates/${affiliateId}/contributions/`, contribution);
    return data;
  },
};

