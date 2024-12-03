from datetime import date, timedelta
from flask_migrate import upgrade, downgrade
from app import app, db
from app.models import BloqueHorario, EstadoCita, Especialidad, Paciente, Medico, Horario, Cita
from app.services.servicio_citas import reservar_cita_medica
import sqlalchemy as sa



def formatear_base_datos():
    '''Reestablece la base de datos a un estado inicial y realiza la migracion para actualizarla'''
    seguro = input("Seguro? Se borraran todos los datos, esta funcion es solo para testear, escriba no para cancelar")
    if seguro:
        downgrade(directory='migrations', revision='base', sql=False, tag=None)
        upgrade(directory='migrations', revision='head', sql=False, tag=None)
    else:
        print("Operacion cancelada")

def popular_base_datos():
    """Crea datos de prueba para la base de datos: 5 pacientes y 5 médicos."""
    pacientes_data = [
        {"nombre": "Juan", "apellido": "Perez", "fecha_nacimiento": "1990-01-01", "email": "juan.perez@example.com", "telefono": "123456789"},
        {"nombre": "Maria", "apellido": "Gomez", "fecha_nacimiento": "1985-05-15", "email": "maria.gomez@example.com", "telefono": "987654321"},
        {"nombre": "Carlos", "apellido": "Lopez", "fecha_nacimiento": "1992-03-10", "email": "carlos.lopez@example.com", "telefono": "5647382910"},
        {"nombre": "Ana", "apellido": "Martinez", "fecha_nacimiento": "1995-08-20", "email": "ana.martinez@example.com", "telefono": "6758493021"},
        {"nombre": "Lucia", "apellido": "Garcia", "fecha_nacimiento": "1989-12-25", "email": "lucia.garcia@example.com", "telefono": "7685941234"},
    ]

    medicos_data = [
        {"nombre": "Dr.", "apellido": "Jose", "especialidad": Especialidad.CARDIOLOGIA, "telefono": "111222333"},
        {"nombre": "Dra", "apellido": "Laura","especialidad": Especialidad.DERMATOLOGIA, "telefono": "444555666"},
        {"nombre": "Dr", "apellido": "Martin","especialidad": Especialidad.PEDIATRIA, "telefono": "777888999"},
        {"nombre": "Dra", "apellido": "Sofia","especialidad": Especialidad.NEUROLOGIA, "telefono": "000111222"},
        {"nombre": "Dr", "apellido": "Diego","especialidad": Especialidad.OTORRINOLARINGOLOGIA, "telefono": "333444555"},
    ]

    # Crear pacientes

    pacientes = []
    for paciente_data in pacientes_data:
        if verificar_paciente_existente(paciente_data["nombre"], paciente_data["apellido"]):
            continue
        else:
            paciente = Paciente.crear_paciente(
                nombre=paciente_data["nombre"],
                apellido=paciente_data["apellido"],
                fecha_nacimiento=date.fromisoformat(paciente_data["fecha_nacimiento"]),
                email=paciente_data["email"],
                telefono=paciente_data["telefono"]
            )
        pacientes.append(paciente)

    # Crear medicos

    medicos = []
    for medico_data in medicos_data:
        if verificar_medico_existente(medico_data["nombre"], medico_data["apellido"]):
            continue
        else:
            medico = Medico.crear_medico(
                nombre=medico_data["nombre"],
                apellido=medico_data["apellido"],
                especialidad=medico_data["especialidad"],
                telefono=medico_data["telefono"]
            )
        medicos.append(medico)

    fecha_inicio = date.today()
    for dia in range(7):
        fecha = fecha_inicio + timedelta(days=dia)
        for paciente in pacientes:
            for medico in medicos:
                for bloque in [BloqueHorario.BLOQUE_1, BloqueHorario.BLOQUE_2, BloqueHorario.BLOQUE_3]:
                    cita = reservar_cita_medica(
                        id_paciente=paciente.id_paciente,
                        id_medico=medico.id_medico,
                        fecha=fecha,
                        bloque=bloque
                    )
                    if cita:
                        print(f"Cita creada para el paciente {paciente.nombre} con el médico {medico.nombre} en la fecha {fecha} y bloque {bloque}")


def popular_solo_medicos():
    """Crea datos de prueba para la base de datos: 5 médicos."""
    medicos_data = [
        {"nombre": "Jose", "apellido": "Martinez", "especialidad": Especialidad.CARDIOLOGIA, "telefono": "111222333"},
        {"nombre": "Laura", "apellido": "Fernandez", "especialidad": Especialidad.DERMATOLOGIA, "telefono": "444555666"},
        {"nombre": "Martin", "apellido": "Rodriguez", "especialidad": Especialidad.PEDIATRIA, "telefono": "777888999"},
        {"nombre": "Sofia", "apellido": "Gonzalez", "especialidad": Especialidad.NEUROLOGIA, "telefono": "000111222"},
        {"nombre": "Diego", "apellido": "Lopez", "especialidad": Especialidad.OTORRINOLARINGOLOGIA, "telefono": "333444555"},
    ]

    medicos = []
    for medico_data in medicos_data:
        if verificar_medico_existente(medico_data["nombre"], medico_data["apellido"]):
            continue
        else:
            medico = Medico.crear_medico(
                nombre=medico_data["nombre"],
                apellido=medico_data["apellido"],
                especialidad=medico_data["especialidad"],
                telefono=medico_data["telefono"]
            )
        medicos.append(medico)

def asignar_citas_medicos():
    """Asigna 2 horarios a cada médico con diferentes pacientes en distintos bloques y fechas."""

    # Obtener todos los pacientes y médicos disponibles
    pacientes = Paciente.query.all()
    medicos = Medico.query.all()

    # Asignar dos citas a cada médico
    fecha_inicial = date.today()  # Empezar desde la fecha de hoy
    bloques = [BloqueHorario.BLOQUE_1, BloqueHorario.BLOQUE_2]  # Ejemplo con dos bloques

    for idx, medico in enumerate(medicos):
        for i, bloque in enumerate(bloques):
            # Crear un horario específico para el médico
            horario = Horario(
                fecha=fecha_inicial + timedelta(days=idx),  # Fecha incrementada para cada médico
                bloque=bloque,
                id_medico=medico.id_medico
            )
            db.session.add(horario)
            db.session.flush()  # Obtener id_horario antes de crear la cita

            # Asignar un paciente a la cita (circular en la lista de pacientes)
            paciente = pacientes[(idx * 2 + i) % len(pacientes)]

            # Crear la cita
            cita = Cita(
                id_paciente=paciente.id_paciente,
                id_medico=medico.id_medico,
                id_horario=horario.id_horario,
                estado=EstadoCita.AGENDADA
            )
            db.session.add(cita)

    # Confirmar inserción en la base de datos
    db.session.commit()

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
        "especialidad": Especialidad.CARDIOLOGIA,
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
        nuevo_medico = Medico.crear_medico(
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

def ocupar_todos_los_bloques(id_medico, fecha):
    """Ocupa todos los bloques de un médico en una fecha específica."""
    for bloque in BloqueHorario:
        horario = Horario.crear_bloque_ocupado(fecha, bloque, id_medico)
        Cita.crear_cita(id_paciente=1, id_medico=id_medico, id_horario=horario.id_horario)

def verificar_paciente_existente(nombre, apellido):
    '''Verifica si un paciente con el nombre y apellido especificados ya existe en la base de datos'''
    return Paciente.query.filter_by(nombre=nombre, apellido=apellido).first()

def verificar_medico_existente(nombre, apellido):
    '''Verifica si un médico con el nombre especificado ya existe en la base de datos'''
    return Medico.query.filter_by(nombre=nombre, apellido=apellido).first()

