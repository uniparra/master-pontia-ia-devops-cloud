import requests

url = "http://127.0.0.1:8000/users/"

user_data = {
    "username":"Unai",
    "email":"jexunai@estanga.com",
    "age":12
}

response = requests.post(url, json=user_data)
print(response)
print(f"Código de respuesta: {response.status_code}")

if response.headers.get("content-type") == "application/json":
    print("Respuesta en formato JSON")
    print(f"Respuesta: {response.json()}")
else:
    print("Respuesta en formato no JSON")
