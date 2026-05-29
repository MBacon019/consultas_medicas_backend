# Generated migration for consultasapi

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('descripcion', models.TextField(blank=True, default='')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Especialidad',
                'verbose_name_plural': 'Especialidades',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=150)),
                ('apellidos', models.CharField(max_length=150)),
                ('cedula', models.CharField(max_length=20, unique=True)),
                ('telefono', models.CharField(blank=True, default='', max_length=20)),
                ('email', models.EmailField(unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('especialidad', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='medicos',
                    to='clinic.especialidad',
                )),
            ],
            options={
                'verbose_name': 'Médico',
                'verbose_name_plural': 'Médicos',
                'ordering': ['apellidos', 'nombres'],
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=150)),
                ('apellidos', models.CharField(max_length=150)),
                ('cedula', models.CharField(max_length=20, unique=True)),
                ('fecha_nac', models.DateField()),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], max_length=1)),
                ('telefono', models.CharField(blank=True, default='', max_length=20)),
                ('email', models.EmailField(blank=True, default='')),
                ('direccion', models.TextField(blank=True, default='')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Paciente',
                'verbose_name_plural': 'Pacientes',
                'ordering': ['apellidos', 'nombres'],
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.IntegerField(choices=[
                    (0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'),
                    (3, 'Jueves'), (4, 'Viernes'), (5, 'Sábado'), (6, 'Domingo'),
                ])),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('medico', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='horarios',
                    to='clinic.medico',
                )),
            ],
            options={
                'verbose_name': 'Horario',
                'verbose_name_plural': 'Horarios',
                'ordering': ['dia_semana', 'hora_inicio'],
                'unique_together': {('medico', 'dia_semana', 'hora_inicio')},
            },
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField()),
                ('motivo', models.CharField(blank=True, default='', max_length=300)),
                ('estado', models.CharField(
                    choices=[
                        ('pendiente', 'Pendiente'),
                        ('confirmada', 'Confirmada'),
                        ('atendida', 'Atendida'),
                        ('cancelada', 'Cancelada'),
                        ('no_asistio', 'No asistió'),
                    ],
                    default='pendiente',
                    max_length=20,
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('paciente', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='citas',
                    to='clinic.paciente',
                )),
                ('medico', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='citas',
                    to='clinic.medico',
                )),
                ('registrado_por', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='citas_registradas',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'Cita',
                'verbose_name_plural': 'Citas',
                'ordering': ['-fecha_hora'],
            },
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo_consulta', models.TextField()),
                ('anamnesis', models.TextField(blank=True, default='')),
                ('examen_fisico', models.TextField(blank=True, default='')),
                ('diagnostico', models.TextField()),
                ('tratamiento', models.TextField(blank=True, default='')),
                ('observaciones', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cita', models.OneToOneField(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='consulta',
                    to='clinic.cita',
                )),
            ],
            options={
                'verbose_name': 'Consulta',
                'verbose_name_plural': 'Consultas',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicamento', models.CharField(max_length=200)),
                ('dosis', models.CharField(max_length=100)),
                ('frecuencia', models.CharField(max_length=100)),
                ('duracion', models.CharField(max_length=100)),
                ('indicaciones', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('consulta', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='recetas',
                    to='clinic.consulta',
                )),
            ],
            options={
                'verbose_name': 'Receta',
                'verbose_name_plural': 'Recetas',
                'ordering': ['medicamento'],
            },
        ),
    ]
