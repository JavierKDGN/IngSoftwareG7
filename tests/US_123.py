from app import app
import app.services.db_helper as dbh
from app.models import BloqueHorario, Horario, Cita
from app.services.servicio_citas import reservar_cita_medica, cancelar_cita_medica

# US01: Como paciente, quiero poder reservar una cita médica.
# Condición de aceptación: El paciente puede reservar una cita con un especialista.

def test_reservar_cita_medica():
    paciente, medico = dbh.crear_paciente_y_medico()
    fecha = "2024-11-07"
    bloque = BloqueHorario.BLOQUE_1
    resultado = reservar_cita_medica(paciente.id_paciente, medico.id_medico, fecha, bloque)
    return resultado

def test_cancelar_cita():
    paciente, medico = dbh.crear_paciente_y_medico()
    fecha = "2024-11-07"
    bloque = BloqueHorario.BLOQUE_1
    bloque2 = BloqueHorario.BLOQUE_2
    resultado = reservar_cita_medica(paciente.id_paciente, medico.id_medico, fecha, bloque)
    resultado2 = reservar_cita_medica(paciente.id_paciente, medico.id_medico, fecha, bloque2)

    #cancelamos cita 2
    citas_paciente = Cita.get_citas_por_paciente(paciente.id_paciente)
    cita_a_cancelar = resultado2 #queremos cancelar al 2da cita
    print(f"Citas del paciente {paciente}: {citas_paciente}")
    print(f"Cita a cancelar: {cita_a_cancelar}")
    resultado_cancelar = cancelar_cita_medica(cita_a_cancelar.id_cita)
    if resultado_cancelar:
        return f"Cita {cita_a_cancelar} cancelada correctamente"
    else:
        return f"Error al cancelar la cita"

def test_ver_disponibilidad():
    paciente, medico = dbh.crear_paciente_y_medico()
    fecha = "2024-11-07"
    bloques_disponibles = Horario.get_bloques_disp_en_fecha_de_medico(fecha, medico.id_medico)
    return f"Bloques disponibles para el medico {medico} en la fecha {fecha}: {bloques_disponibles}"

if __name__ == '__main__':
    with app.app_context():
        story = 0
        while story != -1:
            story = int(input("Ingrese el numero de la user story "))
            if story == 1:
                print('US01: Como paciente, quiero reservar una cita médica con un médico en un horario específico para ser atendido.')
                print(test_reservar_cita_medica())
            elif story == 2:
                print('US02: Como paciente, quiero poder cancelar o reprogramar mi cita en el sitio web para no tener que llamar al centro médico')
                print(test_cancelar_cita())
            elif story == 3:
                print('US03: Como paciente, quiero ver la disponibilidad de los especialistas en un calendario a tiempo real para seleccionar la hora que mejor me convenga.')
                print(test_ver_disponibilidad())