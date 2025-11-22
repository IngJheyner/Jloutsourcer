import { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { affiliatesApi, contributionsApi } from '@/services/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  ArrowLeft,
  DollarSign,
  Calendar,
  TrendingUp,
  Plus,
  Loader2,
  Mail,
  Phone,
  MapPin,
  FileText,
} from 'lucide-react';
import { formatCurrency, formatDate } from '@/lib/utils';
import type { CreateContributionRequest, PaymentMethod } from '@/types';

export function AffiliateDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [showContributionForm, setShowContributionForm] = useState(false);
  const [contributionForm, setContributionForm] = useState<CreateContributionRequest>({
    amount: 0,
    contribution_date: new Date().toISOString().split('T')[0],
    payment_method: 'CASH',
    reference_number: '',
    notes: '',
  });

  const { data: affiliate, isLoading: affiliateLoading } = useQuery({
    queryKey: ['affiliate', id],
    queryFn: () => affiliatesApi.getById(Number(id)),
    enabled: !!id,
  });

  const { data: summary, isLoading: summaryLoading } = useQuery({
    queryKey: ['affiliate-summary', id],
    queryFn: () => affiliatesApi.getSummary(Number(id)),
    enabled: !!id,
  });

  const { data: contributions, isLoading: contributionsLoading } = useQuery({
    queryKey: ['contributions', id],
    queryFn: () => contributionsApi.getByAffiliate(Number(id)),
    enabled: !!id,
  });

  const createContributionMutation = useMutation({
    mutationFn: (data: CreateContributionRequest) =>
      contributionsApi.create(Number(id), data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['contributions', id] });
      queryClient.invalidateQueries({ queryKey: ['affiliate-summary', id] });
      setShowContributionForm(false);
      setContributionForm({
        amount: 0,
        contribution_date: new Date().toISOString().split('T')[0],
        payment_method: 'CASH',
        reference_number: '',
        notes: '',
      });
    },
  });

  const changeStatusMutation = useMutation({
    mutationFn: (newStatus: 'ACTIVE' | 'INACTIVE') =>
      affiliatesApi.updateStatus(Number(id), { status: newStatus }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['affiliate', id] });
      queryClient.invalidateQueries({ queryKey: ['affiliate-summary', id] });
    },
  });

  const handleContributionSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createContributionMutation.mutate(contributionForm);
  };

  const getPaymentMethodLabel = (method: PaymentMethod) => {
    const labels: Record<PaymentMethod, string> = {
      CASH: 'Efectivo',
      TRANSFER: 'Transferencia',
      CARD: 'Tarjeta',
    };
    return labels[method];
  };

  if (affiliateLoading || !affiliate) {
    return (
      <div className="flex justify-center items-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="outline" size="icon" onClick={() => navigate('/affiliates')}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div className="flex-1">
          <h1 className="text-3xl font-bold tracking-tight">{affiliate.full_name}</h1>
          <p className="text-muted-foreground mt-1">
            {affiliate.document_type}: {affiliate.document_number}
          </p>
        </div>
        <Badge variant={affiliate.status === 'ACTIVE' ? 'success' : 'destructive'} className="text-sm">
          {affiliate.status === 'ACTIVE' ? 'Activo' : 'Inactivo'}
        </Badge>
        <Button
          variant="outline"
          onClick={() =>
            changeStatusMutation.mutate(affiliate.status === 'ACTIVE' ? 'INACTIVE' : 'ACTIVE')
          }
          disabled={changeStatusMutation.isPending}
        >
          {changeStatusMutation.isPending ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            `Cambiar a ${affiliate.status === 'ACTIVE' ? 'Inactivo' : 'Activo'}`
          )}
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Aportes</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {summaryLoading ? (
              <Loader2 className="h-6 w-6 animate-spin" />
            ) : (
              <>
                <div className="text-2xl font-bold">
                  {formatCurrency(summary?.total_contributions || 0)}
                </div>
                <p className="text-xs text-muted-foreground mt-1">Histórico completo</p>
              </>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Cantidad de Aportes</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {summaryLoading ? (
              <Loader2 className="h-6 w-6 animate-spin" />
            ) : (
              <>
                <div className="text-2xl font-bold">{summary?.contributions_count || 0}</div>
                <p className="text-xs text-muted-foreground mt-1">Registros totales</p>
              </>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Último Aporte</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            {summaryLoading ? (
              <Loader2 className="h-6 w-6 animate-spin" />
            ) : (
              <>
                <div className="text-2xl font-bold">
                  {summary?.last_contribution_date
                    ? new Date(summary.last_contribution_date).toLocaleDateString('es-CO', {
                        day: '2-digit',
                        month: 'short',
                      })
                    : 'N/A'}
                </div>
                <p className="text-xs text-muted-foreground mt-1">Fecha más reciente</p>
              </>
            )}
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Información de Contacto</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-3">
              <Mail className="h-5 w-5 text-muted-foreground" />
              <div>
                <p className="text-sm font-medium">Email</p>
                <p className="text-sm text-muted-foreground">{affiliate.email}</p>
              </div>
            </div>
            {affiliate.phone_number && (
              <div className="flex items-center gap-3">
                <Phone className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Teléfono</p>
                  <p className="text-sm text-muted-foreground">{affiliate.phone_number}</p>
                </div>
              </div>
            )}
            {affiliate.address && (
              <div className="flex items-center gap-3">
                <MapPin className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Dirección</p>
                  <p className="text-sm text-muted-foreground">{affiliate.address}</p>
                </div>
              </div>
            )}
            {affiliate.notes && (
              <div className="flex items-start gap-3">
                <FileText className="h-5 w-5 text-muted-foreground mt-0.5" />
                <div>
                  <p className="text-sm font-medium">Notas</p>
                  <p className="text-sm text-muted-foreground">{affiliate.notes}</p>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Registrar Nuevo Aporte</CardTitle>
            <CardDescription>Añade un nuevo aporte mensual</CardDescription>
          </CardHeader>
          <CardContent>
            {!showContributionForm ? (
              <Button onClick={() => setShowContributionForm(true)} className="w-full">
                <Plus className="mr-2 h-4 w-4" />
                Nuevo Aporte
              </Button>
            ) : (
              <form onSubmit={handleContributionSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="amount">Monto *</Label>
                  <Input
                    id="amount"
                    type="number"
                    step="0.01"
                    value={contributionForm.amount || ''}
                    onChange={(e) =>
                      setContributionForm((prev) => ({ ...prev, amount: Number(e.target.value) }))
                    }
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="contribution_date">Fecha *</Label>
                  <Input
                    id="contribution_date"
                    type="date"
                    value={contributionForm.contribution_date}
                    onChange={(e) =>
                      setContributionForm((prev) => ({ ...prev, contribution_date: e.target.value }))
                    }
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="payment_method">Método de Pago *</Label>
                  <select
                    id="payment_method"
                    value={contributionForm.payment_method}
                    onChange={(e) =>
                      setContributionForm((prev) => ({
                        ...prev,
                        payment_method: e.target.value as PaymentMethod,
                      }))
                    }
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    required
                  >
                    <option value="CASH">Efectivo</option>
                    <option value="TRANSFER">Transferencia</option>
                    <option value="CARD">Tarjeta</option>
                  </select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="reference_number">Referencia</Label>
                  <Input
                    id="reference_number"
                    value={contributionForm.reference_number}
                    onChange={(e) =>
                      setContributionForm((prev) => ({ ...prev, reference_number: e.target.value }))
                    }
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="notes">Notas</Label>
                  <textarea
                    id="notes"
                    value={contributionForm.notes}
                    onChange={(e) =>
                      setContributionForm((prev) => ({ ...prev, notes: e.target.value }))
                    }
                    rows={2}
                    className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  />
                </div>

                <div className="flex gap-2">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setShowContributionForm(false)}
                    className="flex-1"
                  >
                    Cancelar
                  </Button>
                  <Button
                    type="submit"
                    disabled={createContributionMutation.isPending}
                    className="flex-1"
                  >
                    {createContributionMutation.isPending ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      'Guardar'
                    )}
                  </Button>
                </div>
              </form>
            )}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Historial de Aportes</CardTitle>
          <CardDescription>
            Todos los aportes registrados para este afiliado
          </CardDescription>
        </CardHeader>
        <CardContent>
          {contributionsLoading ? (
            <div className="flex justify-center py-8">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : contributions?.results.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              No hay aportes registrados aún.
            </div>
          ) : (
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Fecha</TableHead>
                    <TableHead>Monto</TableHead>
                    <TableHead>Método de Pago</TableHead>
                    <TableHead>Referencia</TableHead>
                    <TableHead>Notas</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {contributions?.results.map((contribution) => (
                    <TableRow key={contribution.id}>
                      <TableCell className="font-medium">
                        {formatDate(contribution.contribution_date)}
                      </TableCell>
                      <TableCell className="font-semibold text-primary">
                        {formatCurrency(Number(contribution.amount))}
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline">
                          {getPaymentMethodLabel(contribution.payment_method)}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-muted-foreground">
                        {contribution.reference_number || '-'}
                      </TableCell>
                      <TableCell className="text-muted-foreground">
                        {contribution.notes || '-'}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

