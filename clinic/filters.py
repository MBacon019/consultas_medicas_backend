# clinic/filters.py
import django_filters
from clinic.models import Especialidad, Medico, Paciente, Horario, Cita, Consulta


class HorarioFilter(django_filters.FilterSet):
    medico_id = django_filters.NumberFilter(field_name='medico')

    class Meta:
        model  = Horario
        fields = ['medico_id', 'dia_semana', 'is_active']


class EspecialidadFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model  = Especialidad
        fields = ['is_active']


class MedicoFilter(django_filters.FilterSet):
    nombres      = django_filters.CharFilter(lookup_expr='icontains')
    apellidos    = django_filters.CharFilter(lookup_expr='icontains')
    especialidad_nombre = django_filters.CharFilter(
        field_name='especialidad__nombre', lookup_expr='icontains'
    )

    class Meta:
        model  = Medico
        fields = ['is_active', 'especialidad']


class PacienteFilter(django_filters.FilterSet):
    nombres   = django_filters.CharFilter(lookup_expr='icontains')
    apellidos = django_filters.CharFilter(lookup_expr='icontains')
    edad_min  = django_filters.NumberFilter(field_name='fecha_nac', lookup_expr='year__lte')
    edad_max  = django_filters.NumberFilter(field_name='fecha_nac', lookup_expr='year__gte')

    class Meta:
        model  = Paciente
        fields = ['is_active', 'sexo']


class CitaFilter(django_filters.FilterSet):
    desde     = django_filters.DateFilter(field_name='fecha_hora', lookup_expr='date__gte')
    hasta     = django_filters.DateFilter(field_name='fecha_hora', lookup_expr='date__lte')
    medico_id = django_filters.NumberFilter(field_name='medico')
    paciente_id = django_filters.NumberFilter(field_name='paciente')

    class Meta:
        model  = Cita
        fields = ['estado']


class ConsultaFilter(django_filters.FilterSet):
    desde    = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    hasta    = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')
    medico_id = django_filters.NumberFilter(field_name='cita__medico')
    paciente_id = django_filters.NumberFilter(field_name='cita__paciente')

    class Meta:
        model  = Consulta
        fields = []
