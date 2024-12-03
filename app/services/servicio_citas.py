from datetime import date
from app.models import Horario, Cita, BloqueHorario, EstadoCita
from app.utils import parse_bloque

'''Funcionamiento del sistema de reservas
El sistema de reservas se encarga de manejar las citas medicas entre los pacientes y los medicos.

Notas refactoring:
Cuando se reserva una hora, se crea un bloque ocupado en la tabla Horario, y se crea una cita en la tabla Cita.
Si se cancela una cita, se cambia el estado de la cita a CANCELADA sin embargo el bloque sigue existiendo en la tabla Horario.
Esto ultimo es debido a que si se borrase el bloque se generaria un error en la Base de Datos al intentar acceder a un bloque que ya no existe,
cuando se quiere revisar citas canceladas. Para evitar este tipo de problemas ahora se realiza todos los accesos a la base de datos a traves de las funciones
dentro de las clases de models.py y no directamente desde la logica de las funciones. en caso de necesitar un acceso que no esta
en las funciones de models.py se debe crear una nueva funcion en la clase correspondiente. (como un getter o setter)

'''

def reservar_cita_medica(id_paciente,id_medico,fecha,bloque):
    bloque = parse_bloque(bloque)
    horario_ocupado = Horario.get_bloque_ocupado(fecha, bloque, id_medico)

    #Si el horario esta disponible
    if horario_ocupado is None:
        horario_ocupado = Horario.crear_bloque_ocupado(fecha, bloque, id_medico)
        return Cita.crear_cita(id_paciente, id_medico, horario_ocupado.id_horario)

    #Si el horario sale ocupado, hay que revisar si la citas de aquel horario estan canceladas

    citas_existentes = Cita.get_citas_por_horario(horario_ocupado.id_horario)
    for cita in citas_existentes:
        if cita.estado != EstadoCita.CANCELADA:
            return None

    #Si todas las citas estan canceladas, se puede reservar el horario
    return Cita.crear_cita(id_paciente, id_medico, horario_ocupado.id_horario)

def cancelar_cita_medica(id_cita):
    cita_cancelada = Cita.cancelar_cita(id_cita)
    print(cita_cancelada)
    if cita_cancelada:
        print(f"Cita {id_cita} cancelada correctamente")
        return cita_cancelada
    else:
        print(f"Error al cancelar la cita")
        return None

# def obtener_historial_citas_paciente(id_paciente):
#     return Cita.get_citas_por_paciente(id_paciente)
#
# Implementada en Cita.get_citas_por_paciente

