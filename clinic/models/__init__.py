# clinic/models/__init__.py
from .especialidad import Especialidad
from .medico       import Medico
from .paciente     import Paciente
from .horario      import Horario
from .cita         import Cita
from .consulta     import Consulta
from .receta       import Receta

__all__ = [
    'Especialidad', 'Medico', 'Paciente',
    'Horario', 'Cita', 'Consulta', 'Receta',
]
