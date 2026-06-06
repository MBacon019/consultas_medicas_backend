# clinic/models/receta.py
from django.db import models
from .consulta import Consulta


class Receta(models.Model):
    consulta    = models.ForeignKey(
        Consulta,
        on_delete=models.CASCADE,
        related_name='recetas',
    )
    medicamento = models.CharField(max_length=200)
    dosis       = models.CharField(max_length=100)
    frecuencia  = models.CharField(max_length=100)
    duracion    = models.CharField(max_length=100)
    indicaciones = models.TextField(blank=True, default='')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Receta'
        verbose_name_plural = 'Recetas'
        ordering            = ['medicamento']

    def __str__(self):
        return f'{self.medicamento} — {self.dosis} ({self.frecuencia})'

    @property
    def resumen(self):
        return f'{self.medicamento} {self.dosis} cada {self.frecuencia} por {self.duracion}'
