import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox


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

        # Frame de botones CRUD
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=10)

        ttk.Button(button_frame, text="Buscar", command=self.search_estudiante).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Insertar", command=self.insert_estudiante).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=self.update_estudiante).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Borrar", command=self.delete_estudiante).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Mostrar Todos", command=self.show_all_estudiante).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_fields).pack(side=tk.LEFT, padx=5)

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
            messagebox.showwarning("Advertencia", "Por favor, ingrese Documento de estudiante")
            return

        results = self.db_connector.execute_procedure('BuscarEstudiante', Documento)
        if results:
            self.display_results(results)
        else:
            messagebox.showinfo("Información", "No se encontró el estudiante")

    def insert_estudiante(self):
        values = [self.entries[field].get() for field in self.fields[0:]]  # Excluimos Documento
        results = self.db_connector.execute_procedure('CrearEstudiante', *values)
        if results is not None:
            messagebox.showinfo("Éxito", "Estudiante insertado correctamente")
            self.clear_fields()
            self.show_all_estudiante()

    def update_estudiante(self):
        values = [self.entries[field].get() for field in self.fields]
        results = self.db_connector.execute_procedure('ActualizarEstudiante', *values)
        if results is not None:
            messagebox.showinfo("Éxito", "Estudiante actualizado correctamente")
            self.show_all_estudiante()

    def delete_estudiante(self):
        Documento = self.entries['Documento'].get()
        if not Documento:
            messagebox.showwarning("Advertencia", "Por favor, ingrese Documento de estudiante")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este estudiante?"):
            results = self.db_connector.execute_procedure('EliminarEstudiante', Documento)
            if results is not None:
                messagebox.showinfo("Éxito", "Estudiante eliminado correctamente")
                self.clear_fields()
                self.show_all_estudiante()

    def show_all_estudiante(self):
        results = self.db_connector.execute_procedure('verEstudiantes')
        if results:
            self.display_results(results)

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

class Lista(tk.Tk):
    def __init__(self, db_connector):
        super().__init__()
        self.db_connector = db_connector
        self.title("Datos Estudiantes - Lectura con Código de Barras")
        self.geometry("1000x800")

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

        # Treeview para mostrar resultados del estudiante
        tree_frame = tk.Frame(main_frame)
        tree_frame.grid(row=2, column=0, sticky="nsew", pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("Documento", "Nombres", "Apellidos", "Grado", "Acción"),
                                 show="headings")
        self.tree.heading("Documento", text="Documento")
        self.tree.heading("Nombres", text="Nombres")
        self.tree.heading("Apellidos", text="Apellidos")
        self.tree.heading("Grado", text="Grado")
        self.tree.heading("Acción", text="Acción")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configurar expansión de filas y columnas
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

    def handle_barcode_scan(self, event):
        """Este método maneja la lectura del código de barras"""
        barcode = self.barcode_entry.get()
        if not barcode.isdigit():
            messagebox.showwarning("Advertencia", "El código de barras debe ser numérico")
            return

        # Ejecutar el procedimiento almacenado con el código de barras (est_id)
        results = self.db_connector.execute_procedure('FuncionEstudiantesAction', barcode)

        if results:
            self.display_results(results)
        else:
            messagebox.showinfo("Información", "No se encontraron resultados para este código")

        # Limpiar el campo de entrada para el siguiente código de barras
        self.barcode_entry.delete(0, tk.END)

    def display_results(self, results):
        # Limpiar el TreeView antes de mostrar nuevos resultados
        self.tree.delete(*self.tree.get_children())

        for headers, rows in results:
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