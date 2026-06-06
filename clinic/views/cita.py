# clinic/views/cita.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from clinic.models            import Cita, Paciente, Medico
from clinic.serializers.cita  import CitaSerializer, AgendarCitaSerializer
from clinic.permissions       import IsStaffOrReadOnly
from clinic.filters           import CitaFilter
from clinic.pagination        import StandardPagination


class CitaViewSet(viewsets.ModelViewSet):
    serializer_class   = CitaSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, OrderingFilter]
    filterset_class    = CitaFilter
    ordering_fields    = ['fecha_hora', 'created_at']
    ordering           = ['-fecha_hora']
    http_method_names  = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        return (
            Cita.objects
            .select_related('paciente', 'medico', 'registrado_por')
            .all()
        )

    def perform_create(self, serializer):
        serializer.save(registrado_por=self.request.user)

    @action(detail=False, methods=['post'], url_path='agendar')
    def agendar(self, request):
        serializer = AgendarCitaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data
        cita = Cita.objects.create(
            paciente_id    = d['paciente_id'],
            medico_id      = d['medico_id'],
            fecha_hora     = d['fecha_hora'],
            motivo         = d.get('motivo', ''),
            registrado_por = request.user,
        )
        return Response(CitaSerializer(cita).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='confirmar')
    def confirmar(self, request, pk=None):
        cita = self.get_object()
        if cita.estado != 'pendiente':
            return Response(
                {'error': 'Solo se pueden confirmar citas en estado pendiente.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cita.estado = 'confirmada'
        cita.save(update_fields=['estado'])
        return Response(CitaSerializer(cita).data)

    @action(detail=True, methods=['post'], url_path='cancelar')
    def cancelar(self, request, pk=None):
        cita = self.get_object()
        if cita.estado in ['atendida', 'cancelada']:
            return Response(
                {'error': f'No se puede cancelar una cita con estado "{cita.estado}".'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cita.estado = 'cancelada'
        cita.save(update_fields=['estado'])
        return Response(CitaSerializer(cita).data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdminUser],
        url_path='cambiar-estado',
    )
    def cambiar_estado(self, request, pk=None):
        cita          = self.get_object()
        nuevo_estado  = request.data.get('estado')
        estados_validos = [s[0] for s in Cita.ESTADO_CHOICES]
        if nuevo_estado not in estados_validos:
            return Response(
                {'error': f'Estado inválido. Opciones válidas: {estados_validos}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cita.estado = nuevo_estado
        cita.save(update_fields=['estado'])
        return Response(CitaSerializer(cita).data)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAdminUser],
        url_path='stats',
    )
    def stats(self, request):
        from django.db.models import Count
        qs     = Cita.objects.all()
        totals = qs.aggregate(total_citas=Count('id'))
        por_estado = {
            s: qs.filter(estado=s).count()
            for s, _ in Cita.ESTADO_CHOICES
        }
        return Response({
            'total_citas': totals['total_citas'],
            'por_estado':  por_estado,
        })
