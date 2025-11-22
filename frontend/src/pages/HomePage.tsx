import { Link } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Users, DollarSign, TrendingUp } from 'lucide-react';

export function HomePage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold tracking-tight">Bienvenido al Sistema de Cooperativa</h1>
        <p className="text-muted-foreground mt-2">
          Gestiona afiliados y sus aportes mensuales de forma eficiente.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Afiliados</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Gestionar</div>
            <p className="text-xs text-muted-foreground mt-1">
              Crear, editar y ver afiliados
            </p>
            <Link to="/affiliates">
              <Button className="mt-4 w-full" size="sm">
                Ver Afiliados
              </Button>
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Aportes</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Registrar</div>
            <p className="text-xs text-muted-foreground mt-1">
              Registrar aportes mensuales
            </p>
            <Link to="/affiliates">
              <Button className="mt-4 w-full" size="sm" variant="secondary">
                Ir a Afiliados
              </Button>
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Resúmenes</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Consultar</div>
            <p className="text-xs text-muted-foreground mt-1">
              Ver estadísticas de aportes
            </p>
            <Link to="/affiliates">
              <Button className="mt-4 w-full" size="sm" variant="outline">
                Ver Resúmenes
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Características del Sistema</CardTitle>
          <CardDescription>Funcionalidades disponibles</CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2">
            <li className="flex items-start gap-2">
              <span className="text-primary">✓</span>
              <span>Registro completo de afiliados con información de contacto</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary">✓</span>
              <span>Gestión de aportes mensuales con múltiples métodos de pago</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary">✓</span>
              <span>Histórico detallado de aportes por afiliado</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary">✓</span>
              <span>Resúmenes estadísticos con totales y contadores</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary">✓</span>
              <span>Filtros avanzados por estado, documento y nombre</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary">✓</span>
              <span>Interfaz responsiva y moderna con shadcn/ui</span>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}

