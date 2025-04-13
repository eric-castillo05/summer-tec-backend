import enum


class TurnoEnum(enum.Enum):
    MATUTINO = "MAT"
    VESPERTINO = "VES"


class StatusEnum(enum.Enum):
    PENDIENTE = "PENDIENTE"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"


class RolesEnum(enum.Enum):
    ADMIN = "ADMIN"
    ESTUDIANTE = "ESTUDIANTE"
    COORDINADOR = "COORDINADOR"


class DiaSemanaEnum(enum.Enum):
    LUNES = "LUNES"
    MARTES = "MARTES"
    MIERCOLES = "MIERCOLES"
    JUEVES = "JUEVES"
    VIERNES = "VIERNES"
    SABADO = "SABADO"