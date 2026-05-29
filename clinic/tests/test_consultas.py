# clinic/tests/test_consultas.py
from django.test import TestCase
from rest_framework import status

from .helpers import (
    create_user, create_staff, auth_client,
    create_cita, create_consulta,
)


class ConsultaTests(TestCase):

    def setUp(self):
        self.user   = create_user('doctor1')
        self.staff  = create_staff()
        self.cita   = create_cita(estado='confirmada')

    def test_staff_puede_crear_consulta(self):
        resp = auth_client(self.staff).post('/api/consultas/', {
            'cita':            self.cita.id,
            'motivo_consulta': 'Dolor abdominal',
            'diagnostico':     'Gastritis aguda',
            'tratamiento':     'Omeprazol 20mg',
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('recetas', resp.data)

    def test_usuario_regular_no_puede_crear(self):
        resp = auth_client(self.user).post('/api/consultas/', {
            'cita':            self.cita.id,
            'motivo_consulta': 'Prueba',
            'diagnostico':     'Prueba',
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_agregar_receta_a_consulta(self):
        consulta = create_consulta(cita=self.cita)
        resp = auth_client(self.staff).post(
            f'/api/consultas/{consulta.id}/agregar-receta/',
            {
                'medicamento': 'Ibuprofeno',
                'dosis':       '400mg',
                'frecuencia':  '8 horas',
                'duracion':    '5 días',
            }
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['medicamento'], 'Ibuprofeno')

    def test_listar_recetas_de_consulta(self):
        consulta = create_consulta(cita=self.cita)
        resp = auth_client(self.user).get(f'/api/consultas/{consulta.id}/recetas/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_cita_duplicada_retorna_400(self):
        create_consulta(cita=self.cita)
        cita2 = create_cita(estado='confirmada')
        # Intentar crear otra consulta para la misma cita
        resp = auth_client(self.staff).post('/api/consultas/', {
            'cita':            self.cita.id,
            'motivo_consulta': 'Revisión',
            'diagnostico':     'Sin novedad',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
