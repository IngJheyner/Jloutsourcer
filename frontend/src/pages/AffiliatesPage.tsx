import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { affiliatesApi } from '@/services/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Plus, Search, Eye, Loader2 } from 'lucide-react';
import type { AffiliateStatus } from '@/types';

export function AffiliatesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<AffiliateStatus | ''>('');
  const [page, setPage] = useState(1);

  const { data, isLoading, error } = useQuery({
    queryKey: ['affiliates', page, statusFilter, searchTerm],
    queryFn: () =>
      affiliatesApi.getAll({
        page,
        status: statusFilter || undefined,
        full_name: searchTerm || undefined,
      }),
  });

  const getStatusBadge = (status: AffiliateStatus) => {
    return status === 'ACTIVE' ? (
      <Badge variant="success">Activo</Badge>
    ) : (
      <Badge variant="destructive">Inactivo</Badge>
    );
  };

  const getDocumentTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      CC: 'Cédula',
      CE: 'Cédula Extranjería',
      NIT: 'NIT',
    };
    return labels[type] || type;
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Afiliados</h1>
          <p className="text-muted-foreground mt-1">
            Gestiona los afiliados de la cooperativa
          </p>
        </div>
        <Link to="/affiliates/new">
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Nuevo Afiliado
          </Button>
        </Link>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Filtros</CardTitle>
          <CardDescription>Busca y filtra afiliados</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Buscar por nombre o documento..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-9"
              />
            </div>
            <div>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value as AffiliateStatus | '')}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              >
                <option value="">Todos los estados</option>
                <option value="ACTIVE">Activo</option>
                <option value="INACTIVE">Inactivo</option>
              </select>
            </div>
            <Button
              variant="outline"
              onClick={() => {
                setSearchTerm('');
                setStatusFilter('');
                setPage(1);
              }}
            >
              Limpiar Filtros
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Lista de Afiliados</CardTitle>
          <CardDescription>
            {data?.count} afiliado{data?.count !== 1 ? 's' : ''} encontrado{data?.count !== 1 ? 's' : ''}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex justify-center items-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : error ? (
            <div className="text-center py-12 text-destructive">
              Error al cargar los afiliados. Verifica que el backend esté corriendo.
            </div>
          ) : data?.results.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">
              No se encontraron afiliados. {searchTerm || statusFilter ? 'Intenta cambiar los filtros.' : 'Crea el primero.'}
            </div>
          ) : (
            <>
              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Nombre</TableHead>
                      <TableHead>Documento</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Estado</TableHead>
                      <TableHead className="text-right">Acciones</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {data?.results.map((affiliate) => (
                      <TableRow key={affiliate.id}>
                        <TableCell className="font-medium">{affiliate.full_name}</TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="text-sm font-medium">
                              {getDocumentTypeLabel(affiliate.document_type)}
                            </div>
                            <div className="text-sm text-muted-foreground">
                              {affiliate.document_number}
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>{affiliate.email}</TableCell>
                        <TableCell>{getStatusBadge(affiliate.status)}</TableCell>
                        <TableCell className="text-right">
                          <Link to={`/affiliates/${affiliate.id}`}>
                            <Button variant="ghost" size="sm">
                              <Eye className="mr-2 h-4 w-4" />
                              Ver Detalle
                            </Button>
                          </Link>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>

              {(data?.next || data?.previous) && (
                <div className="flex justify-between items-center mt-4">
                  <Button
                    variant="outline"
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                    disabled={!data.previous}
                  >
                    Anterior
                  </Button>
                  <span className="text-sm text-muted-foreground">Página {page}</span>
                  <Button
                    variant="outline"
                    onClick={() => setPage((p) => p + 1)}
                    disabled={!data.next}
                  >
                    Siguiente
                  </Button>
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

