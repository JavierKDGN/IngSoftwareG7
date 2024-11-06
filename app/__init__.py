from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Inicializar flask y configuracion
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar base de datos y migraciones (en caso de modificar la estructura)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# import debe estar abajo para evitar conflictos circulares ya que routes importa app
from app import routes, models