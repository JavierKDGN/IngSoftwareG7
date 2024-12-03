from flask import render_template, redirect, url_for, request
from app import app
from app.models import *
from app.services.servicio_citas import reservar_cita_medica
from app.utils import rango_horario_bloque


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
        id_medico = request.form.get('medico')

        # Si se selecciona una especialidad, cargar los médicos
        if especialidad:
            medicos = Medico.get_medico_por_especialidad(especialidad)

        # Si se selecciona un médico, redirigir a la página de reserva
        if id_medico:
            return redirect(url_for('reservar_cita', id_medico=id_medico))

    return render_template('seleccionar_especialista.html', especialidades=especialidades, medicos=medicos)


@app.route('/reservar/<int:id_medico>', methods=['GET', 'POST'])
def reservar_cita(id_medico):
    medico = Medico.query.get_or_404(id_medico)
    fechas, bloques = None, None
    bloque_string = {}

    if request.method == 'POST':
        fecha = request.form.get('fecha')
        bloque = request.form.get('bloque')

        # Si se selecciona una fecha, cargar los bloques horarios
        if fecha and not bloque:
            bloques = Horario.get_bloques_disp_en_fecha_de_medico(fecha, id_medico)
            bloque_string = {bloque: rango_horario_bloque(bloque) for bloque in bloques}

        # Si se selecciona un bloque, reservar la cita
        elif bloque:
            paciente_id = 1  # Simulación de paciente autenticado
            cita = reservar_cita_medica(paciente_id, id_medico, fecha, bloque)
            if cita:
                return redirect(url_for('cita_confirmada', cita_id=cita.id_cita))
            else:
                return redirect(url_for('cita_rechazada'))

    # Obtener fechas disponibles por default
    dias_disponibles = 7
    fechas = Medico.get_fechas_disponibles_hasta_dias(id_medico, dias_disponibles)

    return render_template('reservar_cita.html', medico=medico, fechas=fechas, bloques=bloque_string)


@app.route('/cita_confirmada/<cita_id>')
def cita_confirmada(cita_id):
    cita = Cita.get_cita(cita_id)
    return f"Cita reservada correctamente, ID: {cita.id_cita}"

@app.route('/cita_rechazada')
def cita_rechazada():
    return "No se pudo reservar la cita, por favor intente nuevamente"
