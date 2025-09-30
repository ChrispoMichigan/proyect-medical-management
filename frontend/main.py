'''
#! Dependencias
#* pip install requests
'''
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime
class APIClient:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
    
    def get_data(self):
        try:
            response = requests.get(f"{self.base_url}/api/data")
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def post_data(self, data):
        try:
            response = requests.post(
                f"{self.base_url}/api/data",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

# Crear ventana principal
root = tk.Tk()
root.title("Sistema de Gestión de Atención Médica")
root.geometry("850x850")
root.resizable(False, False)
# Variables de prueba globales
paciente_var = tk.StringVar()
fecha_var = tk.StringVar()
departamento_var = tk.StringVar(value="general")
busqueda_var = tk.StringVar()

# Función para obtener fecha actual
def obtener_fecha_actual():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Establecer fecha actual al iniciar el programa
fecha_var.set(obtener_fecha_actual())

titulo = ttk.Label(root, text="Sistema de Gestión Médica", font=("Arial", 16))
titulo.place(x=100, y=20)

# registros
ttk.Label(root, text="Registro de Pacientes", font=("Arial", 12)).place(x=20, y=60)

ttk.Label(root, text="Nombre del Paciente:").place(x=20, y=100)
ttk.Entry(root, textvariable=paciente_var, width=30).place(x=150, y=100)

ttk.Label(root, text="Fecha y Hora:").place(x=20, y=140)
ttk.Entry(root, textvariable=fecha_var, width=30).place(x=150, y=140)

ttk.Label(root, text="Departamento:").place(x=20, y=180)
departamento_combo = ttk.Combobox(root, textvariable=departamento_var,values=["urgencia", "general", "diagnostico"], state="readonly")
departamento_combo.place(x=150, y=180)

# Botones de registro
ttk.Button(root, text="Registrar", width=15).place(x=150, y=220)
ttk.Button(root, text="Fecha Actual", width=15, command=lambda: fecha_var.set(obtener_fecha_actual())).place(x=280, y=220)

# gestion de atencion
ttk.Label(root, text="Gestion de Atencion", font=("Arial", 12)).place(x=20, y=270)

ttk.Button(root, text="Atender siguiente paciente").place(x=20, y=300)
ttk.Button(root, text="Ver proximo paciente", width=20).place(x=190, y=300)
ttk.Button(root, text="Ver cola de espera", width=20).place(x=350, y=300)

# departamentos
ttk.Label(root, text="Departamentos medicos", font=("Arial", 12)).place(x=20, y=350)

# crear pestañas para diferentes departamentos
notebook = ttk.Notebook(root)
notebook.place(x=20, y=380, width=760, height=200)

# Pestaña Urgencia
urgencia_frame = ttk.Frame(notebook, padding="10")
notebook.add(urgencia_frame, text="Urgencia")

urgencia_tree = ttk.Treeview(urgencia_frame, columns=("Paciente", "Fecha", "Departamento"), show="headings", height=8)
urgencia_tree.heading("Paciente", text="Paciente")
urgencia_tree.heading("Fecha", text="Fecha de Registro")
urgencia_tree.heading("Departamento", text="Departamento")
urgencia_tree.column("Paciente", width=200)
urgencia_tree.column("Fecha", width=150)
urgencia_tree.column("Departamento", width=100)
urgencia_tree.pack(fill=tk.BOTH, expand=True)

# Pestaña General
general_frame = ttk.Frame(notebook, padding="10")
notebook.add(general_frame, text="General")

general_tree = ttk.Treeview(general_frame, columns=("Paciente", "Fecha", "Departamento"), show="headings", height=8)
general_tree.heading("Paciente", text="Paciente")
general_tree.heading("Fecha", text="Fecha de Registro")
general_tree.heading("Departamento", text="Departamento")
general_tree.column("Paciente", width=200)
general_tree.column("Fecha", width=150)
general_tree.column("Departamento", width=100)
general_tree.pack(fill=tk.BOTH, expand=True)

# Pestaña Diagnóstico
diagnostico_frame = ttk.Frame(notebook, padding="10")
notebook.add(diagnostico_frame, text="Diagnóstico")

diagnostico_tree = ttk.Treeview(diagnostico_frame, columns=("Paciente", "Fecha", "Departamento"), show="headings", height=8)
diagnostico_tree.heading("Paciente", text="Paciente")
diagnostico_tree.heading("Fecha", text="Fecha de Registro")
diagnostico_tree.heading("Departamento", text="Departamento")
diagnostico_tree.column("Paciente", width=200)
diagnostico_tree.column("Fecha", width=150)
diagnostico_tree.column("Departamento", width=100)
diagnostico_tree.pack(fill=tk.BOTH, expand=True)

# estadisticas
ttk.Label(root, text="Estadísticas y Reportes", font=("Arial", 12, )).place(x=20, y=590)

ttk.Label(root, text="Pacientes en espera:").place(x=20, y=620)
ttk.Label(root, text="0").place(x=150, y=620)

ttk.Label(root, text="Tiempo promedio de espera:").place(x=200, y=620)
ttk.Label(root, text="0 min").place(x=360, y=620)

ttk.Button(root, text="Generar Reporte de Eficiencia").place(x=20, y=650)

# busqueda y gestion
ttk.Label(root, text="Búsqueda y Gestión", font=("Arial", 12)).place(x=20, y=700)

ttk.Label(root, text="Buscar Paciente:").place(x=20, y=730)
ttk.Entry(root, textvariable=busqueda_var, width=30).place(x=130, y=730)
ttk.Button(root, text="Buscar", width=15).place(x=350, y=730)
ttk.Button(root, text="Ver Historial", width=15).place(x=60, y=770)
ttk.Button(root, text="Salir", width=15, command=root.quit).place(x=260, y=770)


# Ejecutar la aplicación
root.mainloop()