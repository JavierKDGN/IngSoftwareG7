from operator import truediv

from app.models import Paciente, Medico, Cita, Horario, BloqueHorario, EstadoCita
from user_story.Paciente.HorarioMedico import HorarioMedico
from app.services.db_helper import verificar_paciente_existente, verificar_medico_existente, crear_paciente_y_medico, imprimir_pacientes
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

def buscar_medicos_print(nombre='', apellido='', especialidad=''):
    # Crear consulta
    query = Medico.query

    # Aplicar filtros si se especifican
    if nombre:
        query = query.filter(Medico.nombre.ilike(f'%{nombre}%'))
    if apellido:
        query = query.filter(Medico.apellido.ilike(f'%{apellido}%'))
    if especialidad:
        query = query.filter(Medico.especialidad.ilike(f'%{especialidad}%'))

    # Realizar la consulta y obtener resultados
    medicos = query.all()

    # Imprimir los resultados en consola
    for medico in medicos:
        print(f'ID: {medico.id_medico}, Nombre: {medico.nombre}, Apellido: {medico.apellido}, '
              f'Especialidad: {medico.especialidad}, Teléfono: {medico.telefono}')
    return medicos

def ocupar_todos_los_bloques(id_medico, fecha):
    medico = Medico.query.get(id_medico)
    if not medico:
        print(f"Medico con id {id_medico} no encontrado.")
        return

    # Obtener todos los bloques
    bloques = list(BloqueHorario)

    # Crear horarios ocupados para cada bloque en la fecha especificada
    for bloque in bloques:
        horario = Horario(fecha=fecha, bloque=bloque, id_medico=id_medico)
        db.session.add(horario)
    db.session.commit()
    print(f"Todos los bloques para el medico {medico} en la fecha {fecha} han sido ocupados.")


def get_medico_no_disponible(medico, fecha):
    horario_medico = HorarioMedico()  # Crear una instancia de HorarioMedico
    if medico:
        bloques_disponibles = horario_medico.mostrar_horario_medico_en_fecha(fecha, medico.id_medico)
        print(f"Bloques disponibles para el medico {medico} en la fecha {fecha}: {bloques_disponibles}")
        if not bloques_disponibles:
            return True
        else:
            return False


def buscar_especialistas_por_especialidad(id_medico):
    # Buscar el médico inicial por ID
    medico_inicial = Medico.query.get(id_medico)
    if not medico_inicial:
        print(f"Médico con ID {id_medico} no encontrado.")
        return

    # Obtener la especialidad del médico inicial
    especialidad = medico_inicial.especialidad

    # Buscar todos los médicos con la misma especialidad
    especialistas = Medico.query.filter_by(especialidad=especialidad).all()

    # Imprimir los especialistas encontrados
    print(f"Especialistas en {especialidad}:")
    for especialista in especialistas:
        print(f"ID: {especialista.id_medico}, Nombre: {especialista.nombre} {especialista.apellido}, Teléfono: {especialista.telefono}")



def test_historial_citas(id_paciente):
    historial= obtener_historial_citas(id_paciente)
    for cita in historial:
        print(f"- Cita ID: {cita.id_cita}")
        print(f"  Estado: {cita.estado.name}")
        print(f"  Médico: {cita.medico.nombre} {cita.medico.apellido} - {cita.medico.especialidad}")
        print(f"  Fecha: {cita.horario.fecha}")
        print(f"  Bloque Horario: {cita.horario.bloque.name}")
        print("-" * 30)

