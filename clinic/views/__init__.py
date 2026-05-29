# clinic/views/__init__.py
from .auth         import RegisterView, LogoutView
from .user         import UserViewSet
from .especialidad import EspecialidadViewSet
from .medico       import MedicoViewSet
from .paciente     import PacienteViewSet
from .horario      import HorarioViewSet
from .cita         import CitaViewSet
from .consulta     import ConsultaViewSet
