import US_45 as us45
from datetime import date

from user_story import db_helper
from app.models import Paciente, Medico, Cita, Horario, BloqueHorario, EstadoCita
from app.routes_medicos import buscar_medicos
from user_story.Paciente.HorarioMedico import HorarioMedico
from user_story.Paciente.US_45 import buscar_medicos_print
from user_story.db_helper import verificar_paciente_existente, verificar_medico_existente, crear_paciente_y_medico, \
    imprimir_pacientes, mostrar_citas_medicos
from app import app, db

with app.app_context():
    db_helper.imprimir_medicos()
    #us45.test_historial_citas(1)
    medicos = buscar_medicos_print(nombre="Dr.", especialidad="Cardiología")
    for medico in medicos:

        us45.ocupar_todos_los_bloques(medico.id_medico, date(2024,11,7))
        if us45.get_medico_no_disponible(medico,"2024-11-07"):
            us45.buscar_especialistas_por_especialidad(medico.id_medico)