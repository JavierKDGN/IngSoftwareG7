from typing import Optional
from datetime import date
from enum import Enum
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.utils import parse_fecha

class EstadoCita(Enum):
    AGENDADA = 1
    CONFIRMADA = 2
    REALIZADA = 3
    CANCELADA = 4
    NO_ASISTIO = 5

class BloqueHorario(Enum):
    BLOQUE_1 = 1  # 9:00 - 9:30
    BLOQUE_2 = 2  # 9:30 - 10:00
    BLOQUE_3 = 3  # 10:00 - 10:30
    BLOQUE_4 = 4  # 10:30 - 11:00
    BLOQUE_5 = 5  # 11:00 - 11:30
    BLOQUE_6 = 6  # 11:30 - 12:00
    BLOQUE_7 = 7  # 12:00 - 12:30
    BLOQUE_8 = 8  # 12:30 - 13:00
    BLOQUE_9 = 9  # 13:00 - 13:30
    BLOQUE_10 = 10  # 13:30 - 14:00
    BLOQUE_11 = 11  # 14:00 - 14:30
    BLOQUE_12 = 12  # 14:30 - 15:00
    BLOQUE_13 = 13  # 15:00 - 15:30
    BLOQUE_14 = 14  # 15:30 - 16:00
    BLOQUE_15 = 15  # 16:00 - 16:30
    BLOQUE_16 = 16  # 16:30 - 17:00
    BLOQUE_17 = 17  # 17:00 - 17:30
    BLOQUE_18 = 18  # 17:30 - 18:00

# Tabla Paciente
class Paciente(db.Model):
    id_paciente: so.Mapped[int] = so.mapped_column(primary_key=True)

    nombre: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    apellido: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    fecha_nacimiento: so.Mapped[Optional[date]] = so.mapped_column(nullable=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    telefono: so.Mapped[Optional[str]] = so.mapped_column(sa.String(15))

    @classmethod
    def get_paciente(cls, id_paciente):
        return cls.query.get(id_paciente)

    @classmethod
    def get_all_pacientes(cls):
        return cls.query.all()

    @classmethod
    def crear_paciente(cls, nombre, apellido, fecha_nacimiento, email, telefono):
        nuevo_paciente = cls(nombre=nombre, apellido=apellido, fecha_nacimiento=fecha_nacimiento, email=email, telefono=telefono)
        db.session.add(nuevo_paciente)
        db.session.commit()
        return nuevo_paciente

    def __repr__(self):
        return (f'<Paciente(id_paciente={self.id_paciente}, nombre={self.nombre}, '
                f'apellido={self.apellido}, fecha_nacimiento={self.fecha_nacimiento}, '
                f'email={self.email}, telefono={self.telefono})>')

# Tabla Medico
class Medico(db.Model):
    id_medico: so.Mapped[int] = so.mapped_column(primary_key=True)

    nombre: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    apellido: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    especialidad: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    telefono: so.Mapped[Optional[str]] = so.mapped_column(sa.String(15))

    @classmethod
    def get_medico(cls, id_medico):
        return cls.query.get(id_medico)

    @classmethod
    def get_all_medicos(cls):
        return cls.query.all()

    @classmethod
    def get_medico_por_especialidad(cls, especialidad):
        return cls.query.filter_by(especialidad=especialidad).all()

    @classmethod
    def is_disponible_en_fecha(cls, fecha, id_medico):
        bloques_disponibles = Horario.get_bloques_disp_en_fecha_de_medico(fecha, id_medico)
        return len(bloques_disponibles) > 0

    @classmethod
    def crear_medico(cls, nombre, apellido, especialidad, telefono):
        nuevo_medico = cls(nombre=nombre, apellido=apellido, especialidad=especialidad, telefono=telefono)
        db.session.add(nuevo_medico)
        db.session.commit()
        return nuevo_medico

    def __repr__(self):
        return (f'<Medico(id_medico={self.id_medico}, nombre={self.nombre}, apellido={self.apellido} '
                f'especialidad={self.especialidad}, telefono={self.telefono})>')

# Tabla Horario, cada entrada es un bloque en tal dia ocupado
# ej dia: 1 (lunes), bloque: 1 (9:00-9:30)
class Horario(db.Model):
    id_horario: so.Mapped[int] = so.mapped_column(primary_key=True)

    fecha: so.Mapped[date] = so.mapped_column(sa.Date, nullable=False)  # Ej: 2024-11-04
    bloque:so.Mapped[BloqueHorario] = so.mapped_column(sa.Enum(BloqueHorario), nullable=False)  # Ej: bloque 1 representa"9:00-9:30"

    id_medico: so.Mapped[int] = so.mapped_column(sa.ForeignKey('medico.id_medico'), nullable=False)
    medico: so.Mapped['Medico'] = so.relationship('Medico', backref='horarios_ocupados')

    @classmethod
    def get_bloque(cls, id_horario):
        return cls.query.get(id_horario)

    @classmethod
    def get_all_bloques(cls):
        return cls.query.all()

    @classmethod
    def get_bloque_ocupado(cls, fecha, bloque, id_medico):
        '''Retorna el bloque ocupado en una fecha por medico específico'''
        fecha = parse_fecha(fecha)
        return cls.query.filter_by(fecha=fecha, bloque=bloque, id_medico=id_medico).first()

    @classmethod
    def get_bloques_ocup_en_fecha_de_medico(cls, fecha, id_medico):
        '''Retorna los bloques ocupados en una fecha por medico específico'''
        fecha = parse_fecha(fecha)
        bloques = cls.query.join(Cita).filter(
            cls.fecha == fecha,
            cls.id_medico == id_medico,
            Cita.estado.in_([EstadoCita.AGENDADA, EstadoCita.CONFIRMADA, EstadoCita.REALIZADA])
        ).all()
        return bloques


    @classmethod
    def get_bloques_disp_en_fecha_de_medico(cls, fecha, id_medico):
        bloques_ocupados = cls.get_bloques_ocup_en_fecha_de_medico(fecha, id_medico)
        bloques_ocupados = [bloque.bloque for bloque in bloques_ocupados]
        bloques_disponibles = [bloque for bloque in BloqueHorario if bloque not in bloques_ocupados]
        return bloques_disponibles

    @classmethod
    def is_bloque_disponible(cls, fecha, bloque, id_medico):
        '''Retorna True si el bloque está disponible en la fecha para el medico'''
        fecha = parse_fecha(fecha)
        bloque_ocupado = cls.query.filter_by(fecha=fecha, bloque=bloque, id_medico=id_medico).first()
        return bloque_ocupado is None # True si esta disponible, False si ocupado

    @classmethod
    def crear_bloque_ocupado(cls, fecha, bloque, id_medico):
        fecha = parse_fecha(fecha)
        nuevo_bloque = cls(fecha=fecha, bloque=bloque, id_medico=id_medico)
        db.session.add(nuevo_bloque)
        db.session.commit()
        return nuevo_bloque

    def __repr__(self):
        return (f'<Horario(id_horario={self.id_horario}, id_medico={self.id_medico}, '
                f'fecha={self.fecha}, bloque={self.bloque.name})>')

# Tabla Cita
class Cita(db.Model):
    id_cita: so.Mapped[int] = so.mapped_column(primary_key=True)
    id_paciente: so.Mapped[int] = so.mapped_column(sa.ForeignKey('paciente.id_paciente'), nullable=False)
    id_medico: so.Mapped[int] = so.mapped_column(sa.ForeignKey('medico.id_medico'), nullable=False)
    id_horario: so.Mapped[int] = so.mapped_column(sa.ForeignKey('horario.id_horario'), nullable=False)

    estado: so.Mapped[EstadoCita] = so.mapped_column(sa.Enum(EstadoCita), default=EstadoCita.AGENDADA)  # Estados como "agendada", "cancelada", etc.

    paciente: so.Mapped['Paciente'] = so.relationship('Paciente', backref='citas')
    medico: so.Mapped['Medico'] = so.relationship('Medico', backref='citas')
    horario: so.Mapped['Horario'] = so.relationship('Horario', backref='citas')

    @classmethod
    def get_cita(cls, id_cita):
        return cls.query.get(id_cita)

    @classmethod
    def get_citas_por_horario(cls, id_horario):
        '''Retorna las cita asociada a un horario'''
        return cls.query.filter_by(id_horario=id_horario).all()

    @classmethod
    def get_citas_por_paciente(cls, id_paciente):
        '''Retorna las citas de un paciente'''
        return cls.query.filter_by(id_paciente=id_paciente).all()

    @classmethod
    def get_citas_por_medico(cls, id_medico):
        '''Retorna las citas de un medico'''
        return cls.query.filter_by(id_medico=id_medico).all()

    @classmethod
    def crear_cita(cls, id_paciente, id_medico, id_horario):
        nueva_cita = cls(id_paciente=id_paciente, id_medico=id_medico, id_horario=id_horario)
        db.session.add(nueva_cita)
        db.session.commit()
        return nueva_cita

    @classmethod
    def cancelar_cita(cls, id_cita):
        '''Cambia el estado de una cita a cancelada'''
        cita = cls.query.get(id_cita)
        if cita and cita.estado != EstadoCita.CANCELADA:
            cita.estado = EstadoCita.CANCELADA
            db.session.commit()
            return cita
        return None


    def __repr__(self):
        return (f'<Cita(id_cita={self.id_cita}, id_paciente={self.id_paciente}, '
                f'id_medico={self.id_medico}, id_horario={self.id_horario}, '
                f'estado={self.estado.name})>')