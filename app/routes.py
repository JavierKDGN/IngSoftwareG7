from flask import render_template, redirect, url_for, request
from app import app
from app.models import *
from app.services.servicio_citas import reservar_cita_medica


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

@app.route('/reservar', methods=['GET', 'POST'])
def reservar_cita():
    especialidades = [e.name for e in Especialidad]
    medicos, fechas, bloques = None, None, None

    if request.method == 'POST':
        especialidad = request.form.get('especialidad')
        id_medico = request.form.get('medico')
        fecha = request.form.get('fecha')
        bloque = request.form.get('bloque')

        #Si se selecciona especialidad cargar medicos
        if especialidad and not id_medico:
            medicos = Medico.get_medico_por_especialidad(especialidad)

        #Si se selecciona medico cargar fechas
        elif id_medico and not fecha:
            dias_disponibles = 7
            fechas = Medico.get_fechas_disponibles_hasta_dias(id_medico, dias_disponibles)

        #Si se selecciona fecha cargar bloques
        elif fecha and not bloque:
            bloques = Horario.get_bloques_disp_en_fecha_de_medico(fecha, id_medico)

        #Si se selecciona bloque, reservar cita
        elif bloque:
            bloque = BloqueHorario(int(bloque))
            paciente_id = 1 #simular paciente
            cita = reservar_cita_medica(paciente_id, id_medico, fecha, bloque)
            if cita:
                return redirect(url_for('cita_confirmada', cita_id=cita.id_cita))
            else:
                return redirect(url_for('cita_rechazada'))

    return render_template('reservar_cita.html', especialidades=especialidades, medicos=medicos, fechas=fechas, bloques=bloques)

@app.route('/cita_confirmada/<cita_id>')
def cita_confirmada(cita_id):
    cita = Cita.get_cita_by_id(cita_id)
    return f"Cita reservada correctamente, ID: {cita.id_cita}"

@app.route('/cita_rechazada')
def cita_rechazada():
    return "No se pudo reservar la cita, por favor intente nuevamente"
