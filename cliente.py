import requests

# Configuración de la URL base de la API
BASE_URL = "http://127.0.0.1:8000"

def create_user():
    print("\n--- Crear un nuevo usuario ---")
    nombre = input("Nombre: ")
    email = input("Email: ")
    password = input("Contraseña: ")
    idioma = input("Idioma (opcional): ") or None
    idPlanSuscripcion = input("ID del Plan de Suscripción (opcional): ") or None
    idListaPersonalizada = input("ID de la Lista Personalizada (opcional): ") or None
    idHistorial = input("ID del Historial (opcional): ") or None

    url = f"{BASE_URL}/usuarios/registro"
    payload = {
        "nombre": nombre,
        "email": email,
        "password": password,
        "idioma": idioma,
        "idPlanSuscripcion": idPlanSuscripcion,
        "idListaPersonalizada": idListaPersonalizada,
        "idHistorial": idHistorial
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Usuario creado exitosamente:", response.json())
    else:
        print(f"Error al crear usuario: {response.status_code} - {response.json()}")

def get_users():
    print("\n--- Obtener lista de usuarios ---")
    skip = int(input("Número de usuarios a omitir (skip): ") or 0)
    limit = int(input("Número de usuarios a obtener (limit): ") or 10)

    url = f"{BASE_URL}/usuarios?skip={skip}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Usuarios encontrados:", response.json())
    else:
        print(f"Error al obtener usuarios: {response.status_code} - {response.json()}")

# Ejemplo de uso
if __name__ == "__main__":
    print("Selecciona una opción:")
    print("1. Crear un usuario")
    print("2. Obtener lista de usuarios")
    option = input("Opción (1 o 2): ")
    
    if option == "1":
        create_user()
    elif option == "2":
        get_users()
    else:
        print("Opción no válida.")
