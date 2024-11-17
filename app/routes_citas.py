from flask import jsonify, request
from app import app, db
from app.models import Cita, EstadoCita
from datetime import datetime

# US08: Como médico, quiero actualizar el estatus de una cita (confirmada, cancelada, atendida) directamente en el sistema para mantener la información
# Condición de aceptación: El medico puede seleccionar y realizar el cambio del status de sus citas

@app.route('/api/medico/<int:id_medico>/citas', methods=['GET'])
def obtener_citas_medico(id_medico):
    # Obtener los parametros para el filtro
    fecha = request.args.get('fecha')
    estado = request.args.get('estado')

    # Consulta base
    query = Cita.query.filter_by(id_medico=id_medico)

    # Aplica los filtros si se elijen
    if fecha:
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
        query = query.join(Cita.horario).filter(Horario.fecha == fecha)

    if estado:
        try:
            estado_enum = EstadoCita[estado.upper()]
            query = query.filter_by(estado=estado_enum)
        except KeyError:
            return jsonify({'error': 'Estado inválido'}), 400

    citas = query.all()

    return jsonify([{
        'id': cita.id_cita,
        'paciente': f"{cita.paciente.nombre} {cita.paciente.apellido}",
        'fecha': cita.horario.fecha.isoformat(),
        'bloque': cita.horario.bloque.name,
        'estado': cita.estado.name
    } for cita in citas])


@app.route('/api/citas/<int:id_cita>/estado', methods=['PUT'])
def actualizar_estado_cita(id_cita):
    nuevo_estado = request.json.get('estado')

    # Validar el nuevo estado de la cita
    try:
        estado_enum = EstadoCita[nuevo_estado.upper()]
    except KeyError:
        return jsonify({'error': 'Estado inválido'}), 400

    cita = Cita.query.get_or_404(id_cita)
    cita.estado = estado_enum
    db.session.commit()

    return jsonify({
        'id': cita.id_cita,
        'estado': cita.estado.name,
        'mensaje': 'Estado actualizado correctamente'
    })
