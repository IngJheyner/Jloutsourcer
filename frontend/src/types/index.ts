export type DocumentType = 'CC' | 'CE' | 'NIT';
export type AffiliateStatus = 'ACTIVE' | 'INACTIVE';
export type PaymentMethod = 'CASH' | 'TRANSFER' | 'CARD';

export interface Affiliate {
  id: number;
  full_name: string;
  document_type: DocumentType;
  document_number: string;
  email: string;
  status: AffiliateStatus;
  phone_number?: string | null;
  address?: string | null;
  notes?: string | null;
  created_at: string;
  updated_at: string;
}

export interface Contribution {
  id: number;
  affiliate_id: number;
  amount: string;
  contribution_date: string;
  payment_method: PaymentMethod;
  reference_number?: string | null;
  notes?: string | null;
  verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface AffiliateSummary {
  affiliate: {
    full_name: string;
    document_number: string;
    status: AffiliateStatus;
  };
  total_contributions: number;
  contributions_count: number;
  last_contribution_date: string | null;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface CreateAffiliateRequest {
  full_name: string;
  document_type: DocumentType;
  document_number: string;
  email: string;
  status?: AffiliateStatus;
  phone_number?: string;
  address?: string;
  notes?: string;
}

export interface CreateContributionRequest {
  amount: number;
  contribution_date: string;
  payment_method: PaymentMethod;
  reference_number?: string;
  notes?: string;
}

export interface UpdateStatusRequest {
  status: AffiliateStatus;
}

