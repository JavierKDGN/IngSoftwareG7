from flask import render_template, redirect, url_for
from app import app

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
    especialistas_lista = [
        {'id': 1, 'nombre': 'Dr. Juan Pérez', 'especialidad': 'Cardiología', 'contacto': '934434221'},
        {'id': 2, 'nombre': 'Dra. Ana López', 'especialidad': 'Dermatología', 'contacto': '932435465'},
        {'id': 3, 'nombre': 'Dr. Carlos Sánchez', 'especialidad': 'Pediatría', 'contacto': '982736457'}
    ]
    return render_template('especialistas.html', especialistas=especialistas_lista)

@app.route('/centroayuda')
def centroayuda():
    return render_template('centroayuda.html')


