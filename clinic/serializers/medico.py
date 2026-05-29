# clinic/serializers/medico.py
from rest_framework import serializers
from clinic.models import Medico
from clinic.serializers.especialidad import EspecialidadSerializer


class MedicoSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Medico
        fields = ['id', 'nombres', 'apellidos', 'cedula', 'email', 'is_active']


class MedicoSerializer(serializers.ModelSerializer):
    especialidad    = EspecialidadSerializer(read_only=True)
    especialidad_id = serializers.PrimaryKeyRelatedField(
        source='especialidad',
        write_only=True,
        queryset=Medico.objects.none(),
    )
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model  = Medico
        fields = [
            'id', 'nombres', 'apellidos', 'nombre_completo',
            'cedula', 'telefono', 'email',
            'especialidad', 'especialidad_id',
            'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from clinic.models import Especialidad
        self.fields['especialidad_id'].queryset = Especialidad.objects.filter(is_active=True)

    def get_nombre_completo(self, obj):
        return obj.nombre_completo

    def validate_cedula(self, value):
        qs = Medico.objects.filter(cedula=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Ya existe un médico con esta cédula.')
        return value
