from datetime import date
from app.models import Horario, Cita, BloqueHorario, EstadoCita

def reservar_cita_medica(id_paciente,id_medico,fecha,bloque):

    # Buscar si existe una hora ocupada en la fecha y bloque del medico
    bloques_ocupados = Horario.get_bloques_ocup_en_fecha_de_medico(fecha, id_medico)
    horario_ocupado = None

    if bloque in bloques_ocupados:
        horario_ocupado = bloques_ocupados[bloque]

    #Si es que existe, revisar si ya tiene una cita agendada
    if horario_ocupado:
        cita_existente = Cita.get_citas_por_horario(horario_ocupado.id_horario)
        # Si la cita existe y esta agendada o confirmada/realizada, no se puede reservar
        for cita in cita_existente:
            if cita_existente.estado not in [EstadoCita.CANCELADA]:
                return False

        # Si la cita existe pero fue cancelada, se puede reservar

    else:
        # Crear el bloque ocupado
        horario_ocupado = Horario.crear_bloque_ocupado(fecha, bloque, id_medico)

    # Crear la cita
    nueva_cita = Cita.crear_cita(id_paciente, id_medico, horario_ocupado.id_horario)

    print('Cita creada exitosamente')
    return nueva_cita

def cancelar_cita_medica(id_cita):
    return Cita.cancelar_cita(id_cita)

def obtener_historial_citas_paciente(id_paciente):
    return Cita.get_citas_por_paciente(id_paciente)



