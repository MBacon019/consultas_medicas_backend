import uuid
import random
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from clinic.models import Especialidad, Medico, Paciente, Horario, Cita, Consulta, Receta


def create_user(username='usuario', email=None, password='Pass1234!', **kwargs):
    # Evita duplicados de username
    if username == 'usuario':
        username = f"usuario_{uuid.uuid4().hex[:6]}"
    email = email or f'{username}@test.com'
    return User.objects.create_user(
        username=username, email=email, password=password, **kwargs
    )


def create_staff(username='staff', email=None, password='Admin1234!'):
    # Evita duplicados de username para staff
    if username == 'staff':
        username = f"staff_{uuid.uuid4().hex[:6]}"
    email = email or f'{username}@test.com'
    return User.objects.create_user(
        username=username, email=email, password=password, is_staff=True
    )


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)


def auth_client(user):
    client = APIClient()
    access, _ = get_tokens(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    return client


def create_especialidad(nombre=None, slug=None, is_active=True):
    # Genera nombres y slugs únicos para que no choque el campo unique
    unique_id = uuid.uuid4().hex[:6]
    nombre = nombre or f'Especialidad {unique_id}'
    slug = slug or f'especialidad-{unique_id}'
    return Especialidad.objects.create(nombre=nombre, slug=slug, is_active=is_active)


def create_medico(nombres='Juan', apellidos='Pérez', cedula=None,
                  especialidad=None, is_active=True):
    # Genera cédulas aleatorias de 10 dígitos para evitar el UniqueViolation
    if cedula is None:
        cedula = "".join([str(random.randint(0, 9)) for _ in range(10)])
    if especialidad is None:
        especialidad = create_especialidad()
    return Medico.objects.create(
        nombres=nombres,
        apellidos=apellidos,
        cedula=cedula,
        email=f'{cedula}@medico.com',
        especialidad=especialidad,
        is_active=is_active,
    )


def create_paciente(nombres='Ana', apellidos='García', cedula=None,
                    sexo='F', is_active=True):
    # Genera cédulas aleatorias de 10 dígitos para los pacientes de prueba
    if cedula is None:
        cedula = "".join([str(random.randint(0, 9)) for _ in range(10)])
    return Paciente.objects.create(
        nombres=nombres,
        apellidos=apellidos,
        cedula=cedula,
        fecha_nac='1990-05-15',
        sexo=sexo,
        email=f'{cedula}@paciente.com',
        is_active=is_active,
    )


def create_cita(paciente=None, medico=None, user=None, estado='pendiente'):
    from django.utils import timezone
    from datetime import timedelta
    if paciente is None:
        paciente = create_paciente()
    if medico is None:
        medico = create_medico()
    if user is None:
        user = create_user()
    return Cita.objects.create(
        paciente=paciente,
        medico=medico,
        registrado_por=user,
        fecha_hora=timezone.now() + timedelta(days=1),
        estado=estado,
    )


def create_consulta(cita=None):
    if cita is None:
        cita = create_cita(estado='confirmada')
    return Consulta.objects.create(
        cita=cita,
        motivo_consulta='Dolor de cabeza',
        diagnostico='Migraña tensional',
        tratamiento='Reposo y analgésicos',
    )