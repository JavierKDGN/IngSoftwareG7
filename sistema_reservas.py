import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import Paciente, Medico, Horario, Cita
import user_story.Paciente.US_123 as us123

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'Paciente': Paciente, 'Medico': Medico, 'Horario': Horario, 'Cita': Cita}

with app.app_context():
    story = 0
    while story != -1:
        story = int(input("Ingrese el numero de la user story "))
        if story == 1:
            print('US01: Como paciente, quiero reservar una cita médica con un médico en un horario específico para ser atendido.')
            print(us123.test_reservar_cita_medica())
        elif story == 2:
            print('US02: Como paciente, quiero poder cancelar o reprogramar mi cita en el sitio web para no tener que llamar al centro médico')
            print(us123.test_cancelar_cita())
        elif story == 3:
            print('US03: Como paciente, quiero ver la disponibilidad de los especialistas en un calendario a tiempo real para seleccionar la hora que mejor me convenga.')
            print(us123.test_ver_disponibilidad())