import enum


class TurnoEnum(enum.Enum):
    MATUTINO = "MAT"
    VESPERTINO = "VES"
    NOCTURNO = "NOC"


class StatusEnum(enum.Enum):
    PENDIENTE = "PENDIENTE"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"