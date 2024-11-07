from datetime import date, timedelta
from flask_migrate import upgrade, downgrade
from app import app, db
from app.models import BloqueHorario, EstadoCita
from app.models import Paciente, Medico, Horario, Cita
import sqlalchemy as sa

def formatear_base_datos():
    '''Reestablece la base de datos a un estado inicial y realiza la migracion para actualizarla'''
    seguro = input("Seguro? Se borraran todos los datos, esta funcion es solo para testear, escriba no para cancelar")
    if seguro:
        downgrade(directory='migrations', revision='base', sql=False, tag=None)
        upgrade(directory='migrations', revision='head', sql=False, tag=None)
    else:
        print("Operacion cancelada")


# De aca a abajo son testeos de inserciones en la base de datos hechos por ChatGPT
# para comprobar que las relaciones entre tablas funcionan correctamente

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
        {"nombre": "Dr.", "apellido": "Jose", "especialidad": "Cardiología", "telefono": "111222333"},
        {"nombre": "Dra", "apellido": "Laura","especialidad": "Dermatología", "telefono": "444555666"},
        {"nombre": "Dr", "apellido": "Martin","especialidad": "Pediatría", "telefono": "777888999"},
        {"nombre": "Dra", "apellido": "Sofia","especialidad": "Neurología", "telefono": "000111222"},
        {"nombre": "Dr", "apellido": "Diego","especialidad": "Odontología", "telefono": "333444555"},
    ]

    # Crear pacientes
    for paciente_data in pacientes_data:
        paciente = Paciente(
            nombre=paciente_data["nombre"],
            apellido=paciente_data["apellido"],
            fecha_nacimiento=date.fromisoformat(paciente_data["fecha_nacimiento"]),
            email=paciente_data["email"],
            telefono=paciente_data["telefono"]
        )
        db.session.add(paciente)

    # Crear medicos
    for medico_data in medicos_data:
        medico = Medico(
            nombre=medico_data["nombre"],
            apellido=medico_data["apellido"],
            especialidad=medico_data["especialidad"],
            telefono=medico_data["telefono"]
        )
        db.session.add(medico)

    # Confirmar inserción en la base de datos
    db.session.commit()

def imprimir_pacientes():
    '''Imprime todos los pacientes en la base de datos'''
    pacientes = Paciente.query.all()
    print("Pacientes:")
    for paciente in pacientes:
        print(paciente)

def imprimir_medicos():
    '''Imprime todos los médicos en la base de datos'''
    medicos = Medico.query.all()
    print("Médicos:")
    for medico in medicos:
        print(medico)

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

def mostrar_citas_medicos():
    """Imprime las citas de cada médico, incluyendo el paciente, fecha, bloque y estado."""

    medicos = Medico.query.all()

    for medico in medicos:
        print(f"\nMédico: {medico.apellido} - Especialidad: {medico.especialidad}")
        print("=" * 50)

        # Obtener todas las citas del médico actual
        citas = Cita.query.filter_by(id_medico=medico.id_medico).all()

        if not citas:
            print("No hay citas para este médico.")
            continue

        # Mostrar los detalles de cada cita
        for cita in citas:
            paciente = cita.paciente
            horario = cita.horario
            print(f"Cita ID: {cita.id_cita}")
            print(f"  Paciente: {paciente.nombre} {paciente.apellido}")
            print(f"  Fecha: {horario.fecha}")
            print(f"  Bloque: {horario.bloque.name}")
            print(f"  Estado: {cita.estado.name}")
            print("-" * 50)


def verificar_paciente_existente(nombre, apellido):
    '''Verifica si un paciente con el nombre y apellido especificados ya existe en la base de datos'''
    return Paciente.query.filter_by(nombre=nombre, apellido=apellido).first()

def verificar_medico_existente(nombre, apellido):
    '''Verifica si un médico con el nombre especificado ya existe en la base de datos'''
    return Medico.query.filter_by(nombre=nombre, apellido=apellido).first()