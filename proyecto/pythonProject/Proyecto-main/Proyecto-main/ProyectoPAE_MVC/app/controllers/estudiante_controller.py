from app.models.estudiante import Estudiante

class EstudianteController:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def buscar_estudiante(self, documento):
        results = self.db_connector.execute_procedure('BuscarEstudiante', documento)
        if results and results[0][1]:
            data = results[0][1][0]
            return Estudiante(data[0], data[1], data[2], data[3])
        return None

    def crear_estudiante(self, estudiante):
        results = self.db_connector.execute_procedure('CrearEstudiante',
                                                      estudiante.documento,
                                                      estudiante.nombres,
                                                      estudiante.apellidos,
                                                      estudiante.grado)
        return results is not None

    def actualizar_estudiante(self, estudiante):
        results = self.db_connector.execute_procedure('ActualizarEstudiante',
                                                      estudiante.documento,
                                                      estudiante.nombres,
                                                      estudiante.apellidos,
                                                      estudiante.grado)
        return results is not None

    def eliminar_estudiante(self, documento):
        results = self.db_connector.execute_procedure('EliminarEstudiante', documento)
        return results is not None

    def ver_estudiantes(self):
        results = self.db_connector.execute_procedure('verEstudiantes')
        estudiantes = []
        if results and results[0][1]:
            for data in results[0][1]:
                estudiantes.append(Estudiante(data[0], data[1], data[2], data[3]))
        return estudiantes