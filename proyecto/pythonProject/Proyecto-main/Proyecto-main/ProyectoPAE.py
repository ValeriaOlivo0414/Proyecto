import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from tabulate import tabulate
from datetime import datetime

# Clase del Código 2 para la segunda ventana
class SecondWindow(tk.Toplevel):
    def __init__(self, db_connector):
        super()._init_()
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

        # Botón para marcar acciones como "No reclamado"
        self.mark_no_reclamado_button = ttk.Button(date_frame, text="Finalizar Listado", command=self.handle_mark_no_reclamado)
        self.mark_no_reclamado_button.grid(row=2, column=0, padx=5, pady=5)

        # Treeview para mostrar resultados del estudiante y la fecha
        tree_frame = tk.Frame(main_frame)
        tree_frame.grid(row=2, column=0, sticky="nsew", pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("Documento", "Nombres", "Apellidos", "Grado", "Acción", "Fecha"),
                                 show="headings")
        self.tree.heading("Documento", text="Documento")
        self.tree.heading("Nombres", text="Nombres")
        self.tree.heading("Apellidos", text="Apellidos")
        self.tree.heading("Grado", text="Grado")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Acción", text="Acción")
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
            messagebox.showwarning("Advertencia", "El código de barras debe ser tu Documento de Identidad")
            return

        # Ejecutar el procedimiento almacenado con el código de barras y la fecha ingresada
        results = self.db_connector.execute_procedure('FuncionEstudiantesAction', barcode)

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

        # Ejecutar el procedimiento para filtrar solo por la fecha y ordenar los resultados
        results = self.db_connector.execute_procedure('FuncionEstudiantesActionByDate', action_date)

        if results:
            for headers, rows in results:
                self.display_results(headers, rows)
        else:
            messagebox.showinfo("Información", "No se encontraron resultados de esta fecha")

    def handle_mark_no_reclamado(self):
        """Este método marca las acciones faltantes como 'No reclamado'"""
        action_date = self.date_entry.get() or datetime.now().strftime('%Y-%m-%d')

        # Validar si se ingresó una fecha en el formato correcto
        try:
            datetime.strptime(action_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Advertencia", "La fecha debe tener el formato YYYY-MM-DD")
            return

        # Ejecutar el procedimiento para marcar las acciones como no reclamadas
        self.db_connector.execute_procedure('MarcarNoReclamado', action_date)

        # Informar al usuario que las acciones se han marcado como "No reclamado"
        messagebox.showinfo("Información", "Las acciones faltantes han sido marcadas como 'No reclamado'")

    def display_results(self, headers, rows):
        # Limpiar el TreeView antes de mostrar nuevos resultados
        self.tree.delete(*self.tree.get_children())

        for row in rows:
            self.tree.insert("", "end", values=row)

# Clase del Código 1 (modificada)
class Lista(tk.Tk):
    def __init__(self, db_connector):
        super().__init__()
        self.db_connector = db_connector
        self.title("Datos Estudiantes")
        self.geometry("1000x800")

        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame información del estudiante
        info_frame = tk.LabelFrame(main_frame, text="Información del Estudiante", padx=10, pady=10)
        info_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.fields = ['Documento', 'Nombres', 'Apellidos', 'Grado']
        self.entries = {}

        for i, field in enumerate(self.fields):
            ttk.Label(info_frame, text=field).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            entry = ttk.Entry(info_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[field] = entry

        # Frame de botones CRUD
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=10)

        ttk.Button(button_frame, text="Buscar", command=self.search_estudiante).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Insertar", command=self.insert_estudiante).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=self.update_estudiante).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Borrar", command=self.delete_estudiante).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Mostrar Todos", command=self.show_all_estudiante).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_fields).pack(side=tk.LEFT, padx=5)

        # Botón para abrir la segunda ventana
        ttk.Button(button_frame, text="Escáner", command=self.open_second_window).pack(side=tk.LEFT, padx=5)

        # Treeview para mostrar estudiantes
        tree_frame = tk.Frame(main_frame)
        tree_frame.grid(row=2, column=0, sticky="nsew", pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("Documento", "Nombres", "Apellidos", "Grado"),
                                 show="headings")
        self.tree.heading("Documento", text="Documento")
        self.tree.heading("Nombres", text="Nombres")
        self.tree.heading("Apellidos", text="Apellidos")
        self.tree.heading("Grado", text="Grado")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configurar expansión de filas y columnas
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

    def search_estudiante(self):
        Documento = self.entries['Documento'].get()
        if not Documento:
            messagebox.showwarning("Advertencia", "Por favor, ingrese el Documento para realizar la búsqueda")
            return
        result = self.db_connector.execute_procedure('BuscarEstudiante', Documento)
        if result:
            self.display_results(result[0][0], result[0][1])
        else:
            messagebox.showinfo("Información", "No se encontró ningún estudiante con ese Documento")

    def insert_estudiante(self):
        values = {field: self.entries[field].get() for field in self.fields}
        if not all(values.values()):
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos para insertar")
            return
        self.db_connector.execute_procedure('CrearEstudiante', *values.values())
        messagebox.showinfo("Información", "Estudiante insertado correctamente")
        self.clear_fields()
        self.show_all_estudiante()

    def update_estudiante(self):
        values = {field: self.entries[field].get() for field in self.fields}
        if not all(values.values()):
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos para actualizar")
            return
        self.db_connector.execute_procedure('ActualizarEstudiante', *values.values())
        messagebox.showinfo("Información", "Estudiante actualizado correctamente")
        self.clear_fields()
        self.show_all_estudiante()

    def delete_estudiante(self):
        Documento = self.entries['Documento'].get()
        if not Documento:
            messagebox.showwarning("Advertencia", "Por favor, ingrese el Documento para eliminar")
            return
        self.db_connector.execute_procedure('EliminarEstudiante', Documento)
        messagebox.showinfo("Información", "Estudiante eliminado correctamente")
        self.clear_fields()
        self.show_all_estudiante()

    def show_all_estudiante(self):
        result = self.db_connector.execute_procedure('verEstudiantes')
        if result:
            self.display_results(result[0][0], result[0][1])

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def display_results(self, headers, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)

    def open_second_window(self):
        """Este método abre la segunda ventana"""
        second_window = SecondWindow(self.db_connector)
        second_window.grab_set()  # Bloquea la ventana principal hasta cerrar la segunda

# Ejemplo de la clase DBConnector para ejecutar procedimientos almacenados
class DBConnector:
    def _init_(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def execute_procedure(self, procedure_name, *args):
        try:
            self.cursor.callproc(procedure_name, args)
            results = []
            for result in self.cursor.stored_results():
                rows = result.fetchall()
                headers = result.column_names
                results.append((headers, rows))
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            self.connection.commit()

# Ejemplo de cómo iniciar la aplicación principal
if _name_ == "_main_":
    db_connector = DBConnector('localhost', 'root', '', 'sistemapae')
    app = Lista(db_connector)
    app.mainloop()
