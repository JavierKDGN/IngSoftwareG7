from flask import jsonify, request
from app import app, db
from app.models import Medico

# US09: Como paciente, quiero poder filtrar a los especialistas por tipo de consulta (cardiología, pediatría, etc) para encontrar más rápido el servicio
# Condición de aceptación: El usuario a la hora de agendar su cita tiene la opcion de filtrar a los especialistas lo que simplifica la eleccion de el especialista
@app.route('/api/medicos/buscar', methods=['GET'])
def buscar_medicos():
    # Obtener parametros para el filtro
    nombre = request.args.get('nombre', '').strip()
    apellido = request.args.get('apellido', '').strip()
    especialidad = request.args.get('especialidad', '').strip()

    # Crea consulta
    query = Medico.query

    # Aplicar filtros si se elijen
    if nombre:
        query = query.filter(Medico.nombre.ilike(f'%{nombre}%'))
    if apellido:
        query = query.filter(Medico.apellido.ilike(f'%{apellido}%'))
    if especialidad:
        query = query.filter(Medico.especialidad.ilike(f'%{especialidad}%'))

    # Realizar consulta
    medicos = query.all()

    return jsonify([{
        'id': medico.id_medico,
        'nombre': medico.nombre,
        'apellido': medico.apellido,
        'especialidad': medico.especialidad,
        'telefono': medico.telefono
    } for medico in medicos])


@app.route('/api/especialidades', methods=['GET'])
def obtener_especialidades():
    # Obtener especialidades de los medicos
    especialidades = db.session.query(Medico.especialidad) \
        .distinct() \
        .order_by(Medico.especialidad) \
        .all()
    return jsonify([esp[0] for esp in especialidades])
