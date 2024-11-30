from datetime import date

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