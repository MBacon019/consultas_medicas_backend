# ConsultasAPI

API REST para gestión de consultas médicas, construida con Django + Django REST Framework.

## Stack

- Python 3.12
- Django 6+
- Django REST Framework
- Simple JWT (autenticación)
- PostgreSQL
- django-filter

## URL en producción

```
https://bacon-consultas.uaeftt-ute.site/api/
```

## 7 Tablas de Base de Datos

| Modelo | Descripción |
|---|---|
| `Especialidad` | Especialidades médicas (Cardiología, Pediatría, etc.) |
| `Medico` | Médicos con su especialidad asignada |
| `Paciente` | Datos personales de los pacientes |
| `Horario` | Horarios de atención de cada médico |
| `Cita` | Citas agendadas (paciente + médico + fecha/hora) |
| `Consulta` | Registro clínico de cada cita atendida |
| `Receta` | Medicamentos recetados por consulta |

## Endpoints principales

```
GET  /api/health/

POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
POST /api/auth/token/refresh/

GET/POST   /api/especialidades/
GET/POST   /api/medicos/
GET/POST   /api/pacientes/
GET/POST   /api/citas/
GET/POST   /api/consultas/

POST /api/citas/agendar/
POST /api/citas/{id}/confirmar/
POST /api/citas/{id}/cancelar/
POST /api/citas/{id}/cambiar-estado/

POST /api/consultas/{id}/agregar-receta/
GET  /api/consultas/{id}/recetas/

GET  /api/especialidades/stats/
GET  /api/medicos/stats/
GET  /api/pacientes/stats/
GET  /api/citas/stats/
GET  /api/consultas/stats/

GET  /api/medicos/{id}/citas/
GET  /api/pacientes/{id}/historial/
GET  /api/especialidades/{id}/medicos/
```

## Configuración

```bash
cp .env.example .env
# Editar .env con tus credenciales

uv run manage.py migrate
uv run manage.py createsuperuser
uv run manage.py runserver
```

## Tests

```bash
uv run manage.py test clinic
```

---

## Autenticación

La API usa **JWT (JSON Web Tokens)**. Todos los endpoints excepto `/health/`, `/auth/register/` y `/auth/login/` requieren el header `Authorization`.

### 1. Obtener token (login)

```bash
curl -X POST https://bacon-consultas.uaeftt-ute.site/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "tu_password"}'
```

Respuesta:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "user_id": 1,
  "username": "admin",
  "is_staff": true
}
```

### 2. Usar el token en cada petición

```bash
curl -X GET https://bacon-consultas.uaeftt-ute.site/api/pacientes/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGci..."
```

### 3. Renovar token expirado

```bash
curl -X POST https://bacon-consultas.uaeftt-ute.site/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "eyJ0eXAiOiJKV1QiLCJhbGci..."}'
```

### 4. Cerrar sesión (invalidar token)

```bash
curl -X POST https://bacon-consultas.uaeftt-ute.site/api/auth/logout/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

---

## Listado completo de endpoints

### Autenticación

| Método | Endpoint | Descripción | Auth requerida |
|---|---|---|---|
| POST | `/api/auth/register/` | Registrar nuevo usuario | No |
| POST | `/api/auth/login/` | Obtener token JWT | No |
| POST | `/api/auth/logout/` | Invalidar token | Sí |
| POST | `/api/auth/token/refresh/` | Renovar access token | No |
| POST | `/api/auth/token/verify/` | Verificar token | No |

### Especialidades

| Método | Endpoint | Descripción | Auth requerida |
|---|---|---|---|
| GET | `/api/especialidades/` | Listar | Sí |
| POST | `/api/especialidades/` | Crear | Staff |
| GET | `/api/especialidades/{id}/` | Detalle | Sí |
| PATCH | `/api/especialidades/{id}/` | Actualizar | Staff |
| DELETE | `/api/especialidades/{id}/` | Eliminar | Staff |
| GET | `/api/especialidades/{id}/medicos/` | Médicos de la especialidad | Sí |
| GET | `/api/especialidades/stats/` | Estadísticas | Sí |

### Médicos

| Método | Endpoint | Descripción | Auth requerida |
|---|---|---|---|
| GET | `/api/medicos/` | Listar | Sí |
| POST | `/api/medicos/` | Crear | Staff |
| GET | `/api/medicos/{id}/` | Detalle | Sí |
| PATCH | `/api/medicos/{id}/` | Actualizar | Staff |
| DELETE | `/api/medicos/{id}/` | Eliminar | Staff |
| GET | `/api/medicos/{id}/citas/` | Citas del médico | Sí |
| POST | `/api/medicos/{id}/toggle-active/` | Activar/desactivar | Admin |
| GET | `/api/medicos/stats/` | Estadísticas | Sí |

### Pacientes

| Método | Endpoint | Descripción | Auth requerida |
|---|---|---|---|
| GET | `/api/pacientes/` | Listar | Sí |
| POST | `/api/pacientes/` | Crear | Staff |
| GET | `/api/pacientes/{id}/` | Detalle | Sí |
| PATCH | `/api/pacientes/{id}/` | Actualizar | Staff |
| DELETE | `/api/pacientes/{id}/` | Eliminar | Staff |
| GET | `/api/pacientes/{id}/historial/` | Historial de citas | Sí |
| GET | `/api/pacientes/stats/` | Estadísticas | Sí |

### Horarios

| Método | Endpoint | Descripción | Auth requerida |
|---|---|---|---|
| GET | `/api/horarios/` | Listar | Sí |
| POST | `/api/horarios/` | Crear | Staff |
| GET | `/api/horarios/{id}/` | Detalle | Sí |
| PATCH | `/api/horarios/{id}/` | Actualizar | Staff |
| DELETE | `/api/horarios/{id}/` | Eliminar | Staff |
| GET | `/api/horarios/stats/` | Estadísticas | Sí |

### Citas

| Método | Endpoint | Descripción | Auth requerida |
|---|---|---|---|
| GET | `/api/citas/` | Listar | Sí |
| POST | `/api/citas/` | Crear | Staff |
| GET | `/api/citas/{id}/` | Detalle | Sí |
| PATCH | `/api/citas/{id}/` | Actualizar | Staff |
| DELETE | `/api/citas/{id}/` | Eliminar | Staff |
| POST | `/api/citas/agendar/` | Agendar cita | Staff |
| POST | `/api/citas/{id}/confirmar/` | Confirmar cita | Staff |
| POST | `/api/citas/{id}/cancelar/` | Cancelar cita | Staff |
| POST | `/api/citas/{id}/cambiar-estado/` | Cambiar estado | Staff |
| GET | `/api/citas/stats/` | Estadísticas | Sí |

### Consultas

| Método | Endpoint | Descripción | Auth requerida |
|---|---|---|---|
| GET | `/api/consultas/` | Listar | Sí |
| POST | `/api/consultas/` | Crear | Staff |
| GET | `/api/consultas/{id}/` | Detalle | Sí |
| PATCH | `/api/consultas/{id}/` | Actualizar | Staff |
| DELETE | `/api/consultas/{id}/` | Eliminar | Staff |
| POST | `/api/consultas/{id}/agregar-receta/` | Agregar receta | Staff |
| GET | `/api/consultas/{id}/recetas/` | Listar recetas | Sí |
| GET | `/api/consultas/stats/` | Estadísticas | Admin |

---

## Filtros disponibles

```bash
# Búsqueda por texto
GET /api/pacientes/?search=Juan
GET /api/medicos/?search=García

# Filtros por campo
GET /api/citas/?estado=pendiente
GET /api/citas/?desde=2025-01-01&hasta=2025-12-31
GET /api/medicos/?especialidad=1
GET /api/horarios/?dia_semana=0

# Paginación
GET /api/pacientes/?page=2&page_size=20

# Ordenamiento
GET /api/pacientes/?ordering=-created_at
```

## Permisos

| Rol | Permisos |
|---|---|
| Sin autenticar | Solo `/health/`, `/auth/register/` y `/auth/login/` |
| Usuario autenticado | Lectura (GET) en todos los endpoints |
| Staff (`is_staff=True`) | Lectura y escritura completa |
| Admin (`is_superuser=True`) | Acceso total incluyendo acciones de admin |

## Colección Thunder Client / Postman

Importar el archivo `CONSULTAS-MEDICAS.postman_collection.json` incluido en el repositorio. Contiene 59 endpoints organizados en 8 carpetas.

- **Local:** baseUrl = `http://localhost:8000/api`
- **Producción:** cambiar baseUrl a `https://bacon-consultas.uaeftt-ute.site/api`
