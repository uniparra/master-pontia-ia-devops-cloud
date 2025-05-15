import requests

url = "http://127.0.0.1:8000/users/"

user_data = {
    "username":"jexux",
    "email":"jexux@estanga.com",
    "age":18
}

response = requests.post(url, json=user_data)
print(f"Código de respuesta: {response.status_code}")
print(f"Respuesta: {response.json()}")