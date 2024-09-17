from datetime import datetime

class EstudianteAction:
    def __init__(self, action_id, documento, nombres, apellidos, grado, action_time, action, consult_date):
        self.action_id = action_id
        self.documento = documento
        self.nombres = nombres
        self.apellidos = apellidos
        self.grado = grado
        self.action_time = action_time
        self.action = action
        self.consult_date = consult_date

    def __str__(self):
        return f"Acción {self.action_id}: {self.action} - Estudiante {self.nombres} {self.apellidos} el {self.consult_date}"