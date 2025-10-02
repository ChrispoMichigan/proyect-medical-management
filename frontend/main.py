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
            return {"status": False, "message": f"Error:{str(e)}"}
    
    def post_data(self, data):
        try:
            response = requests.post(
                f"{self.base_url}/api/data",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": False, "message": f"Error:{str(e)}"}
    
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
            return {"status": False, "message": f"Error:{str(e)}"}
    #conexion 2, obtener siguiente paciente
    def get_next_patient(self):
        try:
            response = requests.get(f"{self.base_url}/api/getNextPatient")
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": False, "message": f"Error:{str(e)}"}
    
    def attend_next_patient(self, patient_data):
        try:
            response = requests.post(
                f"{self.base_url}/api/attendPatient",
                json=patient_data,
                headers={'Content-Type': 'application/json'}
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": False, "message": f"Error:{str(e)}"}

    #conexion 4, obtener historial 
    def get_history(self):
        print("")

    def get_queue_data(self, department):
        """Obtiene los datos de la cola de un departamento específico"""
        try:
            response = requests.get(f"{self.base_url}/api/getQueue/{department}")
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": False, "message": f"Error: {str(e)}"}
    
    def get_number_of_patients(self):
        try:
            response = requests.get(f"{self.base_url}/api/patientsWaiting")
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": False, "message": f"Error: {str(e)}"}
        
    def get_stadistics(self):
        try:
            response = requests.get(f"{self.base_url}/api/averageTime")
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": False, "message": f"Error: {str(e)}"}


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
            "age": edad,
            "department": departamento_var.get(),
            "admission": fecha_var.get()
        }
    }
    
    response = api_client.create_patient(patient_data)
    
    if response['status']:
        messagebox.showinfo("Éxito", response['message'])
        # Limpiar campos
        paciente_var.set("")
        edad_var.set("")
        # Actualizar vistas
        actualizar_vistas_departamentos()
        actualizar_estadisticas()
    else:
        messagebox.showerror("Error", f"No se pudo registrar el paciente: {response['message']}")

# Función para atender siguiente paciente
def atender_siguiente_paciente():
    print("")

# Función para ver próximo paciente
def ver_proximo_paciente():
    global api_client
    
    try:
        response = api_client.get_next_patient()
        
        if response.get('status'):
            # Hay un paciente en cola
            patient_data = response.get('data', {}).get('patient', {})
            mostrar_ventana_proximo_paciente(patient_data, response.get('message', ''))
        else:
            # No hay pacientes en cola
            messagebox.showinfo(
                "Sin Pacientes", 
                response.get('message', 'No hay pacientes en cola en ningún departamento')
            )
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener próximo paciente: {str(e)}")

def mostrar_ventana_proximo_paciente(patient_data, message):
    """Muestra una ventana con la información detallada del próximo paciente"""
    
    # Crear ventana emergente
    ventana_paciente = tk.Toplevel(root)
    ventana_paciente.title("Próximo Paciente en Cola")
    ventana_paciente.geometry("450x400")
    ventana_paciente.resizable(False, False)
    ventana_paciente.configure(bg='#f0f0f0')
    
    # Centrar la ventana
    ventana_paciente.transient(root)
    ventana_paciente.grab_set()
    
    # Frame principal con padding
    main_frame = tk.Frame(ventana_paciente, bg='#f0f0f0', padx=20, pady=20)
    main_frame.pack(fill='both', expand=True)
    
    # Título de la ventana
    titulo_label = tk.Label(
        main_frame,
        text="PRÓXIMO PACIENTE",
        font=("Arial", 16, "bold"),
        bg='#f0f0f0',
        fg='#2c3e50'
    )
    titulo_label.pack(pady=(0, 10))
    
    # Mensaje del tipo de cola
    mensaje_label = tk.Label(
        main_frame,
        text=message,
        font=("Arial", 10),
        bg='#f0f0f0',
        fg='#7f8c8d',
        wraplength=400
    )
    mensaje_label.pack(pady=(0, 20))
    
    # Frame para la información del paciente
    info_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
    info_frame.pack(fill='x', pady=(0, 20))
    
    # Información del paciente
    info_padding = tk.Frame(info_frame, bg='white')
    info_padding.pack(fill='both', expand=True, padx=15, pady=15)
    
    # ID del paciente
    id_frame = tk.Frame(info_padding, bg='white')
    id_frame.pack(fill='x', pady=5)
    tk.Label(id_frame, text="ID:", font=("Arial", 10, "bold"), bg='white', fg='#34495e').pack(side='left')
    tk.Label(id_frame, text=str(patient_data.get('id', 'N/A')), font=("Arial", 10), bg='white', fg='#2c3e50').pack(side='left', padx=(10, 0))
    
    # Nombre del paciente
    nombre_frame = tk.Frame(info_padding, bg='white')
    nombre_frame.pack(fill='x', pady=5)
    tk.Label(nombre_frame, text="Nombre:", font=("Arial", 10, "bold"), bg='white', fg='#34495e').pack(side='left')
    tk.Label(nombre_frame, text=patient_data.get('name', 'N/A'), font=("Arial", 10), bg='white', fg='#2c3e50').pack(side='left', padx=(10, 0))
    
    # Edad del paciente
    edad_frame = tk.Frame(info_padding, bg='white')
    edad_frame.pack(fill='x', pady=5)
    tk.Label(edad_frame, text="Edad:", font=("Arial", 10, "bold"), bg='white', fg='#34495e').pack(side='left')
    tk.Label(edad_frame, text=f"{patient_data.get('age', 'N/A')} años", font=("Arial", 10), bg='white', fg='#2c3e50').pack(side='left', padx=(10, 0))
    
    # Departamento
    dept_frame = tk.Frame(info_padding, bg='white')
    dept_frame.pack(fill='x', pady=5)
    tk.Label(dept_frame, text="Departamento:", font=("Arial", 10, "bold"), bg='white', fg='#34495e').pack(side='left')
    
    # Color según el departamento
    dept_colors = {
        'urgencia': '#e74c3c',
        'general': '#3498db', 
        'diagnostico': '#f39c12'
    }
    dept_color = dept_colors.get(patient_data.get('department', '').lower(), '#95a5a6')
    
    tk.Label(
        dept_frame, 
        text=patient_data.get('department', 'N/A').title(), 
        font=("Arial", 10, "bold"), 
        bg='white', 
        fg=dept_color
    ).pack(side='left', padx=(10, 0))
    
    # Fecha de ingreso
    fecha_frame = tk.Frame(info_padding, bg='white')
    fecha_frame.pack(fill='x', pady=5)
    tk.Label(fecha_frame, text="Ingreso:", font=("Arial", 10, "bold"), bg='white', fg='#34495e').pack(side='left')
    
    # Formatear la fecha si está disponible
    fecha_ingreso = patient_data.get('admission', 'N/A')
    if fecha_ingreso != 'N/A':
        try:
            fecha_obj = datetime.strptime(fecha_ingreso, "%Y-%m-%d %H:%M:%S")
            fecha_formateada = fecha_obj.strftime("%d/%m/%Y %H:%M")
        except:
            fecha_formateada = fecha_ingreso
    else:
        fecha_formateada = 'N/A'
    
    tk.Label(fecha_frame, text=fecha_formateada, font=("Arial", 10), bg='white', fg='#2c3e50').pack(side='left', padx=(10, 0))
    
    # Tiempo de espera (si está disponible)
    if patient_data.get('waiting_time'):
        tiempo_frame = tk.Frame(info_padding, bg='white')
        tiempo_frame.pack(fill='x', pady=5)
        tk.Label(tiempo_frame, text="Tiempo de espera:", font=("Arial", 10, "bold"), bg='white', fg='#34495e').pack(side='left')
        tk.Label(tiempo_frame, text=patient_data.get('waiting_time', 'N/A'), font=("Arial", 10), bg='white', fg='#2c3e50').pack(side='left', padx=(10, 0))
    
    # Separador
    separator = tk.Frame(main_frame, height=2, bg='#bdc3c7')
    separator.pack(fill='x', pady=10)
    
    # Frame para los botones
    button_frame = tk.Frame(main_frame, bg='#f0f0f0')
    button_frame.pack(fill='x')
    
    # Botón para atender paciente
    atender_btn = tk.Button(
        button_frame,
        text="Atender Paciente",
        command=lambda: [ventana_paciente.destroy(), atender_paciente_actual(patient_data)],
        bg='#27ae60',
        fg='white',
        font=("Arial", 10, "bold"),
        padx=20,
        pady=8,
        relief='flat',
        cursor='hand2'
    )
    atender_btn.pack(side='left', padx=(0, 10))
    
    # Botón cerrar
    cerrar_btn = tk.Button(
        button_frame,
        text="Cerrar",
        command=ventana_paciente.destroy,
        bg='#95a5a6',
        fg='white',
        font=("Arial", 10, "bold"),
        padx=20,
        pady=8,
        relief='flat',
        cursor='hand2'
    )
    cerrar_btn.pack(side='right')
    
    # Centrar la ventana en la pantalla
    ventana_paciente.update_idletasks()
    width = ventana_paciente.winfo_width()
    height = ventana_paciente.winfo_height()
    x = (ventana_paciente.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana_paciente.winfo_screenheight() // 2) - (height // 2)
    ventana_paciente.geometry(f'{width}x{height}+{x}+{y}')

def atender_paciente_actual(patient_data):
    """Función para atender al paciente actual"""
    global api_client
    
    try:
        # Llamar al backend para atender al paciente
        response = api_client.attend_next_patient(patient_data)
        
        if response.get('status'):
            # Mostrar información completa
            patient_info = response.get('patient', {})
            waiting_time = response.get('waiting_time', 'No calculado')
            department = response.get('department', 'N/A')
            
            messagebox.showinfo(
                "Paciente Atendido Exitosamente",
                f"Paciente: {patient_info.get('name', 'N/A')}\n"
                f"Departamento: {department.title()}\n"
                f"Tiempo de espera: {waiting_time}\n"
                f"Hora de atención: {patient_info.get('egress', 'N/A')}\n\n"
                f"{response.get('message', 'Paciente atendido correctamente')}"
            )
            
            # Actualizar las vistas después de atender al paciente
            actualizar_vistas_departamentos()
            actualizar_estadisticas()
            
        else:
            # Error del backend
            messagebox.showerror(
                "Error al Atender Paciente",
                f"No se pudo atender al paciente:\n\n"
                f"{response.get('message', 'Error desconocido')}"
            )
    
    except Exception as e:
        # Error de conexión o excepción
        messagebox.showerror(
            "Error de Conexión",
            f"Error al conectar con el servidor:\n\n"
            f"{str(e)}\n\n"
        )

# Función para buscar paciente
def buscar_paciente():
    busqueda = busqueda_var.get()
    if not busqueda:
        messagebox.showwarning("Error", "ingrese el nombre a buscar")
        return

# Función para ver historial
def ver_historial():
    print("")

def actualizar_vista_urgencia():
    """Actualiza la vista de urgencia con datos del backend"""
    # Limpiar datos existentes
    for item in urgencia_tree.get_children():
        urgencia_tree.delete(item)
    
    # Obtener datos del backend
    try:
        response = api_client.get_queue_data("urgencia")
        if response.get('status'):
            pacientes = response.get('data', [])
            for paciente in pacientes:
                urgencia_tree.insert("", "end", values=(
                    paciente['name'],
                    paciente['admission'],
                    paciente['department']
                ))
    except Exception as e:
        print(f"Error al actualizar vista urgencia: {e}")

def actualizar_vista_general():
    """Actualiza la vista de general con datos del backend"""
    # Limpiar datos existentes
    for item in general_tree.get_children():
        general_tree.delete(item)
    
    try:
        response = api_client.get_queue_data("general")
        if response.get('status'):
            pacientes = response.get('data', [])
            for paciente in pacientes:
                general_tree.insert("", "end", values=(
                    paciente['name'],
                    paciente['admission'],
                    paciente['department']
                ))
    except Exception as e:
        print(f"Error al actualizar vista general: {e}")

def actualizar_vista_diagnostico():
    """Actualiza la vista de diagnóstico con datos del backend"""
    # Limpiar datos existentes
    for item in diagnostico_tree.get_children():
        diagnostico_tree.delete(item)
    
    try:
        response = api_client.get_queue_data("diagnostico")
        if response.get('status'):
            pacientes = response.get('data', [])
            for paciente in pacientes:
                diagnostico_tree.insert("", "end", values=(
                    paciente['name'],
                    paciente['admission'],
                    paciente['department']
                ))
    except Exception as e:
        print(f"Error al actualizar vista diagnóstico: {e}")

def actualizar_vistas_departamentos():
    """Actualiza todas las vistas de departamentos"""
    actualizar_vista_urgencia()
    actualizar_vista_general()
    actualizar_vista_diagnostico()
    # Actualizar estadísticas después de actualizar las vistas
    actualizar_estadisticas()

# Función para actualizar estadísticas
def actualizar_estadisticas():
    """Actualiza las estadísticas de pacientes en espera desde el backend"""
    global api_client, pacientes_en_espera_label, tiempo_espera_label
    
    try:
        # Obtener datos de pacientes en espera
        response = api_client.get_number_of_patients()
        
        if response.get('status'):
            # Obtener datos del response
            data = response.get('data', {})
            total_patients = data.get('total_patients_waiting', 0)
            summary = data.get('summary', {})
            
            # Actualizar el label de pacientes en espera
            pacientes_en_espera_label.config(text=str(total_patients))
            
            # Mostrar un desglose por departamento
            urgencia_count = summary.get('urgencia_count', 0)
            general_count = summary.get('general_count', 0)
            diagnostico_count = summary.get('diagnostico_count', 0)
            
            # Imprimir estadísticas en consola
            print(f"Estadísticas actualizadas:")
            print(f"  Total: {total_patients}")
            print(f"  Urgencia: {urgencia_count}")
            print(f"  General: {general_count}")
            print(f"  Diagnóstico: {diagnostico_count}")
            
        else:
            # Error del backend - mostrar 0
            pacientes_en_espera_label.config(text="0")
            print(f"Error al obtener estadísticas: {response.get('message', 'Error desconocido')}")
    
    except Exception as e:
        # Error de conexión - mostrar 0
        pacientes_en_espera_label.config(text="0")
        print(f"Error al actualizar estadísticas: {str(e)}")
    
    # Obtener tiempo promedio de espera
    try:
        avg_response = api_client.get_stadistics()
        
        if avg_response.get('status'):
            data = avg_response.get('data', {})
            avg_formatted = data.get('average_formatted', '0 min')
            tiempo_espera_label.config(text=avg_formatted)
            
            print(f"Tiempo promedio actualizado: {avg_formatted}")
        else:
            tiempo_espera_label.config(text="0 min")
            print(f"Error al obtener tiempo promedio: {avg_response.get('message', 'Error desconocido')}")
    
    except Exception as e:
        tiempo_espera_label.config(text="0 min")
        print(f"Error al actualizar tiempo promedio: {str(e)}")

# Función para generar reporte
def generar_reporte():
    """Genera y muestra un reporte completo de eficiencia del sistema"""
    global api_client
    
    try:
        # Obtener estadísticas de pacientes en espera
        patients_response = api_client.get_number_of_patients()
        
        # Obtener estadísticas de tiempo promedio
        avg_response = api_client.get_stadistics()
        
        # Crear ventana del reporte
        reporte_window = tk.Toplevel(root)
        reporte_window.title("Reporte de Eficiencia del Sistema")
        reporte_window.geometry("600x500")
        reporte_window.resizable(False, False)
        reporte_window.configure(bg='#f8f9fa')
        
        # Centrar la ventana
        reporte_window.transient(root)
        reporte_window.grab_set()
        
        # Frame principal con scroll
        main_frame = tk.Frame(reporte_window, bg='#f8f9fa', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título del reporte
        titulo = tk.Label(
            main_frame,
            text="REPORTE DE EFICIENCIA MÉDICA",
            font=("Arial", 16, "bold"),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        titulo.pack(pady=(0, 20))
        
        # Fecha y hora del reporte
        fecha_reporte = tk.Label(
            main_frame,
            text=f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            font=("Arial", 10),
            bg='#f8f9fa',
            fg='#7f8c8d'
        )
        fecha_reporte.pack(pady=(0, 20))
        
        # Frame para estadísticas de pacientes en espera
        espera_frame = tk.LabelFrame(
            main_frame,
            text="Pacientes en Espera",
            font=("Arial", 12, "bold"),
            bg='#ffffff',
            fg='#34495e',
            padx=15,
            pady=10
        )
        espera_frame.pack(fill='x', pady=(0, 15))
        
        if patients_response.get('status'):
            data = patients_response.get('data', {})
            summary = data.get('summary', {})
            
            # Total de pacientes
            total_label = tk.Label(
                espera_frame,
                text=f"Total de pacientes en cola: {summary.get('total_count', 0)}",
                font=("Arial", 11, "bold"),
                bg='#ffffff',
                fg='#2c3e50'
            )
            total_label.pack(anchor='w', pady=2)
            
            # Desglose por departamentos
            urgencia_label = tk.Label(
                espera_frame,
                text=f"Urgencia: {summary.get('urgencia_count', 0)} pacientes",
                font=("Arial", 10),
                bg='#ffffff',
                fg='#e74c3c'
            )
            urgencia_label.pack(anchor='w', pady=1)
            
            general_label = tk.Label(
                espera_frame,
                text=f"General: {summary.get('general_count', 0)} pacientes",
                font=("Arial", 10),
                bg='#ffffff',
                fg='#3498db'
            )
            general_label.pack(anchor='w', pady=1)
            
            diagnostico_label = tk.Label(
                espera_frame,
                text=f"Diagnóstico: {summary.get('diagnostico_count', 0)} pacientes",
                font=("Arial", 10),
                bg='#ffffff',
                fg='#f39c12'
            )
            diagnostico_label.pack(anchor='w', pady=1)
            
        else:
            error_label = tk.Label(
                espera_frame,
                text=f"Error: {patients_response.get('message', 'No se pudieron obtener datos')}",
                font=("Arial", 10),
                bg='#ffffff',
                fg='#e74c3c'
            )
            error_label.pack(anchor='w', pady=2)
        
        # Frame para estadísticas de tiempo
        tiempo_frame = tk.LabelFrame(
            main_frame,
            text="Análisis de Tiempos",
            font=("Arial", 12, "bold"),
            bg='#ffffff',
            fg='#34495e',
            padx=15,
            pady=10
        )
        tiempo_frame.pack(fill='x', pady=(0, 15))
        
        if avg_response.get('status'):
            data = avg_response.get('data', {})
            stats = data.get('statistics', {})
            
            # Tiempo promedio
            avg_label = tk.Label(
                tiempo_frame,
                text=f"Tiempo promedio de espera: {data.get('average_formatted', 'No calculado')}",
                font=("Arial", 11, "bold"),
                bg='#ffffff',
                fg='#2c3e50'
            )
            avg_label.pack(anchor='w', pady=2)
            
            # Estadísticas adicionales
            if stats.get('total_patients_attended', 0) > 0:
                total_atendidos = tk.Label(
                    tiempo_frame,
                    text=f"Total de pacientes atendidos: {stats.get('total_patients_attended', 0)}",
                    font=("Arial", 10),
                    bg='#ffffff',
                    fg='#27ae60'
                )
                total_atendidos.pack(anchor='w', pady=1)
                
                if stats.get('min_time', 0) > 0:
                    min_label = tk.Label(
                        tiempo_frame,
                        text=f"Tiempo mínimo: {stats.get('min_time', 0)} minutos",
                        font=("Arial", 10),
                        bg='#ffffff',
                        fg='#27ae60'
                    )
                    min_label.pack(anchor='w', pady=1)
                
                if stats.get('max_time', 0) > 0:
                    max_label = tk.Label(
                        tiempo_frame,
                        text=f"Tiempo máximo: {stats.get('max_time', 0)} minutos",
                        font=("Arial", 10),
                        bg='#ffffff',
                        fg='#e67e22'
                    )
                    max_label.pack(anchor='w', pady=1)
            else:
                sin_datos = tk.Label(
                    tiempo_frame,
                    text="No hay pacientes atendidos para calcular estadísticas",
                    font=("Arial", 10),
                    bg='#ffffff',
                    fg='#7f8c8d'
                )
                sin_datos.pack(anchor='w', pady=2)
        else:
            error_tiempo = tk.Label(
                tiempo_frame,
                text=f"Error: {avg_response.get('message', 'No se pudieron obtener datos de tiempo')}",
                font=("Arial", 10),
                bg='#ffffff',
                fg='#e74c3c'
            )
            error_tiempo.pack(anchor='w', pady=2)
        
        # Frame para recomendaciones
        recomendaciones_frame = tk.LabelFrame(
            main_frame,
            text="Recomendaciones",
            font=("Arial", 12, "bold"),
            bg='#ffffff',
            fg='#34495e',
            padx=15,
            pady=10
        )
        recomendaciones_frame.pack(fill='x', pady=(0, 15))
        
        # Generar recomendaciones basadas en datos
        if patients_response.get('status') and avg_response.get('status'):
            total_espera = patients_response.get('data', {}).get('summary', {}).get('total_count', 0)
            avg_time = avg_response.get('data', {}).get('average_minutes', 0)
            
            if total_espera > 10:
                rec1 = tk.Label(
                    recomendaciones_frame,
                    text="Alto volumen de pacientes: Considere aumentar personal médico",
                    font=("Arial", 10),
                    bg='#ffffff',
                    fg='#e67e22'
                )
                rec1.pack(anchor='w', pady=1)
            
            if avg_time > 60:
                rec2 = tk.Label(
                    recomendaciones_frame,
                    text="Tiempos altos: Revisar procesos de atención para optimizar flujo",
                    font=("Arial", 10),
                    bg='#ffffff',
                    fg='#e67e22'
                )
                rec2.pack(anchor='w', pady=1)
            
            if total_espera == 0:
                rec3 = tk.Label(
                    recomendaciones_frame,
                    text="Excelente: No hay pacientes en espera actualmente",
                    font=("Arial", 10),
                    bg='#ffffff',
                    fg='#27ae60'
                )
                rec3.pack(anchor='w', pady=1)
        
        # Botón cerrar
        cerrar_btn = tk.Button(
            main_frame,
            text="Cerrar Reporte",
            command=reporte_window.destroy,
            bg='#3498db',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        cerrar_btn.pack(pady=15)
        
        # Centrar la ventana
        reporte_window.update_idletasks()
        width = reporte_window.winfo_width()
        height = reporte_window.winfo_height()
        x = (reporte_window.winfo_screenwidth() // 2) - (width // 2)
        y = (reporte_window.winfo_screenheight() // 2) - (height // 2)
        reporte_window.geometry(f'{width}x{height}+{x}+{y}')
        
    except Exception as e:
        messagebox.showerror(
            "Error al Generar Reporte",
            f"No se pudo generar el reporte de eficiencia:\n\n{str(e)}"
        )

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

ttk.Button(root, text="Ver próximo paciente", width=20, command=ver_proximo_paciente).place(x=190, y=300)

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

# Actualizar las vistas después de atender al paciente
actualizar_vistas_departamentos()
actualizar_estadisticas()

# Ejecutar la aplicación
root.mainloop()