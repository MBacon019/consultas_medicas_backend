# clinic/serializers/paciente.py
from rest_framework import serializers
from clinic.models import Paciente


class PacienteSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Paciente
        fields = ['id', 'nombres', 'apellidos', 'cedula', 'telefono', 'is_active']


class PacienteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    total_citas     = serializers.SerializerMethodField()

    class Meta:
        model  = Paciente
        fields = [
            'id', 'nombres', 'apellidos', 'nombre_completo',
            'cedula', 'fecha_nac', 'sexo',
            'telefono', 'email', 'direccion',
            'is_active', 'total_citas',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_nombre_completo(self, obj):
        return obj.nombre_completo

    def get_total_citas(self, obj):
        return obj.citas.count()

    def validate_cedula(self, value):
        qs = Paciente.objects.filter(cedula=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Ya existe un paciente con esta cédula.')
        return value
