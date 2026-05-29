# clinic/views/especialidad.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from clinic.models                    import Especialidad
from clinic.serializers.especialidad  import EspecialidadSerializer
from clinic.permissions               import IsStaffOrReadOnly
from clinic.filters                   import EspecialidadFilter
from clinic.pagination                import StandardPagination


class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset           = Especialidad.objects.all()
    serializer_class   = EspecialidadSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = EspecialidadFilter
    search_fields      = ['nombre', 'descripcion']
    ordering_fields    = ['nombre', 'created_at']
    ordering           = ['nombre']

    @action(detail=True, methods=['get'], url_path='medicos')
    def medicos_activos(self, request, pk=None):
        from clinic.models import Medico
        from clinic.serializers.medico import MedicoSummarySerializer
        especialidad = self.get_object()
        qs   = especialidad.medicos.filter(is_active=True).order_by('apellidos')
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                MedicoSummarySerializer(page, many=True).data
            )
        return Response(MedicoSummarySerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = Especialidad.objects.annotate(num_medicos=Count('medicos', distinct=True))
        return Response({
            'total':    qs.count(),
            'activas':  qs.filter(is_active=True).count(),
            'inactivas': qs.filter(is_active=False).count(),
            'detalle': [
                {
                    'id':          e.id,
                    'nombre':      e.nombre,
                    'num_medicos': e.num_medicos,
                    'is_active':   e.is_active,
                }
                for e in qs.order_by('nombre')
            ],
        })
