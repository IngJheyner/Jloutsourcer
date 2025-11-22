# 🧪 Guía de Pruebas - Sistema de Cooperativa

Guía paso a paso para probar todas las funcionalidades del sistema.

## 🚀 Iniciar el Sistema Completo

### Con Docker (Recomendado)

```bash
# 1. Levantar backend y base de datos
docker-compose up -d

# 2. Verificar que el backend esté corriendo
curl http://localhost:8000/api/affiliates/

# 3. En otra terminal, levantar frontend
cd frontend
npm install  # Solo la primera vez
npm run dev
```

### Sin Docker

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # o venv\Scripts\activate en Windows
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## ✅ Plan de Pruebas

### 1️⃣ Probar Backend (API REST)

#### Crear Afiliado
```bash
curl -X POST http://localhost:8000/api/affiliates/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Juan Pérez García",
    "document_type": "CC",
    "document_number": "123456789",
    "email": "juan.perez@example.com",
    "status": "ACTIVE",
    "phone_number": "+57 300 1234567",
    "address": "Calle 123 #45-67, Bogotá"
  }'
```

#### Listar Afiliados
```bash
curl http://localhost:8000/api/affiliates/
```

#### Filtrar por Estado
```bash
curl "http://localhost:8000/api/affiliates/?status=ACTIVE"
```

#### Ver Detalle
```bash
curl http://localhost:8000/api/affiliates/1/
```

#### Registrar Aporte
```bash
curl -X POST http://localhost:8000/api/affiliates/1/contributions/ \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50000,
    "contribution_date": "2025-11-21",
    "payment_method": "TRANSFER",
    "reference_number": "TRF-001"
  }'
```

#### Ver Resumen
```bash
curl http://localhost:8000/api/affiliates/1/summary/ | jq
```

### 2️⃣ Probar Frontend (UI)

1. **Abrir en navegador:** http://localhost:5173

2. **Navegar a Afiliados:** Click en "Afiliados" en el header

3. **Crear Nuevo Afiliado:**
   - Click en "Nuevo Afiliado"
   - Llenar formulario
   - Click en "Guardar Afiliado"
   - Verificar redirección a lista

4. **Buscar y Filtrar:**
   - Usar barra de búsqueda
   - Filtrar por estado
   - Verificar resultados en tiempo real

5. **Ver Detalle:**
   - Click en "Ver Detalle" de cualquier afiliado
   - Verificar cards de estadísticas
   - Revisar información de contacto

6. **Registrar Aporte:**
   - En la página de detalle
   - Click en "Nuevo Aporte"
   - Llenar formulario
   - Click en "Guardar"
   - Verificar que aparece en la tabla
   - Verificar que se actualizan las estadísticas

7. **Cambiar Estado:**
   - Click en "Cambiar a Inactivo"
   - Verificar cambio de badge

---

## 🎯 Casos de Prueba Específicos

### ✅ Validaciones Frontend

1. **Email inválido:**
   - Ingresar "email-sin-arroba"
   - Debe mostrar error de validación

2. **Nombre muy corto:**
   - Ingresar "AB"
   - Debe mostrar: "Full name must be at least 3 characters long"

3. **Documento duplicado:**
   - Crear afiliado con documento existente
   - Debe mostrar: "Affiliate with document XXX already exists"

4. **Fecha futura en aporte:**
   - Intentar registrar aporte con fecha 2026
   - Debe mostrar: "Contribution date cannot be in the future"

### ✅ Funcionalidades Complejas

1. **Paginación:**
   - Crear más de 10 afiliados
   - Verificar botones "Anterior" / "Siguiente"

2. **Resumen Estadístico:**
   - Ver página de detalle
   - Verificar que los números coinciden
   - Registrar nuevo aporte
   - Verificar que se actualiza el total

3. **Responsive:**
   - Abrir en móvil (o DevTools → Toggle device toolbar)
   - Verificar que todo se adapta correctamente

---

## 📊 Datos de Prueba Completos

```bash
# Crear 3 afiliados
curl -X POST http://localhost:8000/api/affiliates/ -H "Content-Type: application/json" -d '{"full_name": "Juan Pérez", "document_type": "CC", "document_number": "123456789", "email": "juan@example.com"}'

curl -X POST http://localhost:8000/api/affiliates/ -H "Content-Type: application/json" -d '{"full_name": "María González", "document_type": "CC", "document_number": "987654321", "email": "maria@example.com"}'

curl -X POST http://localhost:8000/api/affiliates/ -H "Content-Type: application/json" -d '{"full_name": "Empresa XYZ S.A.S.", "document_type": "NIT", "document_number": "900123456-7", "email": "contacto@xyz.com"}'

# Registrar aportes para Juan (ID=1)
curl -X POST http://localhost:8000/api/affiliates/1/contributions/ -H "Content-Type: application/json" -d '{"amount": 50000, "contribution_date": "2025-11-01", "payment_method": "TRANSFER"}'

curl -X POST http://localhost:8000/api/affiliates/1/contributions/ -H "Content-Type: application/json" -d '{"amount": 75000, "contribution_date": "2025-11-15", "payment_method": "CASH"}'

# Ver resumen
curl http://localhost:8000/api/affiliates/1/summary/ | jq
```

---

## 🐛 Troubleshooting

### Backend no responde
```bash
docker-compose logs web
# o
docker-compose restart web
```

### Frontend no carga
```bash
# Verificar que VITE_API_BASE_URL esté configurado
cat frontend/.env

# Reiniciar servidor
cd frontend
npm run dev
```

### CORS Error
```bash
# Verificar configuración en .env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Reiniciar backend
docker-compose restart web
```

### Base de datos vacía
```bash
# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Verificar tablas
docker-compose exec db psql -U cooperative_user -d cooperative_db -c "\dt"
```

---

## ✨ Checklist de Funcionalidades

- [ ] ✅ Crear afiliado desde UI
- [ ] ✅ Listar afiliados con paginación
- [ ] ✅ Filtrar por nombre (búsqueda parcial)
- [ ] ✅ Filtrar por estado (ACTIVE/INACTIVE)
- [ ] ✅ Ver detalle de afiliado
- [ ] ✅ Cambiar estado de afiliado
- [ ] ✅ Registrar aporte desde UI
- [ ] ✅ Ver historial de aportes
- [ ] ✅ Ver resumen estadístico
- [ ] ✅ Validaciones en formularios
- [ ] ✅ Manejo de errores de API
- [ ] ✅ Responsive design
- [ ] ✅ Loaders durante carga
- [ ] ✅ Navegación SPA

¡Todas las funcionalidades implementadas! 🎉
