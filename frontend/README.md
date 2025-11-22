# Frontend - Sistema de Cooperativa

Frontend moderno para el sistema de gestión de afiliados y aportes.

## 🛠️ Stack Tecnológico

- **React 19** - Biblioteca UI
- **TypeScript** - Tipado estático
- **Vite 7** - Build tool y dev server
- **shadcn/ui** - Sistema de componentes UI
- **TailwindCSS 4** - Framework CSS utility-first
- **React Router 7** - Enrutamiento SPA
- **TanStack Query (React Query)** - Gestión de estado servidor
- **Axios** - Cliente HTTP
- **Lucide React** - Iconos

## 🚀 Instalación y Desarrollo

### 1. Instalar Dependencias

```bash
npm install
```

### 2. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto frontend:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### 3. Iniciar Servidor de Desarrollo

```bash
npm run dev
```

El frontend estará disponible en: **http://localhost:5173**

### 4. Build para Producción

```bash
npm run build
npm run preview  # Previsualizar el build
```

## 📁 Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/           # Componentes reutilizables
│   │   ├── ui/              # Componentes shadcn/ui (Button, Card, etc.)
│   │   └── features/        # Componentes de funcionalidad (Layout)
│   ├── pages/               # Páginas de la aplicación
│   │   ├── HomePage.tsx
│   │   ├── AffiliatesPage.tsx
│   │   ├── AffiliateFormPage.tsx
│   │   └── AffiliateDetailPage.tsx
│   ├── services/            # API clients
│   │   └── api.ts           # Cliente Axios configurado
│   ├── types/               # Definiciones TypeScript
│   │   └── index.ts         # Tipos compartidos
│   ├── lib/                 # Utilidades
│   │   └── utils.ts         # Funciones helper (cn, formatters)
│   ├── hooks/               # Custom React hooks (por agregar)
│   ├── App.tsx              # Componente raíz
│   ├── main.tsx             # Entry point
│   └── index.css            # Estilos globales
├── package.json
├── vite.config.ts           # Configuración Vite
├── tsconfig.json            # Configuración TypeScript
└── tailwind.config.js       # Configuración Tailwind
```

## 🎨 Componentes UI Disponibles

Los componentes de shadcn/ui ya incluidos:

- **Button** - Botones con múltiples variantes
- **Card** - Contenedores de contenido
- **Input** - Campos de entrada
- **Label** - Etiquetas para formularios
- **Badge** - Insignias de estado
- **Table** - Tablas de datos

## 📄 Páginas Implementadas

### 1. Home Page (`/`)
- Dashboard con resumen de funcionalidades
- Tarjetas de navegación rápida
- Lista de características del sistema

### 2. Affiliates List (`/affiliates`)
- Lista paginada de afiliados
- Filtros por nombre, documento y estado
- Búsqueda en tiempo real
- Navegación a detalle

### 3. Affiliate Form (`/affiliates/new`)
- Formulario completo de creación
- Validaciones en tiempo real
- Manejo de errores de API
- Campos opcionales

### 4. Affiliate Detail (`/affiliates/:id`)
- Vista detallada del afiliado
- Resumen estadístico (total aportes, cantidad, última fecha)
- Formulario para registrar nuevos aportes
- Tabla de histórico de aportes
- Cambio de estado (activo/inactivo)

## 🔗 Integración con API

El frontend consume la API REST del backend Django. La configuración se encuentra en `src/services/api.ts`:

- **Base URL:** Definida en variable de entorno `VITE_API_BASE_URL`
- **Cliente:** Axios con configuración centralizada
- **Cache:** TanStack Query para optimización de requests
- **Tipado:** Todos los endpoints tienen tipos TypeScript

## 🎯 Características

✅ **Responsive Design** - Adaptable a móviles, tablets y desktop
✅ **Tipado Fuerte** - TypeScript en todo el proyecto
✅ **Cache Inteligente** - TanStack Query reduce llamadas innecesarias
✅ **Validaciones** - Tanto en cliente como integración con errores del servidor
✅ **UX Moderna** - Loaders, estados de carga, feedback visual
✅ **Componentes Reutilizables** - Arquitectura modular
✅ **Dark Mode Ready** - Preparado para tema oscuro (por activar)

## 🚧 Mejoras Futuras

- [ ] Implementar tests con Vitest + React Testing Library
- [ ] Agregar toast notifications
- [ ] Implementar dark mode toggle
- [ ] Agregar más filtros avanzados
- [ ] Exportar reportes (PDF, Excel)
- [ ] Implementar gráficos de estadísticas
- [ ] Agregar paginación en historial de aportes
- [ ] Implementar búsqueda avanzada con múltiples criterios
