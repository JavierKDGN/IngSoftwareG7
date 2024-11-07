from typing import Optional
from datetime import date
from enum import Enum
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

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

    def __repr__(self):
        return (f'<Cita(id_cita={self.id_cita}, id_paciente={self.id_paciente}, '
                f'id_medico={self.id_medico}, id_horario={self.id_horario}, '
                f'estado={self.estado.name})>')