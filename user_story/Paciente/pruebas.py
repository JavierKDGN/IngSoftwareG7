import US_45 as us45

from app.models import Paciente, Medico, Cita, Horario, BloqueHorario, EstadoCita
from user_story.db_helper import verificar_paciente_existente, verificar_medico_existente, crear_paciente_y_medico, \
    imprimir_pacientes, mostrar_citas_medicos
from app import app, db

with app.app_context():

    us45.test_historial_citas(1)