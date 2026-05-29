# clinic/models/paciente.py
from django.db import models


class Paciente(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    nombres        = models.CharField(max_length=150)
    apellidos      = models.CharField(max_length=150)
    cedula         = models.CharField(max_length=20, unique=True)
    fecha_nac      = models.DateField()
    sexo           = models.CharField(max_length=1, choices=SEXO_CHOICES)
    telefono       = models.CharField(max_length=20, blank=True, default='')
    email          = models.EmailField(blank=True, default='')
    direccion      = models.TextField(blank=True, default='')
    is_active      = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering            = ['apellidos', 'nombres']

    def __str__(self):
        return f'{self.apellidos} {self.nombres}'

    @property
    def nombre_completo(self):
        return f'{self.nombres} {self.apellidos}'
