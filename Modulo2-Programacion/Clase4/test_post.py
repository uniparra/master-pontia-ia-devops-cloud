import requests

url = "http://127.0.0.1:8000/pilotos/"

print("HOlahola")

pilotos_data = {
    "pilotos":"Fernando Alonso",
    "victorias":32,
    "anosactivo":"33"
}

response = requests.post(url, json=pilotos_data)
print(f"Código de respuesta: {response.status_code}")
if response.headers.get("content-type") == "application/json":
    print(f"Respuesta: {response.json()}")
else:
    print("Respuesta en formato no JSON")