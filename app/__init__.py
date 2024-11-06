from flask import Flask
from config import Config

#Corre la aplicacion flask
app = Flask(__name__)

#Carga la configuracion de la aplicacion
app.config.from_object(Config)

# import debe estar abajo para evitar conflictos circulares ya que routes importa app
from app import routes