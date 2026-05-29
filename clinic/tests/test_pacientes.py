# clinic/tests/test_pacientes.py
from django.test import TestCase
from rest_framework import status

from .helpers import create_user, create_staff, auth_client, create_paciente


class PacientePermissionTests(TestCase):

    def setUp(self):
        self.user     = create_user('recep')
        self.staff    = create_staff()
        self.paciente = create_paciente()

    def test_usuario_autenticado_puede_listar(self):
        resp = auth_client(self.user).get('/api/pacientes/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_usuario_regular_no_puede_crear(self):
        resp = auth_client(self.user).post('/api/pacientes/', {
            'nombres': 'Pedro', 'apellidos': 'Loza',
            'cedula': '5555555555', 'fecha_nac': '1985-03-10', 'sexo': 'M',
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_puede_crear_paciente(self):
        resp = auth_client(self.staff).post('/api/pacientes/', {
            'nombres': 'Sofía', 'apellidos': 'Ruiz',
            'cedula': '6666666666', 'fecha_nac': '1992-07-20', 'sexo': 'F',
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('nombre_completo', resp.data)

    def test_cedula_duplicada_retorna_400(self):
        resp = auth_client(self.staff).post('/api/pacientes/', {
            'nombres': 'Otro', 'apellidos': 'Paciente',
            'cedula': self.paciente.cedula,
            'fecha_nac': '2000-01-01', 'sexo': 'M',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class PacienteFilterTests(TestCase):

    def setUp(self):
        self.client = auth_client(create_user('filtros2'))
        create_paciente('Luis', 'Mora', '7777777777', sexo='M')
        create_paciente('Rosa', 'Pino', '8888888888', sexo='F', is_active=False)

    def test_filtrar_por_activos(self):
        resp = self.client.get('/api/pacientes/?is_active=true')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_filtrar_por_sexo(self):
        resp = self.client.get('/api/pacientes/?sexo=M')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_buscar_por_nombre(self):
        resp = self.client.get('/api/pacientes/?search=mora')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_stats_retorna_campos_esperados(self):
        resp = self.client.get('/api/pacientes/stats/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for field in ['total', 'activos', 'inactivos', 'por_sexo']:
            self.assertIn(field, resp.data)
