from datetime import date
from app.models import Paciente, Medico, Cita, Horario, BloqueHorario, EstadoCita
from user_story.db_helper import verificar_paciente_existente, verificar_medico_existente
from app import app, db

def reservar_cita_medica(id_paciente, id_medico, fecha, bloque):
    fecha = date.fromisoformat(fecha)

    # Verificar si el horario está disponible
    horario = Horario.query.filter_by(fecha=fecha, bloque=bloque, id_medico=id_medico).first()

    if horario:
        return "El horario ya está ocupado."
    else:
        # Crear la cita
        bloque_ocupado = Horario(fecha=fecha,
                                 bloque=bloque,
                                 id_medico=id_medico
                          )
        db.session.add(bloque_ocupado)
        db.session.flush()  # Obtener id_horario antes de crear la cita

        nueva_cita = Cita(id_paciente=id_paciente,
                          id_medico=id_medico,
                          id_horario= bloque_ocupado.id_horario,
                          estado=EstadoCita.AGENDADA
                          )
        db.session.add(nueva_cita)
        db.session.commit()

        return "Cita agendada exitosamente."

def crear_paciente_y_medico():
    datos_paciente_dummy = {
        "nombre": "Juan",
        "apellido": "Perez",
        "fecha_nacimiento": "2024-11-07",
        "email": "juan.perez@test.com",
        "telefono": "912345678"
    }

    datos_medico_dummy = {
        "nombre": "Dr.",
        "apellido": "Jose",
        "especialidad": "Cardiología",
        "telefono": "111222333"
    }

    # Verificar o crear paciente
    if not verificar_paciente_existente(datos_paciente_dummy["nombre"], datos_paciente_dummy["apellido"]):
        nuevo_paciente = Paciente(
            nombre=datos_paciente_dummy["nombre"],
            apellido=datos_paciente_dummy["apellido"],
            fecha_nacimiento=date.fromisoformat(datos_paciente_dummy["fecha_nacimiento"]),
            email=datos_paciente_dummy["email"],
            telefono=datos_paciente_dummy["telefono"]
        )
        db.session.add(nuevo_paciente)
        db.session.commit()
    else:
        nuevo_paciente = Paciente.query.filter_by(
            nombre=datos_paciente_dummy["nombre"],
            apellido=datos_paciente_dummy["apellido"]
        ).first()

    # Verificar o crear médico
    if not verificar_medico_existente("Dr.", "Jose"):
        nuevo_medico = Medico(
            nombre=datos_medico_dummy["nombre"],
            apellido=datos_medico_dummy["apellido"],
            especialidad=datos_medico_dummy["especialidad"],
            telefono=datos_medico_dummy["telefono"]
        )
        db.session.add(nuevo_medico)
        db.session.commit()
    else:
        nuevo_medico = Medico.query.filter_by(
            nombre=datos_medico_dummy["nombre"],
            apellido=datos_medico_dummy["apellido"]
        ).first()

    return nuevo_paciente, nuevo_medico

# US01: Como paciente, quiero reservar una cita médica con un médico en un horario específico para ser atendido.

def test_reservar_cita_medica():
    paciente, medico = crear_paciente_y_medico()
    fecha = "2024-11-07"
    bloque = BloqueHorario.BLOQUE_1
    resultado = reservar_cita_medica(paciente.id_paciente, medico.id_medico, fecha, bloque)
    return resultado



