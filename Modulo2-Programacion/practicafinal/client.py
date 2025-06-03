"""
Módulo cliente para interactuar con la API de resultados de carreras.
"""

import requests

class FormulaUnoClient:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/"

    def crear_resultado(self):
        """
        Realiza una petición POST para crear un nuevo resultado de carrera.
        """
        url = self.base_url + "results/"
        pilotos_data = {
            "raceId": 10,
            "driverId": 24,
            "constructorId": 23,
            "number": 4,
            "grid": 5,
            "position": 2,
            "positionText": "1",
            "positionOrder": 1,
            "points": 25,
            "laps": 56,
            "time": "1:34:05.715",
            "milliseconds": 5645715,
            "fastestLap": 44,
            "rank": 1,
            "fastestLapTime": "1:32.406",
            "fastestLapSpeed": "210,5",
            "statusId": 1
        }
        response = requests.post(url, json=pilotos_data)
        print(f"Código de respuesta: {response.status_code}")
        if response.headers.get("content-type") == "application/json":
            print(f"Respuesta: {response.json()}")
        else:
            print("Respuesta en formato no JSON")

    def eliminar_resultado(self, result_id):
        """
        Realiza una petición DELETE para eliminar un resultado de carrera por su ID.
        """
        url = self.base_url + f"results/{result_id}"
        response = requests.delete(url)
        print(f"Código de respuesta: {response.status_code}")
        if response.headers.get("content-type") == "application/json":
            print(f"Respuesta: {response.json()}")
        else:
            print("Respuesta en formato no JSON")

    def obtener_inventario(self):
        """
        Realiza una petición GET para obtener el inventario de tablas y columnas.
        """
        url = self.base_url + "inventario/"
        response = requests.get(url)
        print(f"Código de respuesta: {response.status_code}")
        if response.headers.get("content-type") == "application/json":
            print(f"Respuesta: {response.json()}")
        else:
            print("Respuesta en formato no JSON")

    def obtener_circuitos(self):
        """
        Realiza una petición GET para obtener los identificadores y nombres de los circuitos.
        """
        url = self.base_url + "circuit_ids"
        response = requests.get(url)
        print(f"Código de respuesta: {response.status_code}")
        if response.headers.get("content-type") == "application/json":
            print(f"Respuesta: {response.json()}")
        else:
            print("Respuesta en formato no JSON")

    def obtener_ultimos_ganadores(self, circuit_id, n):
        """
        Realiza una petición GET para obtener los últimos n ganadores en un circuito específico.
        Args:
            circuit_id (int): ID del circuito.
            n (int): Número de ganadores a consultar.
        """
        url = self.base_url + f"last_n_winners_in_circuit/{circuit_id}/{n}"
        response = requests.get(url)
        print(f"Código de respuesta: {response.status_code}")
        if response.headers.get("content-type") == "application/json":
            print(f"Respuesta: {response.json()}")
        else:
            print("Respuesta en formato no JSON")

if __name__ == "__main__":
    client = FormulaUnoClient()
    print("== Crear resultado ==")
    client.crear_resultado()
    print("\n== Eliminar resultado (ID 23783) ==")
    client.eliminar_resultado(23785)
    print("\n== Obtener inventario ==")
    client.obtener_inventario()
    print("\n== Obtener circuitos ==")
    client.obtener_circuitos()
    print("\n== Obtener últimos ganadores (circuito 1, n=3) ==")
    client.obtener_ultimos_ganadores(1, 3)