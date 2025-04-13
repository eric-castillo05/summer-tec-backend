from flaskr.models import Docente


class DocenteService:
    def __init__(self):
        pass

    def get_all(self, clave_carrera):
        docentes = Docente.query.filter_by(clave_carrera=clave_carrera).all()

        return [
            {
                "id_docente": docente.id_docente,
                "nombre_completo": docente.nombre_completo,
                "email": docente.email,
                "clave_carrera": docente.clave_carrera
            } for docente in docentes
        ]