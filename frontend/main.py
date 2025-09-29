'''
#! Dependencias
#* pip install requests
'''
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

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

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente Frontend")
        self.root.geometry("600x400")
        
        self.api_client = APIClient()
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botón para obtener datos
        get_btn = ttk.Button(
            main_frame, 
            text="Obtener Datos", 
            command=self.get_data
        )
        get_btn.grid(row=0, column=0, padx=5, pady=5)
        
        # Botón para enviar datos
        send_btn = ttk.Button(
            main_frame, 
            text="Enviar Datos", 
            command=self.send_data
        )
        send_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Área de texto para mostrar resultados
        self.result_text = tk.Text(main_frame, height=20, width=70)
        self.result_text.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.result_text.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.result_text.configure(yscrollcommand=scrollbar.set)
    
    def get_data(self):
        result = self.api_client.get_data()
        self.display_result(result)
    
    def send_data(self):
        # Ejemplo de datos a enviar
        data = {"nombre": "ejemplo", "valor": 123}
        result = self.api_client.post_data(data)
        self.display_result(result)
    
    def display_result(self, result):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, json.dumps(result, indent=2, ensure_ascii=False))
        
        if "error" in result:
            messagebox.showerror("Error", f"Error de conexión: {result['error']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()