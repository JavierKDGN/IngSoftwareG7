from app.models import Paciente, Medico, Cita, Horario, BloqueHorario, EstadoCita
from user_story.db_helper import verificar_paciente_existente, verificar_medico_existente, crear_paciente_y_medico, \
    imprimir_pacientes
from app import app, db

def obtener_historial_citas(paciente_id):
    paciente = Paciente.query.get(paciente_id)

    if not paciente:
        return "Paciente no encontrado"

    # Crear una lista para almacenar las citas que serán parte del historial
    historial = []

    # Recorrer todas las citas del paciente
    for cita in paciente.citas:
        # Comprobar si el estado de la cita es REALIZADA o CANCELADA
        if cita.estado == EstadoCita.REALIZADA or cita.estado == EstadoCita.CANCELADA:
            # Agregar la cita al historial si cumple con el criterio
            historial.append(cita)
    return historial


def test_historial_citas(id_paciente):
    historial= obtener_historial_citas(id_paciente)
    for cita in historial:
        print(f"- Cita ID: {cita.id_cita}")
        print(f"  Estado: {cita.estado.name}")
        print(f"  Médico: {cita.medico.nombre} {cita.medico.apellido} - {cita.medico.especialidad}")
        print(f"  Fecha: {cita.horario.fecha}")
        print(f"  Bloque Horario: {cita.horario.bloque.name}")
        print("-" * 30)

