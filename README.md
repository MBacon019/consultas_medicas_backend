# 🏥 ConsultasAPI — Backend

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST-ff1709?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Digital Ocean](https://img.shields.io/badge/Digital_Ocean-0080FF?style=for-the-badge&logo=digitalocean&logoColor=white)

**API REST para gestión de consultas médicas**

Django + DRF · PostgreSQL · JWT · Desplegada en Digital Ocean

**👨‍💻 Desarrollado por:** Bacon Marcelo

[🔗 API en Producción](https://bacon-consultas.uaeftt-ute.site/api/) · [📱 App Android](https://github.com/MBacon019/bacon_app_consultas_medicas) · [📬 Colección Postman](https://github.com/MBacon019/consultas_medicas_backend/blob/master/CONSULTAS-MEDICAS.postman_collection.json)

</div>

---

## 📋 Stack Tecnológico

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.12 |
| Framework | Django 6+ |
| API | Django REST Framework |
| Autenticación | Simple JWT |
| Base de datos | PostgreSQL |
| Filtros | django-filter |
| Servidor | Gunicorn + Nginx |
| Despliegue | Digital Ocean + CI/CD GitHub Actions |

---

## 🌐 URL en Producción

```
https://bacon-consultas.uaeftt-ute.site/api/
```

---

## 🗄️ Las 7 Tablas de Base de Datos

| Modelo | Descripción |
|---|---|
| `Especialidad` | Especialidades médicas (Cardiología, Pediatría, etc.) |
| `Medico` | Médicos con su especialidad asignada |
| `Paciente` | Datos personales de los pacientes |
| `Horario` | Horarios de atención de cada médico |
| `Cita` | Citas agendadas (paciente + médico + fecha/hora) |
| `Consulta` | Registro clínico de cada cita atendida |
| `Receta` | Medicamentos recetados por consulta |

---

## ⚙️ Configuración local

```bash
# 1. Clonar el repositorio
git clone https://github.com/MBacon019/consultas_medicas_backend.git
cd consultas_medicas_backend

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de base de datos

# 3. Instalar dependencias y migrar
uv run manage.py migrate
uv run manage.py createsuperuser
uv run manage.py runserver
```

---

## 🧪 Tests

```bash
uv run manage.py test clinic
```

---

## 🔐 Autenticación JWT

Todos los endpoints excepto `/health/`, `/auth/register/` y `/auth/login/` requieren el header `Authorization`.

### 1. Obtener token (login)

```bash
curl -X POST https://bacon-consultas.uaeftt-ute.site/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin1234!"}'
```

```json
{
  "access": "eyJ...",
  "refresh": "eyJ...",
  "user_id": 1,
  "username": "admin",
  "is_staff": true
}
```

### 2. Usar el token

```bash
curl -X GET https://bacon-consultas.uaeftt-ute.site/api/pacientes/ \
  -H "Authorization: Bearer eyJ..."
```

### 3. Renovar token expirado

```bash
curl -X POST https://bacon-consultas.uaeftt-ute.site/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "eyJ..."}'
```

### 4. Cerrar sesión

```bash
curl -X POST https://bacon-consultas.uaeftt-ute.site/api/auth/logout/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

---

## 📡 Endpoints Principales

```
GET  /api/health/

POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
POST /api/auth/token/refresh/

GET/POST   /api/especialidades/
GET/POST   /api/medicos/
GET/POST   /api/pacientes/
GET/POST   /api/horarios/
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
```

---

## 📋 Listado Completo de Endpoints

### 🔑 Autenticación

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| POST | `/api/auth/register/` | Registrar nuevo usuario | ❌ |
| POST | `/api/auth/login/` | Obtener token JWT | ❌ |
| POST | `/api/auth/logout/` | Invalidar token | ✅ |
| POST | `/api/auth/token/refresh/` | Renovar access token | ❌ |
| POST | `/api/auth/token/verify/` | Verificar token | ❌ |

### 🏷️ Especialidades

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| GET | `/api/especialidades/` | Listar | ✅ |
| POST | `/api/especialidades/` | Crear | 👮 Staff |
| GET | `/api/especialidades/{id}/` | Detalle | ✅ |
| PATCH | `/api/especialidades/{id}/` | Actualizar | 👮 Staff |
| DELETE | `/api/especialidades/{id}/` | Eliminar | 👮 Staff |
| GET | `/api/especialidades/{id}/medicos/` | Médicos de la especialidad | ✅ |
| GET | `/api/especialidades/stats/` | Estadísticas | ✅ |

### 👨‍⚕️ Médicos

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| GET | `/api/medicos/` | Listar | ✅ |
| POST | `/api/medicos/` | Crear | 👮 Staff |
| GET | `/api/medicos/{id}/` | Detalle | ✅ |
| PATCH | `/api/medicos/{id}/` | Actualizar | 👮 Staff |
| DELETE | `/api/medicos/{id}/` | Eliminar | 👮 Staff |
| GET | `/api/medicos/{id}/citas/` | Citas del médico | ✅ |
| POST | `/api/medicos/{id}/toggle-active/` | Activar/desactivar | 👑 Admin |
| GET | `/api/medicos/stats/` | Estadísticas | ✅ |

### 🧑‍🤝‍🧑 Pacientes

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| GET | `/api/pacientes/` | Listar | ✅ |
| POST | `/api/pacientes/` | Crear | 👮 Staff |
| GET | `/api/pacientes/{id}/` | Detalle | ✅ |
| PATCH | `/api/pacientes/{id}/` | Actualizar | 👮 Staff |
| DELETE | `/api/pacientes/{id}/` | Eliminar | 👮 Staff |
| GET | `/api/pacientes/{id}/historial/` | Historial de citas | ✅ |
| GET | `/api/pacientes/stats/` | Estadísticas | ✅ |

### 🕐 Horarios

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| GET | `/api/horarios/` | Listar | ✅ |
| POST | `/api/horarios/` | Crear | 👮 Staff |
| GET | `/api/horarios/{id}/` | Detalle | ✅ |
| PATCH | `/api/horarios/{id}/` | Actualizar | 👮 Staff |
| DELETE | `/api/horarios/{id}/` | Eliminar | 👮 Staff |

### 📅 Citas

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| GET | `/api/citas/` | Listar | ✅ |
| POST | `/api/citas/agendar/` | Agendar cita | ✅ |
| GET | `/api/citas/{id}/` | Detalle | ✅ |
| PATCH | `/api/citas/{id}/` | Actualizar | 👮 Staff |
| DELETE | `/api/citas/{id}/` | Eliminar | 👮 Staff |
| POST | `/api/citas/{id}/confirmar/` | Confirmar | 👮 Staff |
| POST | `/api/citas/{id}/cancelar/` | Cancelar | ✅ |
| POST | `/api/citas/{id}/cambiar-estado/` | Cambiar estado | 👮 Staff |
| GET | `/api/citas/stats/` | Estadísticas | ✅ |

### 🩺 Consultas

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| GET | `/api/consultas/` | Listar | ✅ |
| POST | `/api/consultas/` | Crear | 👮 Staff |
| GET | `/api/consultas/{id}/` | Detalle | ✅ |
| PATCH | `/api/consultas/{id}/` | Actualizar | 👮 Staff |
| DELETE | `/api/consultas/{id}/` | Eliminar | 👮 Staff |
| POST | `/api/consultas/{id}/agregar-receta/` | Agregar receta | 👮 Staff |
| GET | `/api/consultas/{id}/recetas/` | Listar recetas | ✅ |
| GET | `/api/consultas/stats/` | Estadísticas | 👑 Admin |

---

## 🔍 Filtros Disponibles

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

---

## 🛡️ Permisos

| Rol | Permisos |
|---|---|
| ❌ Sin autenticar | Solo `/health/`, `/auth/register/` y `/auth/login/` |
| ✅ Autenticado | Lectura (GET) en todos los endpoints |
| 👮 Staff (`is_staff=True`) | Lectura y escritura completa |
| 👑 Admin (`is_superuser=True`) | Acceso total |

---

## 📬 Colección Postman

Importa el archivo [`CONSULTAS-MEDICAS.postman_collection.json`](https://github.com/MBacon019/consultas_medicas_backend/blob/master/CONSULTAS-MEDICAS.postman_collection.json) incluido en el repositorio.

Contiene **59 endpoints** organizados en 8 carpetas.

| Entorno | Base URL |
|---|---|
| Local | `http://localhost:8000/api` |
| Producción | `https://bacon-consultas.uaeftt-ute.site/api` |

---

## 🔗 Links del Proyecto

| Recurso | URL |
|---|---|
| 🔧 API Producción | [https://bacon-consultas.uaeftt-ute.site/api/](https://bacon-consultas.uaeftt-ute.site/api/) |
| 📱 App Android | [github.com/MBacon019/bacon_app_consultas_medicas](https://github.com/MBacon019/bacon_app_consultas_medicas) |
| 📬 Colección Postman | [CONSULTAS-MEDICAS.postman_collection.json](https://github.com/MBacon019/consultas_medicas_backend/blob/master/CONSULTAS-MEDICAS.postman_collection.json) |