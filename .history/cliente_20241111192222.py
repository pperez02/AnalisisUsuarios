import requests

# Configuración de la URL base de la API
BASE_URL = "http://127.0.0.1:8000"

def login_user():
    print("\n--- Iniciar sesión de usuario ---")
    email = input("Email: ")
    password = input("Contraseña: ")

    url = f"{BASE_URL}/usuarios/login"
    payload = {
        "email": email,
        "password": password
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Inicio de sesión exitoso:", response.json())
    else:
        print(f"Error en el inicio de sesión: {response.status_code} - {response.json()}")

# Ejemplo de uso
if __name__ == "__main__":
    print("Selecciona una opción:")
    print("1. Iniciar sesión")
    option = input("Opción (1): ")
    
    if option == "1":
        login_user()
    else:
        print("Opción no válida.")
