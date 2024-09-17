from app.models.estudiante_action import EstudianteAction

class EstudianteActionController:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def registrar_accion(self, documento):
        results = self.db_connector.execute_procedure('FuncionEstudiantesAction', documento)
        if results and results[0][1]:
            data = results[0][1][0]
            return EstudianteAction(None, data[0], data[1], data[2], data[3], None, data[4], data[5])
        return None