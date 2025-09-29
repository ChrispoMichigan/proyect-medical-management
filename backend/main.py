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
    def __init__(self, name: str, age:int, department:str):
        global id_counter
        id_counter += 1
        self.id = id_counter
        self.department = department
        self.name = name
        self.age = age
        self.admission = datetime.now()
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

'''
#! Cola: Departamentos de atención urgente

#! Emergencias
#TODO - Casos críticos, accidentes, urgencias médicas.
#! Urgencias pediátricas
#TODO - Atención inmediata para niños.
#! Unidad de cuidados intensivos
#TODO - Pacientes graves, monitoreo constante.

'''

'''
#* Cola: Departamentos clínicos generales

#? Pediatría
#TODO - Atención a niños y adolescentes.
#? Urgencias pediátricas
#TODO - Cuidado especializado para adultos mayores.

'''

'''
#* Cola: Departamentos de diagnóstico

#? Radiología
#TODO - Rayos X, resonancias, tomografías.
#? Laboratorio clínico
#TODO - Análisis de sangre, orina, etc.

'''


'''
#* Estructura de llegada al /api/createPatient
data: {
    patient: {
        name: string
        edad: int
    }
    department : string
}
'''
@app.route('/api/createPatient', methods=['POST'])
def createPatient():
    data = request.json
    print(data)
    print(type(data))
    return jsonify({"status": True})
'''
#* Estructura de mandado al /api/getNextPatient
data: {
    patient: {
        id  : int
        name: string
        edad: int
    }
}
'''
@app.route('/api/getNextPatient', methods=['GET'])
def getNextPatient():
    # Tu lógica de negocio aquí
    return jsonify({"message": "Datos del backend", "status": "success"})

@app.route('/api/data', methods=['GET'])
def get_data():
    # Tu lógica de negocio aquí
    return jsonify({"message": "Datos del backend", "status": "success"})

@app.route('/api/data', methods=['POST'])
def create_data():
    data = request.json
    # Procesar datos
    return jsonify({"message": "Datos creados", "data": data})

if __name__ == '__main__':
    app.run(debug=True, port=5000)