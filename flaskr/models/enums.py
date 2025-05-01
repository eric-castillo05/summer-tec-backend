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


class NotificacionesEnum(enum.Enum):
    NUEVO_GRUPO = "NUEVO_GRUPO"
    GRUPO_CANCELADO = "GRUPO_CANCELADO"
    GRUPO_LLENO = "GRUPO_LLENO"
    GRUPO_ACTUALIZADO = "GRUPO_ACTUALIZADO"
    GRUPO_APROBADO = "GRUPO_APROBADO"
