from datetime import date, timedelta
from app import app
import app.services.db_helper as dbh
from app.models import BloqueHorario, Horario, Cita, Paciente, Medico
from app.services.servicio_citas import reservar_cita_medica, cancelar_cita_medica
from app.utils import parse_fecha

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

def test_interaccion_paciente():
    dbh.popular_base_datos()
    print("Ingrese sus datos de paciente: ")
    datos_test = {
        "rut": "11111111-1",
        "nombre": "Test",
        "apellido": "User",
        "fecha_nacimiento": "1990-01-01",
        "email": "test.user@example.com",
        "telefono": "555555555"
    }
    paciente = None

    if dbh.verificar_paciente_existente(datos_test["nombre"], datos_test["apellido"]):
        paciente = Paciente.query.filter_by(nombre=datos_test["nombre"], apellido=datos_test["apellido"]).first()
        print(f"Paciente encontrado: {paciente}")
    else:
        paciente = Paciente.crear_paciente(datos_test["nombre"], datos_test["apellido"], datos_test["fecha_nacimiento"], datos_test["email"], datos_test["telefono"])
        print(f"Paciente creado: {paciente}")

    print("Bienvenido a la aplicacion de citas medicas")
    print("Seleccione una opcion: ")
    print("1. Reservar cita medica")
    print("2. Cancelar cita medica")
    opcion = int(input())
    if opcion == 1:
        print("Reservar cita medica")
        print("Que especialidad desea?")
        especialidad = input()
        medicos = Medico.get_medico_por_especialidad(especialidad)
        print("Medicos disponibles: ")
        for medico in medicos:
            print(f"{medico.id_medico}: Dr. {medico.apellido}")

        while True:
            id_medico = int(input("Seleccione el medico por su id: "))
            if id_medico not in [medico.id_medico for medico in medicos]:
                print("Id de medico invalido")
                continue
            else:
                break

        print(f"Ha seleccionado al medico {Medico.get_medico(id_medico)}")
        print("Verificando disponibilidad de horarios...")

        dias_disponibles = Medico.get_fechas_disponibles_hasta_dias(id_medico, 7)

        if dias_disponibles:
            print("Los dias disponibles son: ")
            for dia in dias_disponibles:
                print(parse_fecha(dia))

        # Seleccionar un día disponible para la cita
        while True:
            fecha_str = input("Seleccione una fecha disponible (YYYY-MM-DD): ")
            fecha_seleccionada = parse_fecha(fecha_str)
            if fecha_seleccionada not in dias_disponibles:
                print("Fecha no disponible. Por favor, elija una de las opciones mostradas.")
                continue
            else:
                break

        # Mostrar bloques disponibles en la fecha seleccionada
        bloques_disponibles = Horario.get_bloques_disp_en_fecha_de_medico(fecha_seleccionada,id_medico)
        if bloques_disponibles:
            print("Los bloques de tiempo disponibles son:")
            for bloque in bloques_disponibles:
                print(f"{bloque}")

            # Seleccionar un bloque de tiempo
            while True:
                bloque = int(input("Seleccione un bloque de tiempo por su número: "))
                bloque = BloqueHorario(bloque)
                if bloque not in bloques_disponibles:
                    print("Bloque no disponible. Intente de nuevo.")
                    continue
                else:
                    break

            cita = reservar_cita_medica(paciente.id_paciente, id_medico, fecha_seleccionada, bloque)
            if cita:
                print(f"Cita reservada con éxito: {cita}")
            else:
                print("No se pudo reservar la cita. El bloque ya está ocupado o todas las citas existentes en el bloque están activas.")
        else:
            print("No hay bloques de tiempo disponibles en la fecha seleccionada.")



if __name__ == '__main__':
    with app.app_context():
        # story = 0
        # while story != -1:
        #     story = int(input("Ingrese el numero de la user story "))
        #     if story == 1:
        #         print('US01: Como paciente, quiero reservar una cita médica con un médico en un horario específico para ser atendido.')
        #         print(test_reservar_cita_medica())
        #     elif story == 2:
        #         print('US02: Como paciente, quiero poder cancelar o reprogramar mi cita en el sitio web para no tener que llamar al centro médico')
        #         print(test_cancelar_cita())
        #     elif story == 3:
        #         print('US03: Como paciente, quiero ver la disponibilidad de los especialistas en un calendario a tiempo real para seleccionar la hora que mejor me convenga.')
        #         print(test_ver_disponibilidad())

        test_interaccion_paciente()