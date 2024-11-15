from datetime import date
from app.models import Paciente, Medico, Cita, Horario, BloqueHorario, EstadoCita
from user_story.db_helper import verificar_paciente_existente, verificar_medico_existente, crear_paciente_y_medico
from app import app, db

class HorarioMedico:

    def __revisar_bloques_ocupados_en_fecha(self, fecha, id_medico):
        bloques_ocupados = Horario.query.filter_by(fecha=fecha, id_medico=id_medico).all()
        return bloques_ocupados

    def mostrar_horario_medico_en_fecha(self, fecha, id_medico):
        fecha = date.fromisoformat(fecha)
        bloques_ocupados = self.__revisar_bloques_ocupados_en_fecha(fecha, id_medico)
        bloques_ocupados = [bloque.bloque for bloque in bloques_ocupados]
        bloques_disponibles = [bloque for bloque in BloqueHorario if bloque not in bloques_ocupados]
        return bloques_disponibles