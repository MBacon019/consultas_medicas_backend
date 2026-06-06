# clinic/serializers/consulta.py
from rest_framework import serializers
from clinic.models import Consulta, Receta


class RecetaSerializer(serializers.ModelSerializer):
    resumen = serializers.SerializerMethodField()

    class Meta:
        model  = Receta
        fields = [
            'id', 'medicamento', 'dosis', 'frecuencia',
            'duracion', 'indicaciones', 'resumen', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_resumen(self, obj):
        return obj.resumen


class ConsultaSerializer(serializers.ModelSerializer):
    recetas      = RecetaSerializer(many=True, read_only=True)
    num_recetas  = serializers.SerializerMethodField()
    cita_info    = serializers.SerializerMethodField()

    class Meta:
        model  = Consulta
        fields = [
            'id', 'cita', 'cita_info',
            'motivo_consulta', 'anamnesis', 'examen_fisico',
            'diagnostico', 'tratamiento', 'observaciones',
            'num_recetas', 'recetas',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_num_recetas(self, obj):
        return obj.recetas.count()

    def get_cita_info(self, obj):
        return {
            'id':        obj.cita.id,
            'paciente':  str(obj.cita.paciente),
            'medico':    str(obj.cita.medico),
            'fecha_hora': obj.cita.fecha_hora,
            'estado':    obj.cita.estado,
        }

    def validate_cita(self, value):
        if hasattr(value, 'consulta') and (self.instance is None or self.instance.cita != value):
            raise serializers.ValidationError('Esta cita ya tiene una consulta registrada.')
        if value.estado not in ['confirmada', 'atendida']:
            raise serializers.ValidationError(
                'Solo se puede registrar consulta para citas confirmadas o atendidas.'
            )
        return value


class AgregarRecetaSerializer(serializers.Serializer):
    medicamento  = serializers.CharField(max_length=200)
    dosis        = serializers.CharField(max_length=100)
    frecuencia   = serializers.CharField(max_length=100)
    duracion     = serializers.CharField(max_length=100)
    indicaciones = serializers.CharField(required=False, default='')
