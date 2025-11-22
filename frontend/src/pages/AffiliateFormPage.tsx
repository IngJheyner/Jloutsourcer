import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { affiliatesApi } from '@/services/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { ArrowLeft, Save, Loader2 } from 'lucide-react';
import type { CreateAffiliateRequest, DocumentType, AffiliateStatus } from '@/types';

export function AffiliateFormPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<CreateAffiliateRequest>({
    full_name: '',
    document_type: 'CC',
    document_number: '',
    email: '',
    status: 'ACTIVE',
    phone_number: '',
    address: '',
    notes: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const createMutation = useMutation({
    mutationFn: (data: CreateAffiliateRequest) => affiliatesApi.create(data),
    onSuccess: () => {
      navigate('/affiliates');
    },
    onError: (error: any) => {
      if (error.response?.data) {
        const apiErrors: Record<string, string> = {};
        Object.entries(error.response.data).forEach(([key, value]) => {
          if (Array.isArray(value)) {
            apiErrors[key] = value[0];
          } else if (typeof value === 'string') {
            apiErrors[key] = value;
          } else if (value && typeof value === 'object' && 'error' in value) {
            apiErrors[key] = (value as any).error;
          }
        });
        setErrors(apiErrors);
      }
    },
  });

  const handleChange = (field: keyof CreateAffiliateRequest, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const dataToSend = {
      ...formData,
      phone_number: formData.phone_number || undefined,
      address: formData.address || undefined,
      notes: formData.notes || undefined,
    };
    createMutation.mutate(dataToSend);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="outline" size="icon" onClick={() => navigate('/affiliates')}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Nuevo Afiliado</h1>
          <p className="text-muted-foreground mt-1">Completa el formulario para registrar un nuevo afiliado</p>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Información del Afiliado</CardTitle>
          <CardDescription>Campos marcados con * son obligatorios</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid gap-6 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="full_name">Nombre Completo *</Label>
                <Input
                  id="full_name"
                  value={formData.full_name}
                  onChange={(e) => handleChange('full_name', e.target.value)}
                  placeholder="Juan Pérez García"
                  required
                />
                {errors.full_name && (
                  <p className="text-sm text-destructive">{errors.full_name}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email *</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleChange('email', e.target.value)}
                  placeholder="juan.perez@example.com"
                  required
                />
                {errors.email && <p className="text-sm text-destructive">{errors.email}</p>}
              </div>

              <div className="space-y-2">
                <Label htmlFor="document_type">Tipo de Documento *</Label>
                <select
                  id="document_type"
                  value={formData.document_type}
                  onChange={(e) => handleChange('document_type', e.target.value)}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  required
                >
                  <option value="CC">Cédula de Ciudadanía</option>
                  <option value="CE">Cédula de Extranjería</option>
                  <option value="NIT">NIT</option>
                </select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="document_number">Número de Documento *</Label>
                <Input
                  id="document_number"
                  value={formData.document_number}
                  onChange={(e) => handleChange('document_number', e.target.value)}
                  placeholder="123456789"
                  required
                />
                {errors.document_number && (
                  <p className="text-sm text-destructive">{errors.document_number}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="phone_number">Teléfono</Label>
                <Input
                  id="phone_number"
                  value={formData.phone_number}
                  onChange={(e) => handleChange('phone_number', e.target.value)}
                  placeholder="+57 300 1234567"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="status">Estado *</Label>
                <select
                  id="status"
                  value={formData.status}
                  onChange={(e) => handleChange('status', e.target.value)}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  required
                >
                  <option value="ACTIVE">Activo</option>
                  <option value="INACTIVE">Inactivo</option>
                </select>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="address">Dirección</Label>
              <Input
                id="address"
                value={formData.address}
                onChange={(e) => handleChange('address', e.target.value)}
                placeholder="Calle 123 #45-67, Bogotá"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="notes">Notas</Label>
              <textarea
                id="notes"
                value={formData.notes}
                onChange={(e) => handleChange('notes', e.target.value)}
                placeholder="Información adicional..."
                rows={4}
                className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              />
            </div>

            {errors.error && (
              <div className="p-4 bg-destructive/10 text-destructive rounded-md">
                {errors.error}
              </div>
            )}

            <div className="flex gap-3 justify-end">
              <Button type="button" variant="outline" onClick={() => navigate('/affiliates')}>
                Cancelar
              </Button>
              <Button type="submit" disabled={createMutation.isPending}>
                {createMutation.isPending ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Guardando...
                  </>
                ) : (
                  <>
                    <Save className="mr-2 h-4 w-4" />
                    Guardar Afiliado
                  </>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

