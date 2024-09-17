import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime  # Para obtener la fecha actual y filtrar


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
            self.cursor = self.connection.cursor()
            print("Conexión establecida a la base de datos")
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            messagebox.showerror("Error de conexión", f"Error al conectar a la base de datos: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")

    def execute_procedure(self, procedure_name, *args):
        try:
            self.cursor.callproc(procedure_name, args)
            results = []
            for result in self.cursor.stored_results():
                rows = result.fetchall()
                if rows:
                    headers = [i[0] for i in result.description]
                    results.append((headers, rows))
            self.connection.commit()
            return results
        except mysql.connector.Error as e:
            self.connection.rollback()
            print(f"Error al ejecutar el procedimiento {procedure_name}: {e}")
            messagebox.showerror("Error", f"Error al ejecutar el procedimiento {procedure_name}: {e}")
            return None


class Lista(tk.Tk):
    def __init__(self, db_connector):
        super().__init__()
        self.db_connector = db_connector
        self.title("Lectura con Código de Barras")
        self.geometry("1000x600")

        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Campo para el código de barras
        barcode_frame = tk.LabelFrame(main_frame, text="Escanear Código de Barras", padx=10, pady=10)
        barcode_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.barcode_entry = ttk.Entry(barcode_frame, width=40)
        self.barcode_entry.grid(row=0, column=0, padx=5, pady=5)
        self.barcode_entry.bind("<Return>", self.handle_barcode_scan)  # Se activa al presionar "Enter"

        # Campo para ingresar la fecha
        date_frame = tk.LabelFrame(main_frame, text="Filtrar por Fecha (YYYY-MM-DD)", padx=10, pady=10)
        date_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.date_entry = ttk.Entry(date_frame, width=40)
        self.date_entry.grid(row=0, column=0, padx=5, pady=5)

        # Botón para filtrar por fecha
        self.search_button = ttk.Button(date_frame, text="Buscar por Fecha", command=self.handle_date_search)
        self.search_button.grid(row=1, column=0, padx=5, pady=5)

        # Treeview para mostrar resultados del estudiante y la fecha
        tree_frame = tk.Frame(main_frame)
        tree_frame.grid(row=2, column=0, sticky="nsew", pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("Documento", "Nombres", "Apellidos", "Grado", "Acción", "Fecha"),
                                 show="headings")
        self.tree.heading("Documento", text="Documento")
        self.tree.heading("Nombres", text="Nombres")
        self.tree.heading("Apellidos", text="Apellidos")
        self.tree.heading("Grado", text="Grado")
        self.tree.heading("Acción", text="Acción")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configurar expansión de filas y columnas
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

    def handle_barcode_scan(self, event):
        """Este método maneja la lectura del código de barras"""
        barcode = self.barcode_entry.get()
        action_date = self.date_entry.get() or datetime.now().strftime(
            '%Y-%m-%d')  # Tomar la fecha actual si no se ingresa

        if not barcode.isdigit():
            messagebox.showwarning("Advertencia", "El código de barras debe ser numérico")
            return

        # Ejecutar el procedimiento almacenado con el código de barras y la fecha ingresada
        results = self.db_connector.execute_procedure('FuncionEstudiantesAction', barcode, action_date)

        if results:
            for headers, rows in results:
                self.display_results(headers, rows)
        else:
            messagebox.showinfo("Información", "No se encontraron resultados para este código en la fecha seleccionada")

        # Limpiar el campo de entrada para el siguiente código de barras
        self.barcode_entry.delete(0, tk.END)

    def handle_date_search(self):
        """Este método filtra las acciones por la fecha ingresada manualmente"""
        action_date = self.date_entry.get()

        # Validar si se ingresó una fecha en el formato correcto
        try:
            datetime.strptime(action_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Advertencia", "La fecha debe tener el formato YYYY-MM-DD")
            return

        # Ejecutar el procedimiento para filtrar solo por la fecha
        results = self.db_connector.execute_procedure('FuncionEstudiantesActionByDate', action_date)

        if results:
            for headers, rows in results:
                self.display_results(headers, rows)
        else:
            messagebox.showinfo("Información", "No se encontraron resultados para la fecha seleccionada")

    def display_results(self, headers, rows):
        # Limpiar el TreeView antes de mostrar nuevos resultados
        self.tree.delete(*self.tree.get_children())

        for row in rows:
            self.tree.insert("", "end", values=row)


# Configuración de la base de datos
user = 'root'
password = '1234'
host = 'localhost'
database = 'sistemapae'

# Crear y conectar a la base de datos
db_connector = DatabaseConnector(host, user, password, database)
db_connector.connect()

# Crear y ejecutar la aplicación
app = Lista(db_connector)
app.mainloop()

# Cerrar la conexión a la base de datos al cerrar la aplicación
db_connector.disconnect()