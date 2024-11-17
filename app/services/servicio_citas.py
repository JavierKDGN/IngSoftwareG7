from datetime import date
from app.models import Horario, Cita, BloqueHorario, EstadoCita

def reservar_cita_medica(id_paciente,id_medico,fecha,bloque):

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
    if cita_cancelada:
        print(f"Cita {id_cita} cancelada correctamente")
        return True
    else:
        print(f"Error al cancelar la cita")
        return False

def obtener_historial_citas_paciente(id_paciente):
    return Cita.get_citas_por_paciente(id_paciente)



