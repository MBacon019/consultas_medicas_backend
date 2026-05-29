# ConsultasAPI

API REST para gestión de consultas médicas, construida con Django + Django REST Framework.

## Stack

- Python 3.12
- Django 6+
- Django REST Framework
- Simple JWT (autenticación)
- PostgreSQL
- django-filter

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

server {
    listen 80;
    server_name bacon-consultas.uaeftt-ute.site;

    # Logs
    access_log /var/log/nginx/bacon_consultas-access.log;
    error_log  /var/log/nginx/bacon_consultas-error.log;

    # Archivos estáticos (incluye CSS del admin de Django)
    location /static/ {
        alias /opt/shopapi/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Peticiones a la API via Gunicorn
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn-bacon_consultas.sock;
        proxy_read_timeout 90;
        proxy_connect_timeout 90;
    }
}