import requests

url = "http://127.0.0.1:8000/users/"

user_data = {
    "username":"jexuxEstangaPiparrategi",
    "email":"jexux@estanga.com",
    "age":50
}

print("Hola")

response = requests.post(url, json=user_data)
print(response)
print(f"Código de respuesta: {response.status_code}")
print(f"Respuesta: {response.json()}")