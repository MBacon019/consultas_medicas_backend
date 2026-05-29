# clinic/views/paciente.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from clinic.models              import Paciente
from clinic.serializers.paciente import PacienteSerializer, PacienteSummarySerializer
from clinic.permissions         import IsStaffOrReadOnly
from clinic.filters             import PacienteFilter
from clinic.pagination          import StandardPagination


class PacienteViewSet(viewsets.ModelViewSet):
    queryset           = Paciente.objects.all()
    serializer_class   = PacienteSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = PacienteFilter
    search_fields      = ['nombres', 'apellidos', 'cedula', 'email']
    ordering_fields    = ['apellidos', 'nombres', 'fecha_nac', 'created_at']
    ordering           = ['apellidos']

    @action(detail=True, methods=['get'], url_path='historial')
    def historial(self, request, pk=None):
        from clinic.models import Cita
        from clinic.serializers.cita import CitaSerializer
        paciente = self.get_object()
        qs       = paciente.citas.select_related('medico').order_by('-fecha_hora')
        page     = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(CitaSerializer(page, many=True).data)
        return Response(CitaSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = Paciente.objects.all()
        return Response({
            'total':     qs.count(),
            'activos':   qs.filter(is_active=True).count(),
            'inactivos': qs.filter(is_active=False).count(),
            'por_sexo': list(
                qs.values('sexo')
                  .annotate(total=Count('id'))
                  .order_by('sexo')
            ),
        })
