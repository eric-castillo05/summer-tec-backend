import enum


class TurnoEnum(enum.Enum):
    MATUTINO = "MAT"
    VESPERTINO = "VES"


class StatusEnum(enum.Enum):
    PENDIENTE = "PENDIENTE"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"