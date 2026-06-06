# clinic/views/horario.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from clinic.models               import Horario
from clinic.serializers.horario  import HorarioSerializer
from clinic.permissions          import IsStaffOrReadOnly
from clinic.filters              import HorarioFilter
from clinic.pagination           import StandardPagination


class HorarioViewSet(viewsets.ModelViewSet):
    queryset           = Horario.objects.select_related('medico', 'medico__especialidad').all()
    serializer_class   = HorarioSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = HorarioFilter
    search_fields      = ['medico__nombres', 'medico__apellidos']
    ordering_fields    = ['dia_semana', 'hora_inicio', 'medico__apellidos']
    ordering           = ['dia_semana', 'hora_inicio']

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = Horario.objects.all()
        return Response({
            'total':    qs.count(),
            'activos':  qs.filter(is_active=True).count(),
            'inactivos': qs.filter(is_active=False).count(),
        })
