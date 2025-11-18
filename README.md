# Sistema de Gestión de Afiliados - Cooperativa

Sistema interno para la gestión de afiliados y sus aportes mensuales en una cooperativa.

## 📋 Descripción del Proyecto

Aplicación full-stack que permite administrar afiliados de una cooperativa y realizar el seguimiento de sus aportes mensuales. El sistema implementa Clean Architecture + Domain-Driven Design (DDD) + principios SOLID para garantizar un código mantenible, escalable y de alta calidad.

### Funcionalidades Principales

- ✅ Registro y gestión de afiliados
- ✅ Registro de aportes mensuales por afiliado
- ✅ Consulta de histórico de aportes
- ✅ Visualización de resumen estadístico por afiliado
- ✅ Filtros avanzados de búsqueda
- ✅ API REST completamente documentada

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.11+**
- **Django 5.0.1** - Framework web
- **Django REST Framework 3.14.0** - API REST
- **PostgreSQL 16** - Base de datos
- **django-filter** - Filtros avanzados
- **django-cors-headers** - CORS para comunicación con frontend
- **python-decouple** - Gestión de variables de entorno

### Frontend
- **React 18+** - Framework UI
- **TypeScript** - Tipado estático
- **shadcn/ui** - Componentes UI
- **Vite** - Build tool
- *(En desarrollo)*

### DevOps & Herramientas
- **Docker & Docker Compose** - Containerización
- **PostgreSQL** - Base de datos relacional
- **Git** - Control de versiones
- **pytest** - Testing framework

---

## 📁 Estructura del Proyecto

```
JlOutsourcer/
│
├── backend/                          # Aplicación Django
│   ├── config/                       # Configuración del proyecto
│   │   ├── settings.py              # Configuración principal
│   │   ├── urls.py                  # URLs principales
│   │   └── wsgi.py
│   │
│   ├── app_affiliate/                # Módulo de dominio (Clean Architecture)
│   │   ├── domain/                  # 💎 Capa de Dominio
│   │   │   ├── models/              # Entidades: Affiliate, Contribution
│   │   │   ├── interfaces/          # Interfaces (contratos abstractos)
│   │   │   └── exceptions.py        # Excepciones del dominio
│   │   │
│   │   ├── application/             # 🎯 Capa de Aplicación
│   │   │   └── services/            # Casos de uso
│   │   │
│   │   ├── infrastructure/          # 🔧 Capa de Infraestructura
│   │   │   ├── repositories/        # Implementación ORM
│   │   │   └── services/            # Servicios técnicos
│   │   │
│   │   └── api/                     # 🌐 Capa de Presentación
│   │       ├── serializers/         # Serialización JSON
│   │       ├── views/               # Endpoints REST
│   │       ├── filters.py           # Filtros de búsqueda
│   │       └── urls.py              # Rutas de la API
│   │
│   ├── manage.py                    # CLI de Django
│   ├── requirements.txt             # Dependencias Python
│   └── Dockerfile                   # Configuración Docker backend
│
├── frontend/                        # Aplicación React
│   └── (En desarrollo)
│
├── docker-compose.yml               # Orquestación de servicios
├── .env.example                     # Plantilla de variables de entorno
├── .env                             # Variables de entorno (no versionado)
└── README.md                        # Este archivo
```

---

## 🚀 Instalación y Configuración

### Prerrequisitos

- Docker & Docker Compose instalados
- Git
- *(Opcional)* Python 3.11+ y Node.js 18+ para desarrollo local

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd JlOutsourcer
```

### 2. Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp env.example .env

# Editar el archivo .env con tus configuraciones
nano .env
```

**Variables importantes:**
```env
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
DB_NAME=cooperative_db
DB_USER=cooperative_user
DB_PASSWORD=cooperative_pass
DB_HOST=db
DB_PORT=5432
```

---

## 🐳 Levantar el Proyecto con Docker (Recomendado)

### Opción 1: Comando Único

```bash
# Construir y levantar todos los servicios
docker-compose up --build
```

### Opción 2: Paso a Paso

```bash
# 1. Construir las imágenes
docker-compose build

# 2. Levantar los servicios en background
docker-compose up -d

# 3. Ver los logs
docker-compose logs -f

# 4. Verificar el estado
docker-compose ps
```

### Servicios Disponibles

- **Backend (Django):** http://localhost:8000
- **Base de Datos (PostgreSQL):** localhost:5432
- **Frontend (React):** http://localhost:3000 *(próximamente)*

### Comandos Útiles de Docker

```bash
# Detener los servicios
docker-compose down

# Detener y eliminar volúmenes (⚠️ elimina datos de BD)
docker-compose down -v

# Ver logs de un servicio específico
docker-compose logs web
docker-compose logs db

# Ejecutar comandos dentro del contenedor
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py shell

# Reiniciar un servicio
docker-compose restart web
```

---

## 🔧 Levantar el Backend (Sin Docker)

### 1. Crear Entorno Virtual

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

```bash
# Crear archivo .env en la raíz del proyecto
# Asegúrate de cambiar DB_HOST=localhost (no 'db')
```

### 4. Ejecutar Migraciones

```bash
python manage.py migrate
```

### 5. Crear Superusuario (Opcional)

```bash
python manage.py createsuperuser
```

### 6. Iniciar Servidor de Desarrollo

```bash
python manage.py runserver
```

El backend estará disponible en http://localhost:8000

---

## ⚛️ Levantar el Frontend (En Desarrollo)

```bash
# Próximamente...
cd frontend
npm install
npm run dev
```

---

## 📡 API Endpoints

### Base URL: `http://localhost:8000/api`

#### Afiliados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/affiliates/` | Listar afiliados (paginado, con filtros) |
| POST | `/affiliates/` | Crear nuevo afiliado |
| GET | `/affiliates/{id}/` | Obtener detalle de un afiliado |
| PUT | `/affiliates/{id}/` | Actualizar afiliado completo |
| PATCH | `/affiliates/{id}/status/` | Cambiar estado (ACTIVE/INACTIVE) |
| GET | `/affiliates/{id}/summary/` | Obtener resumen estadístico |

#### Aportes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/affiliates/{id}/contributions/` | Listar aportes de un afiliado |
| POST | `/affiliates/{id}/contributions/` | Registrar nuevo aporte |

### Filtros Disponibles

```bash
# Filtrar por estado
GET /api/affiliates/?status=ACTIVE

# Filtrar por número de documento
GET /api/affiliates/?document_number=123456789

# Búsqueda parcial por nombre
GET /api/affiliates/?full_name=juan

# Paginación
GET /api/affiliates/?page=2
```

### Ejemplo de Petición

```bash
# Crear afiliado
curl -X POST http://localhost:8000/api/affiliates/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Juan Pérez",
    "document_type": "CC",
    "document_number": "123456789",
    "email": "juan@example.com",
    "status": "ACTIVE"
  }'
```

---

## 🏗️ Arquitectura Aplicada

### Clean Architecture + DDD + SOLID

El proyecto implementa una arquitectura en capas que garantiza:
- **Independencia de frameworks:** La lógica de negocio no depende de Django
- **Testeable:** Cada capa puede probarse independientemente
- **Mantenible:** Cambios localizados sin efectos secundarios
- **Escalable:** Fácil agregar nuevas funcionalidades

#### Capas de la Arquitectura

```
┌─────────────────────────────────────────┐
│         API Layer (Presentación)         │  ← HTTP, Serializers, Views
├─────────────────────────────────────────┤
│      Application Layer (Casos de Uso)   │  ← CreateAffiliateService
├─────────────────────────────────────────┤
│      Domain Layer (Lógica de Negocio)   │  ← Entities, Value Objects
├─────────────────────────────────────────┤
│   Infrastructure Layer (Detalles Técnicos) │  ← ORM, Repositories
└─────────────────────────────────────────┘
```

#### 1. **Domain Layer (Dominio)** 💎
- **Propósito:** Contiene la lógica de negocio pura
- **Contenido:** Entidades, Value Objects, Interfaces, Excepciones
- **Regla:** NO depende de ninguna otra capa
- **Ejemplo:** `Affiliate.activate()`, `Email`, `Money`

#### 2. **Application Layer (Aplicación)** 🎯
- **Propósito:** Coordina los casos de uso del negocio
- **Contenido:** Services (casos de uso)
- **Regla:** Orquesta domain e infrastructure
- **Ejemplo:** `CreateAffiliateService`, `RegisterContributionService`

#### 3. **Infrastructure Layer (Infraestructura)** 🔧
- **Propósito:** Implementa detalles técnicos
- **Contenido:** Modelos ORM, Repositorios, Servicios externos
- **Regla:** Implementa interfaces definidas en domain
- **Ejemplo:** `DjangoAffiliateRepository`, `AffiliateORM`

#### 4. **API Layer (Presentación)** 🌐
- **Propósito:** Maneja comunicación HTTP
- **Contenido:** Serializers, Views, URLs, Filtros
- **Regla:** Solo transforma HTTP ↔ Application layer
- **Ejemplo:** `AffiliateViewSet`, `AffiliateSerializer`

### Principios SOLID Aplicados

- **S**ingle Responsibility: Cada clase tiene una única responsabilidad
- **O**pen/Closed: Abierto a extensión, cerrado a modificación
- **L**iskov Substitution: Las implementaciones son intercambiables
- **I**nterface Segregation: Interfaces específicas y cohesivas
- **D**ependency Inversion: Dependemos de abstracciones, no implementaciones

### Flujo de una Request

```
1. HTTP Request
   ↓
2. API Layer → AffiliateViewSet.create()
   ↓
3. Serializer valida JSON
   ↓
4. Application Layer → CreateAffiliateService.execute()
   ↓
5. Domain Layer → Affiliate.create() (valida reglas de negocio)
   ↓
6. Infrastructure → DjangoAffiliateRepository.save()
   ↓
7. PostgreSQL
   ↓
8. HTTP Response (JSON)
```

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
docker-compose exec web pytest

# Tests con coverage
docker-compose exec web pytest --cov=app_affiliate

# Tests específicos
docker-compose exec web pytest app_affiliate/tests/test_affiliates.py
```

---

## 📊 Modelo de Datos

### Affiliate (Afiliado)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | ID único (auto-generado) |
| full_name | String(255) | Nombre completo |
| document_type | Enum | CC, CE, NIT |
| document_number | String(20) | Número de documento (único) |
| email | Email | Correo electrónico |
| status | Enum | ACTIVE, INACTIVE |
| created_at | DateTime | Fecha de creación |
| updated_at | DateTime | Fecha de actualización |

### Contribution (Aporte)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | ID único (auto-generado) |
| affiliate | ForeignKey | Relación con Affiliate |
| amount | Decimal | Monto del aporte |
| contribution_date | Date | Fecha del aporte |
| payment_method | Enum | CASH, TRANSFER, CARD |
| created_at | DateTime | Fecha de registro |
| updated_at | DateTime | Fecha de actualización |

**Índices:**
- `affiliate_id` + `contribution_date` (compuesto) para optimizar consultas

---

## 📝 Estándares de Código

### Convenciones de Nombres

- **Clases:** `PascalCase` (Ej: `AffiliateService`, `Contribution`)
- **Funciones/métodos:** `snake_case` (Ej: `create_affiliate()`, `get_summary()`)
- **Variables:** `snake_case` (Ej: `total_amount`, `affiliate_id`)
- **Constantes:** `UPPER_SNAKE_CASE` (Ej: `MAX_PAGE_SIZE`)

### Idioma

- **Código:** Inglés (clases, funciones, variables)
- **Comentarios:** Español
- **Documentación:** Español

---

## 🔒 Seguridad

- ✅ Variables sensibles en archivo `.env` (no versionado)
- ✅ SECRET_KEY único en producción
- ✅ DEBUG=False en producción
- ✅ CORS configurado para orígenes específicos
- ✅ Validación de datos en múltiples capas
- ✅ PostgreSQL con credenciales seguras

---

## 🚧 Limitaciones Conocidas y Mejoras Futuras

### Limitaciones Actuales

- [ ] No hay autenticación/autorización implementada (JWT pendiente)
- [ ] No hay paginación customizable por usuario
- [ ] Falta documentación Swagger/OpenAPI
- [ ] No hay tests e2e del frontend

### Mejoras Futuras

#### Backend
- [ ] Implementar autenticación JWT
- [ ] Agregar roles y permisos (admin, operador, solo lectura)
- [ ] Webhooks para notificaciones de aportes
- [ ] Exportación de reportes (PDF, Excel)
- [ ] Logs estructurados y monitoreo
- [ ] Cache con Redis para consultas frecuentes
- [ ] Auditoría de cambios (tracking de modificaciones)

#### Frontend
- [ ] Dashboard con gráficos estadísticos
- [ ] Notificaciones en tiempo real
- [ ] Modo offline con sincronización
- [ ] Impresión de recibos de aportes
- [ ] Temas claro/oscuro

#### DevOps
- [ ] CI/CD con GitHub Actions
- [ ] Deploy automatizado
- [ ] Backups automáticos de BD
- [ ] Monitoreo con Prometheus/Grafana
- [ ] Logs centralizados con ELK Stack

---

## 👥 Contribuciones

### Workflow de Desarrollo

```bash
# 1. Crear rama desde main
git checkout -b feature/nombre-funcionalidad

# 2. Hacer commits descriptivos
git commit -m "feat: add affiliate summary endpoint"

# 3. Push y Pull Request
git push origin feature/nombre-funcionalidad
```

### Commits Convencionales

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `refactor:` Refactorización de código
- `test:` Agregar o modificar tests
- `chore:` Tareas de mantenimiento

---

## 📄 Licencia

Este proyecto es parte de una prueba técnica para Core Apps.

---

## 📞 Contacto

Para consultas o soporte, contactar a: [Tu email o información de contacto]

---

## 🙏 Agradecimientos

Desarrollado como parte del proceso de selección para Core Apps, aplicando las mejores prácticas de arquitectura de software y desarrollo profesional.

---

**Última actualización:** Noviembre 2025

