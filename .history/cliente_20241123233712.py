import requests
import json

BASE_URL = "http://localhost:8000"  # Cambia esto si tu servidor está en otro puerto

def get_input(message):
    return input(message)

def create_actor():
    nombre = get_input("Ingrese el nombre del actor: ")
    nacionalidad = get_input("Ingrese la nacionalidad del actor: ")
    fecha_nacimiento = get_input("Ingrese la fecha de nacimiento del actor (YYYY-MM-DD): ")
    
    payload = {
        "nombre": nombre,
        "nacionalidad": nacionalidad,
        "fechaNacimiento": fecha_nacimiento
    }
    
    response = requests.post(f"{BASE_URL}/actores", json=payload)
    if response.status_code == 200:
        print("Actor creado:", response.json())
    else:
        print("Error al crear el actor:", response.text)

def create_director():
    nombre = get_input("Ingrese el nombre del director: ")
    nacionalidad = get_input("Ingrese la nacionalidad del director: ")
    fecha_nacimiento = get_input("Ingrese la fecha de nacimiento del director (YYYY-MM-DD): ")
    
    payload = {
        "nombre": nombre,
        "nacionalidad": nacionalidad,
        "fechaNacimiento": fecha_nacimiento
    }
    
    response = requests.post(f"{BASE_URL}/directores", json=payload)
    if response.status_code == 200:
        print("Director creado:", response.json())
    else:
        print("Error al crear el director:", response.text)

def get_actor():
    actor_id = get_input("Ingrese el ID del actor a visualizar: ")
    response = requests.get(f"{BASE_URL}/actores/{actor_id}")
    if response.status_code == 200:
        print("Actor encontrado:", response.json())
    else:
        print("Error al obtener el actor:", response.text)

def get_director():
    director_id = get_input("Ingrese el ID del director a visualizar: ")
    response = requests.get(f"{BASE_URL}/directores/{director_id}")
    if response.status_code == 200:
        print("Director encontrado:", response.json())
    else:
        print("Error al obtener el director:", response.text)

def update_actor():
    actor_id = get_input("Ingrese el ID del actor a actualizar: ")
    nombre = get_input("Ingrese el nuevo nombre del actor: ")
    nacionalidad = get_input("Ingrese la nueva nacionalidad del actor: ")
    fecha_nacimiento = get_input("Ingrese la nueva fecha de nacimiento del actor (YYYY-MM-DD): ")
    
    payload = {
        "nombre": nombre,
        "nacionalidad": nacionalidad,
        "fechaNacimiento": fecha_nacimiento
    }

    print(payload)
    
    response = requests.put(f"{BASE_URL}/actores/{actor_id}", json=payload)
    if response.status_code == 200:
        print("Actor actualizado:", response.json())
    else:
        print("Error al actualizar el actor:", response.text)

def update_director():
    director_id = get_input("Ingrese el ID del director a actualizar: ")
    nombre = get_input("Ingrese el nuevo nombre del director: ")
    nacionalidad = get_input("Ingrese la nueva nacionalidad del director: ")
    fecha_nacimiento = get_input("Ingrese la nueva fecha de nacimiento del director (YYYY-MM-DD): ")
    
    payload = {
        "nombre": nombre,
        "nacionalidad": nacionalidad,
        "fechaNacimiento": fecha_nacimiento
    }
    
    response = requests.put(f"{BASE_URL}/directores/{director_id}", json=payload)
    if response.status_code == 200:
        print("Director actualizado:", response.json())
    else:
        print("Error al actualizar el director:", response.text)

def delete_actor():
    actor_id = get_input("Ingrese el ID del actor a eliminar: ")
    response = requests.delete(f"{BASE_URL}/actores/{actor_id}")
    if response.status_code == 200:
        print("Actor eliminado exitosamente")
    else:
        print("Error al eliminar el actor:", response.text)

def delete_director():
    director_id = get_input("Ingrese el ID del director a eliminar: ")
    response = requests.delete(f"{BASE_URL}/directores/{director_id}")
    if response.status_code == 200:
        print("Director eliminado exitosamente")
    else:
        print("Error al eliminar el director:", response.text)

def menu():
    while True:
        print("\n--- Menú ---")
        print("1. Crear actor")
        print("2. Crear director")
        print("3. Visualizar actor")
        print("4. Visualizar director")
        print("5. Actualizar actor")
        print("6. Actualizar director")
        print("7. Eliminar actor")
        print("8. Eliminar director")
        print("9. Salir")

        choice = get_input("Seleccione una opción: ")

        if choice == "1":
            create_actor()
        elif choice == "2":
            create_director()
        elif choice == "3":
            get_actor()
        elif choice == "4":
            get_director()
        elif choice == "5":
            update_actor()
        elif choice == "6":
            update_director()
        elif choice == "7":
            delete_actor()
        elif choice == "8":
            delete_director()
        elif choice == "9":
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    menu()
