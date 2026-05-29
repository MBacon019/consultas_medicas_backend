# clinic/serializers/cita.py
from rest_framework import serializers
from clinic.models import Cita, Paciente, Medico
from clinic.serializers.paciente import PacienteSummarySerializer
from clinic.serializers.medico   import MedicoSummarySerializer


class CitaSerializer(serializers.ModelSerializer):
    paciente       = PacienteSummarySerializer(read_only=True)
    paciente_id    = serializers.PrimaryKeyRelatedField(
        source='paciente',
        write_only=True,
        queryset=Paciente.objects.none(),
    )
    medico         = MedicoSummarySerializer(read_only=True)
    medico_id      = serializers.PrimaryKeyRelatedField(
        source='medico',
        write_only=True,
        queryset=Medico.objects.none(),
    )
    registrado_por_username = serializers.CharField(
        source='registrado_por.username', read_only=True
    )
    tiene_consulta = serializers.SerializerMethodField()

    class Meta:
        model  = Cita
        fields = [
            'id', 'paciente', 'paciente_id',
            'medico', 'medico_id',
            'registrado_por_username',
            'fecha_hora', 'motivo', 'estado',
            'tiene_consulta',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente_id'].queryset = Paciente.objects.filter(is_active=True)
        self.fields['medico_id'].queryset   = Medico.objects.filter(is_active=True)

    def get_tiene_consulta(self, obj):
        return hasattr(obj, 'consulta')


class AgendarCitaSerializer(serializers.Serializer):
    paciente_id = serializers.IntegerField()
    medico_id   = serializers.IntegerField()
    fecha_hora  = serializers.DateTimeField()
    motivo      = serializers.CharField(max_length=300, required=False, default='')

    def validate_paciente_id(self, value):
        try:
            Paciente.objects.get(pk=value, is_active=True)
        except Paciente.DoesNotExist:
            raise serializers.ValidationError(f'Paciente {value} no encontrado o inactivo.')
        return value

    def validate_medico_id(self, value):
        try:
            Medico.objects.get(pk=value, is_active=True)
        except Medico.DoesNotExist:
            raise serializers.ValidationError(f'Médico {value} no encontrado o inactivo.')
        return value

    def validate(self, data):
        from django.utils import timezone
        if data['fecha_hora'] < timezone.now():
            raise serializers.ValidationError(
                {'fecha_hora': 'La fecha de la cita no puede estar en el pasado.'}
            )
        conflicto = Cita.objects.filter(
            medico_id=data['medico_id'],
            fecha_hora=data['fecha_hora'],
            estado__in=['pendiente', 'confirmada'],
        ).exists()
        if conflicto:
            raise serializers.ValidationError(
                {'fecha_hora': 'El médico ya tiene una cita en esa fecha y hora.'}
            )
        return data
