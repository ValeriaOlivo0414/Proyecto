from datetime import date, time

class EventoAlimenticio:
    def __init__(self, id_evento, documento, fecha, hora, tipo_evento):
        self.id_evento = id_evento
        self.documento = documento
        self.fecha = fecha
        self.hora = hora
        self.tipo_evento = tipo_evento

    def __str__(self):
        return f"Evento {self.id_evento}: {self.tipo_evento} - Estudiante {self.documento} el {self.fecha} a las {self.hora}"