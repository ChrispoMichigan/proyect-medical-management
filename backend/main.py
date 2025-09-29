'''
#! Dependencias
#* pip install flask flask-cors
'''
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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