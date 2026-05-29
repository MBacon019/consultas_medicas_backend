# clinic/views/medico.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from clinic.models              import Medico
from clinic.serializers.medico  import MedicoSerializer, MedicoSummarySerializer
from clinic.permissions         import IsStaffOrReadOnly
from clinic.filters             import MedicoFilter
from clinic.pagination          import StandardPagination


class MedicoViewSet(viewsets.ModelViewSet):
    queryset           = Medico.objects.select_related('especialidad').all()
    serializer_class   = MedicoSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = MedicoFilter
    search_fields      = ['nombres', 'apellidos', 'cedula', 'email', 'especialidad__nombre']
    ordering_fields    = ['apellidos', 'nombres', 'created_at']
    ordering           = ['apellidos']

    @action(detail=True, methods=['get'], url_path='citas')
    def citas_medico(self, request, pk=None):
        from clinic.models import Cita
        from clinic.serializers.cita import CitaSerializer
        medico = self.get_object()
        qs     = medico.citas.select_related('paciente').order_by('-fecha_hora')
        estado = request.query_params.get('estado')
        if estado:
            qs = qs.filter(estado=estado)
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(CitaSerializer(page, many=True).data)
        return Response(CitaSerializer(qs, many=True).data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdminUser],
        url_path='toggle-active',
    )
    def toggle_active(self, request, pk=None):
        medico = self.get_object()
        medico.is_active = not medico.is_active
        medico.save(update_fields=['is_active'])
        estado = 'activado' if medico.is_active else 'desactivado'
        return Response({'message': f'Médico {estado}.', 'is_active': medico.is_active})

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = Medico.objects.all()
        return Response({
            'total':     qs.count(),
            'activos':   qs.filter(is_active=True).count(),
            'inactivos': qs.filter(is_active=False).count(),
            'por_especialidad': list(
                qs.values('especialidad__nombre')
                  .annotate(total=Count('id'))
                  .order_by('-total')
            ),
        })
