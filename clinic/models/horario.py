# clinic/models/horario.py
from django.db import models
from .medico import Medico


class Horario(models.Model):
    DIA_CHOICES = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    medico      = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name='horarios',
    )
    dia_semana  = models.IntegerField(choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin    = models.TimeField()
    is_active   = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Horario'
        verbose_name_plural = 'Horarios'
        ordering            = ['dia_semana', 'hora_inicio']
        unique_together     = [('medico', 'dia_semana', 'hora_inicio')]

    def __str__(self):
        return f'{self.medico} — {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}'
