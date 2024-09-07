import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
import logging

logging.basicConfig(level=logging.DEBUG)


class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor(dictionary=True)
            logging.info("Conexión establecida a la base de datos")
        except Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            messagebox.showerror("Error de conexión", f"Error al conectar a la base de datos: {e}")

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            logging.info("Conexión cerrada")

    def execute_query(self, query, params=None):
        try:
            logging.debug(f"Ejecutando query: {query}")
            logging.debug(f"Parámetros: {params}")
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            if self.cursor.with_rows:
                result = self.cursor.fetchall()
            else:
                result = []

            self.connection.commit()
            logging.debug(f"Resultado: {result}")
            return result
        except Error as e:
            logging.error(f"Error al ejecutar la consulta: {e}")
            messagebox.showerror("Error", f"Error al ejecutar la consulta: {e}")
            return None

    def call_procedure(self, proc_name, params=None):
        try:
            logging.debug(f"Llamando al procedimiento: {proc_name}")
            logging.debug(f"Parámetros: {params}")
            if params:
                self.cursor.callproc(proc_name, params)
            else:
                self.cursor.callproc(proc_name)

            self.connection.commit()

            results = []
            for result in self.cursor.stored_results():
                results.extend(result.fetchall())

            logging.debug(f"Resultado del procedimiento: {results}")
            return results
        except Error as e:
            logging.error(f"Error al llamar al procedimiento almacenado: {e}")
            messagebox.showerror("Error", f"Error al llamar al procedimiento almacenado: {e}")
            return None