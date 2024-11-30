from app import app
from app.routes import especialistas
from app.services import db_helper
from app.models import Cita, Medico, Especialidad

def test_historial_citas(id_paciente):
    historial= Cita.get_citas_por_paciente(id_paciente)
    for cita in historial:
        print(f"- Cita ID: {cita.id_cita}")
        print(f"  Estado: {cita.estado.name}")
        print(f"  Médico: {cita.medico.nombre} {cita.medico.apellido} - {cita.medico.especialidad}")
        print(f"  Fecha: {cita.horario.fecha}")
        print(f"  Bloque Horario: {cita.horario.bloque.name}")
        print("-" * 30)

if __name__ == '__main__':
    with app.app_context():
        print(Medico.get_all_medicos())
        medicos = Medico.get_medico_por_especialidad(Especialidad.CARDIOLOGIA)
        for medico in medicos:
            db_helper.ocupar_todos_los_bloques(medico.id_medico, '2024-11-07')
            if not Medico.is_disponible_en_fecha("2024-11-07", medico.id_medico):
                print(f"El médico {medico.nombre} {medico.apellido} no está disponible el 7 de noviembre")
                especialidad = medico.especialidad
                print(f"Buscando especialistas en {especialidad}")
                especialistas = Medico.get_medico_por_especialidad(especialidad)
                for especialista in especialistas:
                    print(f"ID: {especialista.id_medico}, Nombre: {especialista.nombre} {especialista.apellido}, Teléfono: {especialista.telefono}")

