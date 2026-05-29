# clinic/admin.py
from django.contrib import admin
from clinic.models import Especialidad, Medico, Paciente, Horario, Cita, Consulta, Receta


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display        = ['id', 'nombre', 'slug', 'is_active', 'created_at']
    list_filter         = ['is_active']
    search_fields       = ['nombre']
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'apellidos', 'nombres', 'cedula', 'especialidad', 'is_active']
    list_filter   = ['is_active', 'especialidad']
    search_fields = ['nombres', 'apellidos', 'cedula', 'email']
    list_editable = ['is_active']


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display  = ['id', 'apellidos', 'nombres', 'cedula', 'sexo', 'telefono', 'is_active']
    list_filter   = ['is_active', 'sexo']
    search_fields = ['nombres', 'apellidos', 'cedula', 'email']
    list_editable = ['is_active']


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'medico', 'dia_semana', 'hora_inicio', 'hora_fin', 'is_active']
    list_filter  = ['dia_semana', 'is_active', 'medico']


class RecetaInline(admin.TabularInline):
    model  = Receta
    extra  = 0
    fields = ['medicamento', 'dosis', 'frecuencia', 'duracion']


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display    = ['id', 'cita', 'diagnostico', 'created_at']
    search_fields   = ['diagnostico', 'cita__paciente__apellidos']
    readonly_fields = ['created_at', 'updated_at']
    inlines         = [RecetaInline]


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display    = ['id', 'paciente', 'medico', 'fecha_hora', 'estado', 'registrado_por']
    list_filter     = ['estado']
    search_fields   = ['paciente__apellidos', 'medico__apellidos']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'consulta', 'medicamento', 'dosis', 'frecuencia', 'duracion']
    search_fields = ['medicamento']
