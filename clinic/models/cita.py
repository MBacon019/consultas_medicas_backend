# clinic/models/cita.py
from django.db import models
from django.contrib.auth.models import User
from .medico import Medico
from .paciente import Paciente


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente',   'Pendiente'),
        ('confirmada',  'Confirmada'),
        ('atendida',    'Atendida'),
        ('cancelada',   'Cancelada'),
        ('no_asistio',  'No asistió'),
    ]

    paciente       = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        related_name='citas',
    )
    medico         = models.ForeignKey(
        Medico,
        on_delete=models.PROTECT,
        related_name='citas',
    )
    registrado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='citas_registradas',
    )
    fecha_hora     = models.DateTimeField()
    motivo         = models.CharField(max_length=300, blank=True, default='')
    estado         = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
    )
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Cita'
        verbose_name_plural = 'Citas'
        ordering            = ['-fecha_hora']

    def __str__(self):
        return f'Cita #{self.id} — {self.paciente} con {self.medico} ({self.estado})'
