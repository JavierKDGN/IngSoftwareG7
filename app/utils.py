from datetime import date
from app.models import Especialidad, BloqueHorario

def parse_fecha(fecha):
    """
    Convierte una entrada en formato string 'YYYY-MM-DD' o un objeto datetime.date
    al formato datetime.date. Si la entrada ya es datetime.date, la retorna directamente.

    :param fecha_input: Puede ser un string 'YYYY-MM-DD' o un objeto datetime.date.
    :return: Un objeto datetime.date.
    :raises ValueError: Si el formato del string no es válido o si el tipo de entrada es incorrecto.
    """

    if isinstance(fecha, date):
        return fecha

    if isinstance(fecha, str):
        try:
            return date.fromisoformat(fecha)
        except ValueError:
            raise ValueError(f'Formato de fecha incorrecto. Formato esperado: YYYY-MM-DD. Fecha recibida: {fecha}')

    raise TypeError(f"Tipo de entrada inválido: {type(fecha)}. Debe ser str o datetime.date.")

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
        #Si se le pasa como BloqueHorario.BloqueX de la pagina
        try:
            bloque = bloque.replace("BloqueHorario.","").upper()
            return BloqueHorario[bloque]
        except KeyError:
            raise ValueError(f'Bloque horario no válido: {bloque}. Los bloques válidos son: {", ".join([b.name for b in BloqueHorario])}')
    elif isinstance(bloque, int):
        try:
            return BloqueHorario(bloque)
        except ValueError:
            raise ValueError(f'Bloque horario no válido: {bloque}. Los bloques válidos son: {", ".join([b.name for b in BloqueHorario])}')
    else:
        raise TypeError(f"Tipo de entrada inválido: {type(bloque)}. Debe ser str o BloqueHorario.")

def rango_horario_bloque(bloque_num):
    bloque_num = bloque_num.value if isinstance(bloque_num, BloqueHorario) else bloque_num
    hora_inicio = 9 + (bloque_num - 1) // 2
    minuto_inicio = 30 * ((bloque_num - 1) % 2)
    hora_fin = 9 + bloque_num // 2
    minuto_fin = 30 * (bloque_num % 2)

    return f"{hora_inicio:02}:{minuto_inicio:02}-{hora_fin:02}:{minuto_fin:02}"