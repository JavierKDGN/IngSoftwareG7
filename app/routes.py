import time

from flask import render_template, redirect, url_for, request, jsonify, session
from app import app
from app.models import *
from app.services.servicio_citas import reservar_cita_medica
from app.utils import bloque_a_rango_horario, parse_nombre, parse_rut


# Este archivo define las rutas de la aplicacion
# se utilizan los decoradores @app.route('/')
# para definir las rutas, y el comportamiento
# de la pagina (lo que se mostrara y renderizara en html)

# decoradores para definir las rutas
#ej de ruta localhost:5000/ mostrara el mensaje Hello!
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/especialistas')
def especialistas():
    especialistas_lista = Medico.get_all_medicos()
    return render_template('especialistas.html', especialistas=especialistas_lista)

@app.route('/centroayuda')
def centroayuda():
    return render_template('centroayuda.html')

@app.route('/reservar/especialistas', methods=['GET', 'POST'])
def seleccionar_especialista():
    especialidades = [e.name for e in Especialidad]
    medicos = None

    if request.method == 'POST':
        especialidad = request.form.get('especialidad')
        id_medico = request.form.get('especialista')
        fecha = request.form.get('fecha')
        bloque = request.form.get('bloque')

        print(f"POST Data: {request.form}")
        print(f"Datos enviados:  {id_medico}, {fecha}, {bloque}")
        # Si se seleccionan todos los datos, redirigir a la página de datos del paciente
        if id_medico and fecha and bloque:
            print("Redirigiendo a datos del paciente")
            return redirect(url_for('datos_paciente', id_medico=id_medico, fecha=fecha, bloque=bloque))

        # Si se selecciona una especialidad, cargar los médicos
        if especialidad:
            medicos = Medico.get_medico_por_especialidad(especialidad)

    return render_template('seleccionar_especialista.html', especialidades=especialidades, medicos=medicos)

@app.route('/especialistas/<especialidad_name>')
def obtener_especialistas(especialidad_name):
    try:
        especialidad = Especialidad[especialidad_name]  # Convierte el nombre al Enum
        especialistas = Medico.get_medico_por_especialidad(especialidad)
        especialistas_data = [
            {'id': medico.id_medico, 'nombre': medico.get_nombre_medico()}
            for medico in especialistas
        ]
        return jsonify(especialistas_data)
    except KeyError:
        return jsonify({'error': 'Especialidad no encontrada'}), 404

@app.route('/especialistas/<int:id_medico>/disponibilidad', methods=['GET'])
def obtener_disponibilidad_medico(id_medico):
    # Simulación de días disponibles (puedes ajustar según la lógica real)
    dias_disponibles = 7
    fechas = Medico.get_fechas_disponibles_hasta_dias(id_medico, dias_disponibles)

    disponibilidad = {}
    for fecha in fechas:
        bloques = Horario.get_bloques_disp_en_fecha_de_medico(fecha, id_medico)
        disponibilidad[str(fecha)] = [bloque_a_rango_horario(bloque) for bloque in bloques]

    return jsonify(disponibilidad)

@app.route('/reservar/datos-paciente', methods=['GET', 'POST'])
def datos_paciente():
    """Formulario para ingresar los datos del paciente después de seleccionar el médico y el horario."""
    if request.method == 'POST':
        id_medico = request.form.get('id_medico')
        fecha = request.form.get('fecha')
        bloque = request.form.get('bloque')
        nombre_paciente = request.form.get('nombre_paciente')
        rut_paciente = request.form.get('rut_paciente')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        bloque = parse_bloque(bloque)

        nombre_paciente, apellido_paciente = parse_nombre(nombre_paciente)
        rut_paciente = parse_rut(rut_paciente)

        paciente = Paciente.crear_paciente(rut=rut_paciente, nombre=nombre_paciente,apellido=apellido_paciente, telefono=telefono, email=email)
        paciente_id = paciente.id_paciente
        print(f"Reservando cita para paciente {paciente_id} con médico {id_medico} el {fecha} en el bloque {bloque}")
        cita = reservar_cita_medica(paciente_id, id_medico, fecha, bloque)

        print(cita)
        if cita:
            return redirect(url_for('cita_confirmada', cita_id=cita.id_cita))
        else:
            return redirect(url_for('cita_rechazada'))

    # Si es get renderizar formulario
    id_medico = request.args.get('id_medico')
    fecha = request.args.get('fecha')
    bloque = request.args.get('bloque')
    medico = Medico.query.get_or_404(id_medico)

    return render_template('datos_paciente.html', medico=medico, fecha=fecha, bloque=bloque)

@app.route('/cita_confirmada/<cita_id>')
def cita_confirmada(cita_id):
    """Muestra la confirmación de una cita exitosa."""
    cita = Cita.get_cita(cita_id)
    return f"Cita reservada correctamente, ID: {cita.id_cita}"

@app.route('/cita_rechazada')
def cita_rechazada():
    """Muestra un mensaje de error si no se pudo reservar la cita."""
    return "No se pudo reservar la cita, por favor intente nuevamente"