'''
#! Dependencias
#* pip install flask flask-cors
'''
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

'''
#* Clase de colas
'''
class Queue:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, element):
        """
            #* Añade un elemento al final de la cola.
        """
        self.queue.append(element)

    def dequeue(self):
        """
            #* Devuelve el primer item de la cola y lo borra.

            #TODO - Returns:
                Retorna el elemento borrado
        """
        if self.isEmpty():
            return None
        return self.queue.pop(0)

    def peek(self):
        '''
            #* Devuelve el primer item de la cola

            #TODO - Returns:
                Retorna el elemento al inicio de la cola
        '''
        if self.isEmpty():
            return "Queue is empty"
        return self.queue[0]

    def isEmpty(self):
        '''
            #* Revisa si la cola esta vacia

            #TODO - Returns:
                True: en caso de que la cola este vacia
                False: en caso de que la cola contenga algún elemento
        '''
        return len(self.queue) == 0

    def size(self):
        '''
            #* Obtiene el número de elementos de la cola

            #TODO - Returns:
                int: retorna el número de elementos
        '''
        return len(self.queue)

'''
#* Data del paciente
'''
id_counter = 0
class Patient:
    def __init__(self, name: str, age:int, department:str, admission : datetime):
        global id_counter
        id_counter += 1
        self.id = id_counter
        self.department = department
        self.name = name
        self.age = age
        self.admission = admission
        self.egress = None
        self.waiting_time = None

'''
#* Clase de historial de pacientes
'''
class Record:
    def __init__(self):
        self.record = []

    def addHistory(self, patient : Patient):
        self.record.append(patient)

'''
#* Clase de departamento
'''
class Department:
    def __init__(self, name: str):
        self.name = name,
        self.cola = Queue()

    def addPatiend(self, patient : Patient):
        self.cola.enqueue(patient)

    def getNext(self):
        return self.cola.peek()
    
    def attendPatient(self):
        return self.cola.dequeue()
    
    def viewPatients(self):
        return self.cola.queue

'''
#! Cola: Departamentos de atención urgente

#! Emergencias
#TODO - Casos críticos, accidentes, urgencias médicas.
#! Urgencias pediátricas
#TODO - Atención inmediata para niños.
#! Unidad de cuidados intensivos
#TODO - Pacientes graves, monitoreo constante.

'''
urgencia = Department('urgencia')

'''
#* Cola: Departamentos clínicos generales

#? Pediatría
#TODO - Atención a niños y adolescentes.
#? Urgencias pediátricas
#TODO - Cuidado especializado para adultos mayores.

'''
general = Department('general')

'''
#* Cola: Departamentos de diagnóstico

#? Radiología
#TODO - Rayos X, resonancias, tomografías.
#? Laboratorio clínico
#TODO - Análisis de sangre, orina, etc.

'''
diagnostico = Department('diagnostico')

'''
#* Historial global de pacientes atendidos
'''
historial = Record()

'''
#* Estructura de llegada al /api/createPatient
{
  "data": {
    "patient": {
        "name"      : "Juan",
        "age"       : 65,
        "department": "general",
        "admission" : null | Date
    }
  }
}
'''
@app.route('/api/createPatient', methods=['POST'])
def createPatient():
    data = request.json
    # print('Respuesta obtenida')
    # print(data)
    # print('--------------------------')
    global urgencia
    global general
    global diagnostico

    try:
        department = data['patient']['department']
        name = data['patient']['name']
        age = data['patient']['age']
        admission = data['patient']['admission']
        if admission is None:
            admission = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        patient = Patient(
            name,
            age,
            department,
            admission
        )

        if department == 'general':
            general.addPatiend(patient)
            print('Añadido a la cola general')
            for value in general.cola.queue:
                print('--------------------------')
                print(value.name)
                print(value.age)
                print(type(value.admission))
                print('--------------------------')
            return jsonify({"status": True, "message": "Añadido a la cola general"})
        
        if department == 'urgencia':
            urgencia.addPatiend(patient)
            #print(urgencia.cola.queue)
            return jsonify({"status": True, "message": "Añadido a la cola urgencias"})
        
        if department == 'diagnostico':
            diagnostico.addPatiend(patient)
            #print(urgencia.cola.queue)
            return jsonify({"status": True, "message": "Añadido a la cola diagnosticos"}) 
    except Exception as error:
        print(f'Error: {str(error)}')
        return jsonify({"status": False, "message": f"Error: {str(error)}"})
       

@app.route('/api/attendPatient', methods=['POST'])
def attendPatient():
    data = request.json
    global urgencia, general, diagnostico, historial
    
    try:
        # Obtener datos del paciente desde el request
        patient_data = data
        
        # Validar que tenemos los datos necesarios
        required_fields = ['id', 'name', 'age', 'department', 'admission']
        for field in required_fields:
            if field not in patient_data:
                return jsonify({
                    "status": False, 
                    "message": f"Campo requerido faltante: {field}"
                })
        
        # Obtener el departamento del paciente
        department_name = patient_data['department']
        
        # Determinar de qué cola remover el paciente
        department_obj = None
        if department_name == 'urgencia':
            department_obj = urgencia
        elif department_name == 'general':
            department_obj = general
        elif department_name == 'diagnostico':
            department_obj = diagnostico
        else:
            return jsonify({
                "status": False,
                "message": f"Departamento no válido: {department_name}"
            })
        
        # Buscar y remover el paciente de la cola
        patient_found = None
        cola = department_obj.cola.queue
        
        for i, patient in enumerate(cola):
            if patient.id == patient_data['id']:
                patient_found = cola.pop(i)  # Remover de la cola
                break
        
        if not patient_found:
            return jsonify({
                "status": False,
                "message": f"Paciente con ID {patient_data['id']} no encontrado en la cola de {department_name}"
            })
        
        # Calcular tiempo de egreso (actual)
        egress_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calcular tiempo de espera
        try:
            admission_datetime = datetime.strptime(patient_found.admission, "%Y-%m-%d %H:%M:%S")
            egress_datetime = datetime.strptime(egress_time, "%Y-%m-%d %H:%M:%S")
            
            # Calcular diferencia en minutos
            time_diff = egress_datetime - admission_datetime
            waiting_minutes = int(time_diff.total_seconds() / 60)
            waiting_time = f"{waiting_minutes} minutos"
            
        except ValueError as e:
            print(f"Error al calcular tiempo de espera: {str(e)}")
            waiting_time = "No calculado"
        
        # Crear un diccionario con todos los datos del paciente atendido
        attended_patient = {
            'id': patient_found.id,  # Conservar ID original
            'name': patient_found.name,
            'age': patient_found.age,
            'department': patient_found.department,
            'admission': patient_found.admission,
            'egress': egress_time,
            'waiting_time': waiting_time
        }
        
        # Actualizar el objeto paciente encontrado
        patient_found.egress = egress_time
        patient_found.waiting_time = waiting_time
        
        # Agregar al historial
        historial.addHistory(patient_found)
        
        return jsonify({
            "status": True,
            "message": f"Paciente {patient_found.name} atendido correctamente en {department_name}",
            "patient": attended_patient,
            "waiting_time": waiting_time,
            "department": department_name
        })
        
    except KeyError as e:
        print(f'Error de clave faltante: {str(e)}')
        return jsonify({
            "status": False, 
            "message": f"Datos incompletos en la petición: {str(e)}"
        })
        
    except Exception as error:
        print(f'Error en attendPatient: {str(error)}')
        return jsonify({
            "status": False, 
            "message": f"Error interno del servidor: {str(error)}"
        })

'''
#* Estructura de mandado al /api/getNextPatient
{
    "patient": {
        "id"        : 1
        "name"      : "Juan",
        "age"      : 65,
        "department": "general"
    }
}
'''
@app.route('/api/getNextPatient', methods=['GET'])
def getNextPatient():
    global urgencia, general, diagnostico
    
    try:
        # 1. Revisar primero si hay pacientes en urgencia (máxima prioridad)
        if not urgencia.cola.isEmpty():
            patient = urgencia.cola.peek()
            if patient != "Queue is empty":
                data = {
                    "patient": {
                        "id": patient.id,
                        "name": patient.name,
                        "age": patient.age,
                        "department": patient.department,
                        "admission": patient.admission,
                        "waiting_time": patient.waiting_time,
                        "egress": patient.egress
                    }
                }
                return jsonify({"data": data, "status": True, "message": "Siguiente paciente de urgencia"})
        
        # 2. Si urgencia está vacía, revisar general y diagnóstico
        general_patient = None
        diagnostico_patient = None
        
        # Obtener paciente de general si no está vacía
        if not general.cola.isEmpty():
            temp_general = general.cola.peek()
            if temp_general != "Queue is empty":
                general_patient = temp_general
        
        # Obtener paciente de diagnóstico si no está vacía
        if not diagnostico.cola.isEmpty():
            temp_diagnostico = diagnostico.cola.peek()
            if temp_diagnostico != "Queue is empty":
                diagnostico_patient = temp_diagnostico
        
        # 3. Comparar fechas de admisión para determinar prioridad
        selected_patient = None
        
        if general_patient and diagnostico_patient:
            # Ambas colas tienen pacientes - comparar fechas
            try:
                # Convertir strings de fecha a objetos datetime para comparación
                general_admission = datetime.strptime(general_patient.admission, "%Y-%m-%d %H:%M:%S")
                diagnostico_admission = datetime.strptime(diagnostico_patient.admission, "%Y-%m-%d %H:%M:%S")
                
                # Seleccionar el que llegó primero (fecha más temprana)
                if general_admission <= diagnostico_admission:
                    selected_patient = general_patient
                else:
                    selected_patient = diagnostico_patient
                    
            except ValueError as e:
                print(f"Error al parsear fechas: {str(e)}")
                # En caso de error, priorizar general
                selected_patient = general_patient
                
        elif general_patient:
            # Solo hay pacientes en general
            selected_patient = general_patient
            
        elif diagnostico_patient:
            # Solo hay pacientes en diagnóstico
            selected_patient = diagnostico_patient
        
        # 4. Devolver el paciente seleccionado
        if selected_patient:
            data = {
                "patient": {
                    "id": selected_patient.id,
                    "name": selected_patient.name,
                    "age": selected_patient.age,
                    "department": selected_patient.department,
                    "admission": selected_patient.admission,
                    "waiting_time": selected_patient.waiting_time,
                    "egress": selected_patient.egress
                }
            }
            return jsonify({
                "data": data, 
                "status": True, 
                "message": f"Siguiente paciente de {selected_patient.department}"
            })
        
        # 5. No hay pacientes en ninguna cola
        return jsonify({
            "data": None, 
            "status": False, 
            "message": "No hay pacientes en cola en ningún departamento"
        })
        
    except Exception as error:
        print(f'Error en getNextPatient: {str(error)}')
        return jsonify({
            "data": None, 
            "status": False, 
            "message": f"Error interno del servidor: {str(error)}"
        })

@app.route('/api/getQueue/general', methods=['GET'])
def colaGeneral():
    global general
    
    try:
        cola = general.cola.queue
        
        # Convertir objetos Patient a formato JSON
        pacientes_data = []
        for patient in cola:
            paciente_info = {
                "id": patient.id,
                "name": patient.name,
                "age": patient.age,
                "department": patient.department,
                "admission": patient.admission,
                "waiting_time": patient.waiting_time,
                "egress": patient.egress
            }
            pacientes_data.append(paciente_info)
        
        return jsonify({
            "data": pacientes_data,
            "status": True,
            "message": f"Cola general - {len(pacientes_data)} pacientes en espera",
            "count": len(pacientes_data)
        })
        
    except Exception as error:
        print(f'Error en colaGeneral: {str(error)}')
        return jsonify({
            "data": [],
            "status": False,
            "message": f"Error al obtener cola general: {str(error)}",
            "count": 0
        })

@app.route('/api/getQueue/urgencia', methods=['GET'])
def colaUrgencia():
    global urgencia
    
    try:
        cola = urgencia.cola.queue
        
        # Convertir objetos Patient a formato JSON
        pacientes_data = []
        for patient in cola:
            paciente_info = {
                "id": patient.id,
                "name": patient.name,
                "age": patient.age,
                "department": patient.department,
                "admission": patient.admission,
                "waiting_time": patient.waiting_time,
                "egress": patient.egress
            }
            pacientes_data.append(paciente_info)
        
        return jsonify({
            "data": pacientes_data,
            "status": True,
            "message": f"Cola urgencia - {len(pacientes_data)} pacientes en espera",
            "count": len(pacientes_data)
        })
        
    except Exception as error:
        print(f'Error en colaUrgencia: {str(error)}')
        return jsonify({
            "data": [],
            "status": False,
            "message": f"Error al obtener cola urgencia: {str(error)}",
            "count": 0
        })

@app.route('/api/getQueue/diagnostico', methods=['GET'])
def colaDiagnostico():
    global diagnostico
    
    try:
        cola = diagnostico.cola.queue
        
        # Convertir objetos Patient a formato JSON
        pacientes_data = []
        for patient in cola:
            paciente_info = {
                "id": patient.id,
                "name": patient.name,
                "age": patient.age,
                "department": patient.department,
                "admission": patient.admission,
                "waiting_time": patient.waiting_time,
                "egress": patient.egress
            }
            pacientes_data.append(paciente_info)
        
        return jsonify({
            "data": pacientes_data,
            "status": True,
            "message": f"Cola diagnóstico - {len(pacientes_data)} pacientes en espera",
            "count": len(pacientes_data)
        })
        
    except Exception as error:
        print(f'Error en colaDiagnostico: {str(error)}')
        return jsonify({
            "data": [],
            "status": False,
            "message": f"Error al obtener cola diagnóstico: {str(error)}",
            "count": 0
        })

@app.route('/api/patientsWaiting', methods=['GET'])
def patientsWaiting():
    global urgencia, general, diagnostico
    
    try:
        # Obtener el número de pacientes en cada cola
        urgencia_count = len(urgencia.cola.queue)
        general_count = len(general.cola.queue)
        diagnostico_count = len(diagnostico.cola.queue)
        
        # Calcular el total
        total_patients = urgencia_count + general_count + diagnostico_count
        
        # Crear respuesta
        response_data = {
            "total_patients_waiting": total_patients,
            "summary": {
                "urgencia_count": urgencia_count,
                "general_count": general_count,
                "diagnostico_count": diagnostico_count,
                "total_count": total_patients
            }
        }
        
        # Determinar mensaje según la cantidad de pacientes
        if total_patients == 0:
            message = "No hay pacientes en espera en ningún departamento"
        elif total_patients == 1:
            message = "Hay 1 paciente esperando atención"
        else:
            message = f"Hay {total_patients} pacientes esperando atención"
        
        return jsonify({
            "data": response_data,
            "status": True,
            "message": message,
            "total_waiting": total_patients
        })
        
    except Exception as error:
        print(f'Error en patientsWaiting: {str(error)}')
        return jsonify({
            "data": None,
            "status": False,
            "message": f"Error al obtener estadísticas de pacientes: {str(error)}",
            "total_waiting": 0
        })

@app.route('/api/averageTime', methods=['GET'])
def averageTime():
    global historial
    
    try:
        # Obtener todos los pacientes del historial
        patients_history = historial.record
        
        # Verificar si hay pacientes en el historial
        if not patients_history:
            return jsonify({
                "data": {
                    "average_waiting_time": 0,
                    "total_patients": 0,
                    "average_minutes": 0,
                    "average_formatted": "0 minutos"
                },
                "status": True,
                "message": "No hay pacientes atendidos en el historial"
            })
        
        # Lista para almacenar los tiempos válidos en minutos
        valid_waiting_times = []
        
        # Procesar cada paciente del historial
        for patient in patients_history:
            waiting_time = patient.waiting_time
            
            # Verificar que el paciente tenga tiempo de espera
            if waiting_time and waiting_time != "No calculado":
                try:
                    # Extraer número de minutos del string "X minutos"
                    if "minutos" in waiting_time:
                        minutes_str = waiting_time.replace("minutos", "").strip()
                        minutes = int(minutes_str)
                        valid_waiting_times.append(minutes)
                    elif "horas" in waiting_time:
                        # Si alguien estuvo más de una hora, convertir a minutos
                        hours_str = waiting_time.replace("horas", "").strip()
                        hours = float(hours_str)
                        minutes = int(hours * 60)
                        valid_waiting_times.append(minutes)
                except (ValueError, AttributeError) as e:
                    print(f"Error procesando tiempo de espera '{waiting_time}': {str(e)}")
                    continue
        
        # Calcular promedio si hay tiempos válidos
        if valid_waiting_times:
            average_minutes = sum(valid_waiting_times) / len(valid_waiting_times)
            average_rounded = round(average_minutes, 2)
            
            # Formatear el resultado
            if average_rounded >= 60:
                hours = average_rounded / 60
                average_formatted = f"{round(hours, 1)} horas"
            else:
                average_formatted = f"{round(average_rounded)} minutos"
            
        else:
            average_minutes = 0
            average_rounded = 0
            average_formatted = "0 minutos"
        
        # Crear respuesta detallada
        response_data = {
            "average_waiting_time": average_rounded,
            "total_patients": len(patients_history),
            "patients_with_valid_time": len(valid_waiting_times),
            "average_minutes": average_rounded,
            "average_formatted": average_formatted,
            "raw_times": valid_waiting_times,  # Para debug
            "statistics": {
                "min_time": min(valid_waiting_times) if valid_waiting_times else 0,
                "max_time": max(valid_waiting_times) if valid_waiting_times else 0,
                "total_patients_attended": len(patients_history),
                "patients_with_calculated_time": len(valid_waiting_times)
            }
        }
        
        # Determinar mensaje
        if len(valid_waiting_times) == 0:
            message = f"Se encontraron {len(patients_history)} pacientes atendidos, pero ninguno tiene tiempo de espera calculado"
        elif len(valid_waiting_times) == 1:
            message = f"Tiempo promedio de espera: {average_formatted} (basado en 1 paciente)"
        else:
            message = f"Tiempo promedio de espera: {average_formatted} (basado en {len(valid_waiting_times)} pacientes)"
        
        return jsonify({
            "data": response_data,
            "status": True,
            "message": message
        })
        
    except Exception as error:
        print(f'Error en averageTime: {str(error)}')
        return jsonify({
            "data": {
                "average_waiting_time": 0,
                "total_patients": 0,
                "average_minutes": 0,
                "average_formatted": "Error al calcular"
            },
            "status": False,
            "message": f"Error al calcular tiempo promedio: {str(error)}"
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)