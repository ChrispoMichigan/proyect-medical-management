'''
#! Dependencias
#* pip install requests
'''
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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
    
    #conexion 1, crear paciente, CREO que esto ya deberia funcionar 
    def create_patient(self, patient_data):
        try:
            response = requests.post(
                f"{self.base_url}/api/createPatient",
                json=patient_data,
                headers={'Content-Type': 'application/json'}
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    #conexion 2, obtener siguiente paciente
    def get_next_patient(self):
        print("eldiablo")
    #conexion 3, obtener la cola de espera 
    def get_waiting_queue(self):
        print("ola c:")
    
    #conexion 4, obtener historial 
    def get_history(self):
        print("")
    
    

# Crear ventana principal
root = tk.Tk()
root.title("Sistema de Gestión de Atención Médica")
root.geometry("850x850")
root.resizable(False, False)

# Inicializar cliente API
api_client = APIClient()

# Variables globales
paciente_var = tk.StringVar()
fecha_var = tk.StringVar()
departamento_var = tk.StringVar(value="general")
busqueda_var = tk.StringVar()
edad_var = tk.StringVar()

# Función para obtener fecha actual
def obtener_fecha_actual():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Establecer fecha actual al iniciar el programa
fecha_var.set(obtener_fecha_actual())

# Función para registrar paciente
def registrar_paciente():
    if not paciente_var.get():
        messagebox.showwarning("Error", "Por favor ingrese el nombre del paciente")
        return
    
    if not edad_var.get():
        messagebox.showwarning("Error", "Por favor ingrese la edad del paciente")
        return
    
    try:
        edad = int(edad_var.get())
        if edad < 0 :
             messagebox.showwarning("Error", "la edad no puede ser menor a 0")
             return
    except ValueError:
        messagebox.showwarning("Error", "La edad debe ser un número válido")
        return
    
    patient_data = {
        "patient": {
            "name": paciente_var.get(),
            "edad": edad,
            "department": departamento_var.get(),
            "fecha_registro": fecha_var.get()
        }
    }
    
    response = api_client.create_patient(patient_data)
    
    if "error" in response:
        messagebox.showerror("Error", f"No se pudo registrar el paciente: {response['error']}")
    else:
        messagebox.showinfo("Éxito", "Paciente registrado correctamente")
        # Limpiar campos
        paciente_var.set("")
        edad_var.set("")
        # Actualizar vistas
        actualizar_vistas_departamentos()
        actualizar_estadisticas()

# Función para atender siguiente paciente
def atender_siguiente_paciente():
    print("")
# Función para ver próximo paciente
def ver_proximo_paciente():
    print("")

# Función para ver cola de espera
def ver_cola_espera():
    print("")
# Función para buscar paciente
def buscar_paciente():
    busqueda = busqueda_var.get()
    if not busqueda:
        messagebox.showwarning("Error", "ingrese el nombre a buscar")
        return
    

# Función para ver historial
def ver_historial():
    print("")
# Función para actualizar las vistas de departamentos
def actualizar_vistas_departamentos():
    print("")

# Función para actualizar estadísticas
def actualizar_estadisticas():
    print("")

# Función para generar reporte
def generar_reporte():
    print("")

# Interfaz gráfica
titulo = ttk.Label(root, text="Sistema de Gestión Médica", font=("Arial", 16))
titulo.place(x=100, y=20)

# Registros
ttk.Label(root, text="Registro de Pacientes", font=("Arial", 12)).place(x=20, y=60)

ttk.Label(root, text="Nombre del Paciente:").place(x=20, y=100)
ttk.Entry(root, textvariable=paciente_var, width=30).place(x=150, y=100)

ttk.Label(root, text="Edad:").place(x=20, y=130)
ttk.Entry(root, textvariable=edad_var, width=30).place(x=150, y=130)

ttk.Label(root, text="Fecha y Hora:").place(x=20, y=160)
ttk.Entry(root, textvariable=fecha_var, width=30).place(x=150, y=160)

ttk.Label(root, text="Departamento:").place(x=20, y=190)
departamento_combo = ttk.Combobox(root, textvariable=departamento_var,values=["urgencia", "general", "diagnostico"], state="readonly")
departamento_combo.place(x=150, y=190)

# Botones de registro
ttk.Button(root, text="Registrar", width=15, command=registrar_paciente).place(x=150, y=220)
ttk.Button(root, text="Fecha Actual", width=15, command=lambda: fecha_var.set(obtener_fecha_actual())).place(x=280, y=220)

# Gestión de atención
ttk.Label(root, text="Gestión de Atención", font=("Arial", 12)).place(x=20, y=270)

ttk.Button(root, text="Atender siguiente paciente", command=atender_siguiente_paciente).place(x=20, y=300)
ttk.Button(root, text="Ver próximo paciente", width=20, command=ver_proximo_paciente).place(x=190, y=300)
ttk.Button(root, text="Ver cola de espera", width=20, command=ver_cola_espera).place(x=350, y=300)

# Departamentos
ttk.Label(root, text="Departamentos médicos", font=("Arial", 12)).place(x=20, y=350)

# Crear pestañas para diferentes departamentos
notebook = ttk.Notebook(root)
notebook.place(x=20, y=380, width=760, height=200)

# Pestaña Urgencia
urgencia_frame = ttk.Frame(notebook, padding="10")
notebook.add(urgencia_frame, text="Urgencia")

urgencia_tree = ttk.Treeview(urgencia_frame, columns=("Paciente", "Fecha", "Departamento"), 
                            show="headings", height=8)
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

general_tree = ttk.Treeview(general_frame, columns=("Paciente", "Fecha", "Departamento"), 
                           show="headings", height=8)
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

# Estadísticas
ttk.Label(root, text="Estadísticas y Reportes", font=("Arial", 12)).place(x=20, y=590)

ttk.Label(root, text="Pacientes en espera:").place(x=20, y=620)
pacientes_en_espera_label = ttk.Label(root, text="0")
pacientes_en_espera_label.place(x=150, y=620)

ttk.Label(root, text="Tiempo promedio de espera:").place(x=200, y=620)
tiempo_espera_label = ttk.Label(root, text="0 min")
tiempo_espera_label.place(x=360, y=620)

ttk.Button(root, text="Generar Reporte de Eficiencia", command=generar_reporte).place(x=20, y=650)

# Búsqueda y gestión
ttk.Label(root, text="Búsqueda y Gestión", font=("Arial", 12)).place(x=20, y=700)

ttk.Label(root, text="Buscar Paciente:").place(x=20, y=730)
ttk.Entry(root, textvariable=busqueda_var, width=30).place(x=130, y=730)
ttk.Button(root, text="Buscar", width=15, command=buscar_paciente).place(x=350, y=730)
ttk.Button(root, text="Ver Historial", width=15, command=ver_historial).place(x=60, y=770)
ttk.Button(root, text="Salir", width=15, command=root.quit).place(x=260, y=770)



# Ejecutar la aplicación
root.mainloop()