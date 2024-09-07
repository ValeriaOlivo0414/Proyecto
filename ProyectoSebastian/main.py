from database.connector import DatabaseConnector
from gui.main_window import MainWindow
import config
import logging

logging.basicConfig(level=logging.DEBUG)

def main():
    db_connector = None
    try:
        db_connector = DatabaseConnector(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        db_connector.connect()
        app = MainWindow(db_connector)
        app.mainloop()
    except Exception as e:
        logging.exception(f"Error al iniciar la aplicación: {e}")
    finally:
        if db_connector:
            db_connector.disconnect()

if __name__ == "__main__":
    main()