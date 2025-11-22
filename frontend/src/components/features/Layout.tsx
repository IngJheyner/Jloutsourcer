import { Link, Outlet, useLocation } from 'react-router-dom';
import { Users, Home } from 'lucide-react';
import { cn } from '@/lib/utils';

export function Layout() {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Inicio', icon: Home },
    { path: '/affiliates', label: 'Afiliados', icon: Users },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Users className="h-8 w-8 text-primary" />
              <h1 className="text-2xl font-bold text-gray-900">Sistema de Cooperativa</h1>
            </div>
            <nav className="flex gap-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={cn(
                      'flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors',
                      isActive
                        ? 'bg-primary text-primary-foreground'
                        : 'text-gray-700 hover:bg-gray-100'
                    )}
                  >
                    <Icon className="h-4 w-4" />
                    {item.label}
                  </Link>
                );
              })}
            </nav>
          </div>
        </div>
      </header>
      <main className="container mx-auto px-4 py-8">
        <Outlet />
      </main>
    </div>
  );
}

