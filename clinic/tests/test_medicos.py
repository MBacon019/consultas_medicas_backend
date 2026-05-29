# clinic/tests/test_medicos.py
from django.test import TestCase
from rest_framework import status

from .helpers import create_user, create_staff, auth_client, create_medico, create_especialidad


class MedicoPermissionTests(TestCase):

    def setUp(self):
        self.user   = create_user('usuario1')
        self.staff  = create_staff()
        self.medico = create_medico()

    def test_usuario_autenticado_puede_listar(self):
        resp = auth_client(self.user).get('/api/medicos/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_usuario_regular_no_puede_crear(self):
        esp = create_especialidad('Pediatría', 'pediatria')
        resp = auth_client(self.user).post('/api/medicos/', {
            'nombres': 'Carlos', 'apellidos': 'Ramos',
            'cedula': '1111111111', 'email': 'carlos@med.com',
            'especialidad_id': esp.id,
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_puede_crear_medico(self):
        esp = create_especialidad('Neurología', 'neurologia')
        resp = auth_client(self.staff).post('/api/medicos/', {
            'nombres': 'María', 'apellidos': 'Torres',
            'cedula': '2222222222', 'email': 'maria@med.com',
            'especialidad_id': esp.id,
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('nombre_completo', resp.data)

    def test_cedula_duplicada_retorna_400(self):
        esp = create_especialidad('Pediatría', 'pediatria')
        cedula = self.medico.cedula
        resp = auth_client(self.staff).post('/api/medicos/', {
            'nombres': 'Otro', 'apellidos': 'Medico',
            'cedula': cedula, 'email': 'otro@med.com',
            'especialidad_id': esp.id,
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class MedicoFilterTests(TestCase):

    def setUp(self):
        self.client = auth_client(create_user('filtros'))
        esp1 = create_especialidad('Cardiología', 'cardiologia')
        esp2 = create_especialidad('Pediatría', 'pediatria')
        create_medico('Luis', 'Mendoza', '3333333333', especialidad=esp1)
        create_medico('Ana', 'Vega', '4444444444', especialidad=esp2, is_active=False)

    def test_filtrar_por_activos(self):
        resp = self.client.get('/api/medicos/?is_active=true')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_buscar_por_apellido(self):
        resp = self.client.get('/api/medicos/?search=mendoza')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_stats_retorna_campos_esperados(self):
        resp = self.client.get('/api/medicos/stats/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for field in ['total', 'activos', 'inactivos', 'por_especialidad']:
            self.assertIn(field, resp.data)
