from datetime import date
from app.models import Paciente, Medico, Cita, Horario, BloqueHorario, EstadoCita
from user_story.db_helper import verificar_paciente_existente, verificar_medico_existente, crear_paciente_y_medico
from app import app, db
from HorarioMedico import HorarioMedico

# US01: Como paciente, quiero poder reservar una cita médica.
# Condición de aceptación: El paciente puede reservar una cita con un especialista.

# Clase que contiene funciones para revisar los bloques ocupados y mostrar el horario de un medico
# indicando los bloques ocupados y los libres


def reservar_cita_medica(id_paciente, id_medico, fecha, bloque):
    fecha = date.fromisoformat(fecha)

    # Buscar si existe una hora ocupada en la fecha y bloque del medico
    horario_ocupado = Horario.query.filter_by(fecha=fecha,
                                              bloque=bloque,
                                              id_medico=id_medico).first()

    #Si es que existe, revisar si ya tiene una cita agendada
    if horario_ocupado:
        cita_existente = Cita.query.filter(
            Cita.id_horario == horario_ocupado.id_horario,
            Cita.estado.in_([EstadoCita.AGENDADA, EstadoCita.CONFIRMADA, EstadoCita.REALIZADA])
        ).first()

        if cita_existente:
            # Si la cita existe y esta agendada o confirmada/realizada, no se puede reservar
            return False # Horario ocupado

    else:
        # Crear la cita y el bloque ocupado
        horario_ocupado = Horario(fecha=fecha,
                                 bloque=bloque,
                                 id_medico=id_medico
                          )
        db.session.add(horario_ocupado)
        db.session.flush()  # Obtener id_horario antes de crear la cita

        nueva_cita = Cita(id_paciente=id_paciente,
                          id_medico=id_medico,
                          id_horario= horario_ocupado.id_horario,
                          estado=EstadoCita.AGENDADA
                          )
        db.session.add(nueva_cita)
        db.session.commit()

        return id_paciente, id_medico, fecha, bloque, nueva_cita.id_cita

def cancelar_cita_medica(id_cita):
    cita = Cita.query.get(id_cita)
    if cita:
        cita.estado = EstadoCita.CANCELADA
        #luego se libera el bloque del medico
        db.session.commit()
        return True
    else:
        return False

def test_reservar_cita_medica():
    paciente, medico = crear_paciente_y_medico()
    fecha = "2024-11-07"
    bloque = BloqueHorario.BLOQUE_1
    resultado = reservar_cita_medica(paciente.id_paciente, medico.id_medico, fecha, bloque)
    return resultado

def test_cancelar_cita():
    paciente, medico = crear_paciente_y_medico()
    fecha = "2024-11-07"
    bloque = BloqueHorario.BLOQUE_1
    bloque2 = BloqueHorario.BLOQUE_2
    resultado = reservar_cita_medica(paciente.id_paciente, medico.id_medico, fecha, bloque)
    resultado2 = reservar_cita_medica(paciente.id_paciente, medico.id_medico, fecha, bloque2)

    #cancelamos cita 2
    citas_paciente = Cita.query.filter_by(id_paciente=paciente.id_paciente).all()
    cita_a_cancelar = citas_paciente[1] #queremos cancelar al 2da cita
    resultado_cancelar = cancelar_cita_medica(cita_a_cancelar.id_cita)
    if resultado_cancelar:
        return f"Cita {cita_a_cancelar} cancelada correctamente"
    else:
        return f"Error al cancelar la cita"

def test_ver_disponibilidad():
    paciente, medico = crear_paciente_y_medico()
    fecha = "2024-11-07"
    horario_medico = HorarioMedico()
    bloques_disponibles = horario_medico.mostrar_horario_medico_en_fecha(fecha, medico.id_medico)
    return f"Bloques disponibles para el medico {medico} en la fecha {fecha}: {bloques_disponibles}"

