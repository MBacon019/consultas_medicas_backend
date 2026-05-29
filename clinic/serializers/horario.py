# clinic/serializers/horario.py
from rest_framework import serializers
from clinic.models import Horario
from clinic.serializers.medico import MedicoSummarySerializer


class HorarioSerializer(serializers.ModelSerializer):
    medico    = MedicoSummarySerializer(read_only=True)
    medico_id = serializers.PrimaryKeyRelatedField(
        source='medico',
        write_only=True,
        queryset=Horario.objects.none(),
    )
    dia_nombre = serializers.CharField(source='get_dia_semana_display', read_only=True)

    class Meta:
        model  = Horario
        fields = [
            'id', 'medico', 'medico_id', 'dia_semana', 'dia_nombre',
            'hora_inicio', 'hora_fin', 'is_active',
        ]
        read_only_fields = ['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from clinic.models import Medico
        self.fields['medico_id'].queryset = Medico.objects.filter(is_active=True)

    def validate(self, data):
        hora_inicio = data.get('hora_inicio', getattr(self.instance, 'hora_inicio', None))
        hora_fin    = data.get('hora_fin',    getattr(self.instance, 'hora_fin',    None))
        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise serializers.ValidationError(
                'La hora de inicio debe ser anterior a la hora de fin.'
            )
        return data
