# clinic/models/medico.py
from django.db import models
from .especialidad import Especialidad


class Medico(models.Model):
    nombres       = models.CharField(max_length=150)
    apellidos     = models.CharField(max_length=150)
    cedula        = models.CharField(max_length=20, unique=True)
    telefono      = models.CharField(max_length=20, blank=True, default='')
    email         = models.EmailField(unique=True)
    especialidad  = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
        related_name='medicos',
    )
    is_active     = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Médico'
        verbose_name_plural = 'Médicos'
        ordering            = ['apellidos', 'nombres']

    def __str__(self):
        return f'Dr(a). {self.apellidos} {self.nombres}'

    @property
    def nombre_completo(self):
        return f'{self.nombres} {self.apellidos}'
