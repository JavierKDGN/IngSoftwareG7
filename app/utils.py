from datetime import date
from app.models import Especialidad, BloqueHorario

def parse_fecha(fecha):
    """
    Convierte una entrada en formato string 'YYYY-MM-DD' o un objeto datetime.date
    al formato datetime.date. Si la entrada ya es datetime.date, la retorna directamente.

    :param fecha_input: Puede ser un string 'YYYY-MM-DD' o un objeto datetime.date.
    :return: Un objeto datetime.date.
    :raises ValueError: Si el formato del string no es valido o si el tipo de entrada es incorrecto.
    """

    if isinstance(fecha, date):
        return fecha

    if isinstance(fecha, str):
        try:
            return date.fromisoformat(fecha)
        except ValueError:
            raise ValueError(f'Formato de fecha incorrecto. Formato esperado: YYYY-MM-DD. Fecha recibida: {fecha}')

    raise TypeError(f"Tipo de entrada invalido: {type(fecha)}. Debe ser str o datetime.date.")

def parse_especialidad(especialidad):
    if isinstance(especialidad, Especialidad):
        return especialidad
    elif isinstance(especialidad, str):
        try:
            return Especialidad[especialidad.upper()]
        except KeyError:
            raise ValueError(f'Especialidad no válida: {especialidad}. Las especialidades válidas son: {", ".join([e.name for e in Especialidad])}')

def parse_bloque(bloque):
    if isinstance(bloque, BloqueHorario):
        return bloque
    elif isinstance(bloque, str):
        #Si se le pasa como rango horario desde la pagina
        try:
            bloque = rango_horario_a_bloque(bloque)
            return bloque
        except KeyError:
            raise ValueError(f'Bloque horario no valido: {bloque}. Los bloques validos son: {", ".join([b.name for b in BloqueHorario])}')
    elif isinstance(bloque, int):
        try:
            return BloqueHorario(bloque)
        except ValueError:
            raise ValueError(f'Bloque horario no valido: {bloque}. Los bloques validos son: {", ".join([b.name for b in BloqueHorario])}')
    else:
        raise TypeError(f"Tipo de entrada invalido: {type(bloque)}. Debe ser str o BloqueHorario.")


#las siguientes funciones determinan el bloque segun la string, no se de que otra forma pasarlo entre las paginas
#y probablemente sea mal codigo pero funciona
def bloque_a_rango_horario(bloque_num):
    bloque_num = bloque_num.value if isinstance(bloque_num, BloqueHorario) else bloque_num
    hora_inicio = 9 + (bloque_num - 1) // 2
    minuto_inicio = 30 * ((bloque_num - 1) % 2)
    hora_fin = 9 + bloque_num // 2
    minuto_fin = 30 * (bloque_num % 2)

    return f"{hora_inicio:02}:{minuto_inicio:02}-{hora_fin:02}:{minuto_fin:02}"

def rango_horario_a_bloque(rango_horario):
    try:
        hora_inicio, hora_fin = rango_horario.split('-')
        # Convertir a minutos desde las 9:00
        inicio_minutos = int(hora_inicio.split(':')[0]) * 60 + int(hora_inicio.split(':')[1]) - 540  # 9:00 es 540 minutos
        fin_minutos = int(hora_fin.split(':')[0]) * 60 + int(hora_fin.split(':')[1]) - 540

        # Cada bloque tiene 30 minutos, por lo que calculamos el índice basado en el inicio
        bloque_num = inicio_minutos // 30 + 1
        return BloqueHorario(bloque_num)
    except Exception as e:
        raise ValueError(f'Rango horario no valido: {rango_horario}. Error: {e}')
