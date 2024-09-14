import sys
import os

# Añade el directorio raíz del proyecto al PYTHONPATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.database.connector import DatabaseConnector
from app.controllers.estudiante_controller import EstudianteController
from app.controllers.evento_alimenticio_controller import EventoAlimenticioController
from app.controllers.estudiante_action_controller import EstudianteActionController
from app.views.main_view import MainView
from config.config import DB_CONFIG

def main():
    # Inicializar la conexión a la base de datos
    db_connector = DatabaseConnector(**DB_CONFIG)
    db_connector.connect()

    # Inicializar controladores
    estudiante_controller = EstudianteController(db_connector)
    evento_alimenticio_controller = EventoAlimenticioController(db_connector)
    estudiante_action_controller = EstudianteActionController(db_connector)

    # Iniciar la interfaz principal
    app = MainView(estudiante_controller, estudiante_action_controller)
    app.mainloop()

    # Cerrar la conexión a la base de datos al cerrar la aplicación
    db_connector.disconnect()

if __name__ == "__main__":
    main()