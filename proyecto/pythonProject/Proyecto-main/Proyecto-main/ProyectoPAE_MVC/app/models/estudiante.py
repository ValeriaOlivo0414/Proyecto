class Estudiante:
    def __init__(self, documento, nombres, apellidos, grado):
        self.documento = documento
        self.nombres = nombres
        self.apellidos = apellidos
        self.grado = grado

    def __str__(self):
        return f"{self.nombres} {self.apellidos} (Documento: {self.documento}, Grado: {self.grado})"