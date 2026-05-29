# clinic/serializers/__init__.py
from .auth           import CustomTokenSerializer, CustomTokenView
from .user           import (
    RegisterSerializer,
    UserSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)
from .especialidad   import EspecialidadSerializer
from .medico         import MedicoSerializer, MedicoSummarySerializer
from .paciente       import PacienteSerializer, PacienteSummarySerializer
from .horario        import HorarioSerializer
from .cita           import CitaSerializer, AgendarCitaSerializer
from .consulta       import ConsultaSerializer, RecetaSerializer, AgregarRecetaSerializer
