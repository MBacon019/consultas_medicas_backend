# clinic/models/consulta.py
from django.db import models
from .cita import Cita


class Consulta(models.Model):
    cita            = models.OneToOneField(
        Cita,
        on_delete=models.PROTECT,
        related_name='consulta',
    )
    motivo_consulta = models.TextField()
    anamnesis       = models.TextField(blank=True, default='')
    examen_fisico   = models.TextField(blank=True, default='')
    diagnostico     = models.TextField()
    tratamiento     = models.TextField(blank=True, default='')
    observaciones   = models.TextField(blank=True, default='')
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering            = ['-created_at']

    def __str__(self):
        return f'Consulta #{self.id} — Cita #{self.cita_id}'
