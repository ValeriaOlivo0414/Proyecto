from app.models.evento_alimenticio import EventoAlimenticio

class EventoAlimenticioController:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def ver_evento_alimenticio(self, id_evento):
        results = self.db_connector.execute_procedure('verEventoAlimenticio', id_evento)
        if results and results[0][1]:
            data = results[0][1][0]
            return EventoAlimenticio(data[0], data[1], data[2], data[3], data[4])
        return None

    def crear_evento_alimenticio(self, evento):
        results = self.db_connector.execute_procedure('CrearEventoAlimenticio',
                                                      evento.id_evento,
                                                      evento.documento,
                                                      evento.fecha,
                                                      evento.hora,
                                                      evento.tipo_evento)
        return results is not None

    def actualizar_evento_alimenticio(self, evento):
        results = self.db_connector.execute_procedure('ActualizarEventoAlimenticio',
                                                      evento.id_evento,
                                                      evento.documento,
                                                      evento.fecha,
                                                      evento.hora,
                                                      evento.tipo_evento)
        return results is not None

    def eliminar_evento_alimenticio(self, id_evento):
        results = self.db_connector.execute_procedure('EliminarEventoAlimenticio', id_evento)
        return results is not None