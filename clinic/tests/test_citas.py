# clinic/tests/test_citas.py
from django.test import TestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from .helpers import (
    create_user, create_staff, auth_client,
    create_cita, create_medico, create_paciente,
)


class CitaPermissionTests(TestCase):

    def setUp(self):
        self.user   = create_user('recepcion')
        self.staff  = create_staff()
        self.cita   = create_cita(user=self.user)

    def test_usuario_autenticado_puede_listar(self):
        resp = auth_client(self.user).get('/api/citas/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_no_autenticado_retorna_401(self):
        from rest_framework.test import APIClient
        resp = APIClient().get('/api/citas/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class CitaWorkflowTests(TestCase):

    def setUp(self):
        self.user    = create_user('recepcion2')
        self.staff   = create_staff()
        self.medico  = create_medico()
        self.paciente = create_paciente()

    def test_agendar_cita(self):
        fecha = (timezone.now() + timedelta(days=2)).isoformat()
        resp = auth_client(self.user).post('/api/citas/agendar/', {
            'paciente_id': self.paciente.id,
            'medico_id':   self.medico.id,
            'fecha_hora':  fecha,
            'motivo':      'Chequeo general',
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['estado'], 'pendiente')

    def test_confirmar_cita_pendiente(self):
        cita = create_cita(paciente=self.paciente, medico=self.medico, user=self.user)
        resp = auth_client(self.user).post(f'/api/citas/{cita.id}/confirmar/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['estado'], 'confirmada')

    def test_cancelar_cita(self):
        cita = create_cita(paciente=self.paciente, medico=self.medico, user=self.user)
        resp = auth_client(self.user).post(f'/api/citas/{cita.id}/cancelar/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['estado'], 'cancelada')

    def test_confirmar_cita_ya_cancelada_retorna_400(self):
        cita = create_cita(
            paciente=self.paciente, medico=self.medico,
            user=self.user, estado='cancelada',
        )
        resp = auth_client(self.user).post(f'/api/citas/{cita.id}/confirmar/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_stats_requiere_admin(self):
        resp = auth_client(self.user).get('/api/citas/stats/')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_stats_accesible_para_staff(self):
        resp = auth_client(self.staff).get('/api/citas/stats/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('total_citas', resp.data)
        self.assertIn('por_estado', resp.data)
