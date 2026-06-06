# clinic/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from clinic.views.health       import health_check, testing_cicd
from clinic.views.auth         import RegisterView, LogoutView
from clinic.views.user         import UserViewSet
from clinic.views.especialidad import EspecialidadViewSet
from clinic.views.medico       import MedicoViewSet
from clinic.views.paciente     import PacienteViewSet
from clinic.views.horario      import HorarioViewSet
from clinic.views.cita         import CitaViewSet
from clinic.views.consulta     import ConsultaViewSet
from clinic.serializers.auth   import CustomTokenView

router = DefaultRouter()
router.register('users',         UserViewSet,         basename='user')
router.register('especialidades', EspecialidadViewSet, basename='especialidad')
router.register('medicos',       MedicoViewSet,       basename='medico')
router.register('pacientes',     PacienteViewSet,     basename='paciente')
router.register('horarios',      HorarioViewSet,      basename='horario')
router.register('citas',         CitaViewSet,         basename='cita')
router.register('consultas',     ConsultaViewSet,     basename='consulta')

urlpatterns = [
    path('health/',             health_check),
    path('testing-cicd/',       testing_cicd),
    path('auth/register/',      RegisterView.as_view()),
    path('auth/login/',         CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/',  TokenVerifyView.as_view()),
    path('auth/logout/',        LogoutView.as_view()),
    path('', include(router.urls)),
]
