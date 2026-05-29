# clinic/views/consulta.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from clinic.models              import Consulta, Receta
from clinic.serializers.consulta import (
    ConsultaSerializer,
    RecetaSerializer,
    AgregarRecetaSerializer,
)
from clinic.permissions         import IsStaffOrReadOnly
from clinic.filters             import ConsultaFilter
from clinic.pagination          import StandardPagination


class ConsultaViewSet(viewsets.ModelViewSet):
    queryset           = Consulta.objects.select_related('cita__paciente', 'cita__medico').all()
    serializer_class   = ConsultaSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, OrderingFilter]
    filterset_class    = ConsultaFilter
    ordering_fields    = ['created_at']
    ordering           = ['-created_at']
    http_method_names  = ['get', 'post', 'patch', 'delete', 'head', 'options']

    @action(detail=True, methods=['post'], url_path='agregar-receta')
    def agregar_receta(self, request, pk=None):
        consulta   = self.get_object()
        serializer = AgregarRecetaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        receta = Receta.objects.create(
            consulta=consulta,
            **serializer.validated_data,
        )
        return Response(RecetaSerializer(receta).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='recetas')
    def listar_recetas(self, request, pk=None):
        consulta = self.get_object()
        qs       = consulta.recetas.all()
        page     = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(RecetaSerializer(page, many=True).data)
        return Response(RecetaSerializer(qs, many=True).data)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAdminUser],
        url_path='stats',
    )
    def stats(self, request):
        from django.db.models import Count, Avg
        qs = Consulta.objects.all()
        data = qs.aggregate(
            total_consultas = Count('id'),
            promedio_recetas = Avg('recetas__id'),
        )
        return Response({
            'total_consultas':  data['total_consultas'],
            'total_recetas':    Receta.objects.count(),
        })
