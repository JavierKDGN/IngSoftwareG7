from flask import render_template
from app import app

# Este archivo define las rutas de la aplicacion
# se utilizan los decoradores @app.route('/')
# para definir las rutas, y el comportamiento
# de la pagina (lo que se mostrara y renderizara en html)

# decoradores para definir las rutas
#ej de ruta localhost:5000/ mostrara el mensaje Hello!
@app.route('/')
def hello_world():
    return 'Hello!'

@app.route('/test')
def test():
    user = {'username': 'Paciente'}
    return render_template('test.html', title='Test', user=user)

