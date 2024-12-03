import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import Paciente, Medico, Horario, Cita
import app.services.db_helper as dbh
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'Paciente': Paciente, 'Medico': Medico, 'Horario': Horario, 'Cita': Cita}

