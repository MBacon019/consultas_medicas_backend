# clinic/serializers/especialidad.py
from rest_framework import serializers
from django.utils.text import slugify
from clinic.models import Especialidad


class EspecialidadSerializer(serializers.ModelSerializer):
    total_medicos = serializers.SerializerMethodField()

    class Meta:
        model  = Especialidad
        fields = [
            'id', 'nombre', 'slug', 'descripcion',
            'is_active', 'total_medicos', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_total_medicos(self, obj):
        return obj.medicos.filter(is_active=True).count()

    def validate_slug(self, value):
        return slugify(value)

    def validate_nombre(self, value):
        qs = Especialidad.objects.filter(nombre__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Ya existe una especialidad con este nombre.')
        return value
