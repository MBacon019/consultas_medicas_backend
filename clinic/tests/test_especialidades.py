# clinic/tests/test_especialidades.py
from django.test import TestCase
from rest_framework import status

from .helpers import create_user, create_staff, auth_client, create_especialidad


class EspecialidadPermissionTests(TestCase):

    def setUp(self):
        self.user          = create_user('eve')
        self.staff         = create_staff()
        self.especialidad  = create_especialidad()

    def test_usuario_autenticado_puede_listar(self):
        resp = auth_client(self.user).get('/api/especialidades/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_no_autenticado_retorna_401(self):
        from rest_framework.test import APIClient
        resp = APIClient().get('/api/especialidades/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_usuario_regular_no_puede_crear(self):
        resp = auth_client(self.user).post('/api/especialidades/', {
            'nombre': 'Pediatría', 'slug': 'pediatria'
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_puede_crear(self):
        resp = auth_client(self.staff).post('/api/especialidades/', {
            'nombre': 'Neurología', 'slug': 'neurologia', 'is_active': True
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_staff_puede_eliminar(self):
        resp = auth_client(self.staff).delete(f'/api/especialidades/{self.especialidad.id}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)


class EspecialidadFilterTests(TestCase):

    def setUp(self):
        self.client = auth_client(create_user('filtros'))
        create_especialidad('Cardiología',  'cardiologia',  is_active=True)
        create_especialidad('Dermatología', 'dermatologia', is_active=False)

    def test_filtrar_por_activas(self):
        resp = self.client.get('/api/especialidades/?is_active=true')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)
        self.assertEqual(resp.data['results'][0]['nombre'], 'Cardiología')

    def test_buscar_por_nombre(self):
        resp = self.client.get('/api/especialidades/?search=cardio')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_stats_retorna_campos_esperados(self):
        resp = self.client.get('/api/especialidades/stats/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for field in ['total', 'activas', 'inactivas', 'detalle']:
            self.assertIn(field, resp.data)
