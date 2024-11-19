import requests

BASE_URL = "http://127.0.0.1:8001"  # Asegúrate de que sea la URL correcta del microservicio

def menu():
    print("\n== Menú de opciones ==")
    print("1. Consultar historial de un usuario")
    print("2. Añadir contenido al historial de un usuario")
    print("3. Salir")
    return input("Elige una opción: ")

def consultar_historial():
    usuario_id = input("Introduce el ID del usuario: ")
    response = requests.get(f"{BASE_URL}/usuarios/{usuario_id}/historial")
    if response.status_code == 200:
        historial = response.json()
        print("\n== Historial del usuario ==")
        for contenido in historial:
            print(f"Título: {contenido['titulo']}, Género: {contenido['idGenero']}, Fecha de Lanzamiento: {contenido['fechaLanzamiento']}")
    else:
        print(f"Error al consultar el historial: {response.status_code}, {response.json()}")

def añadir_a_historial():
    usuario_id = input("Introduce el ID del usuario: ")
    contenido_id = input("Introduce el ID del contenido: ")
    response = requests.post(f"{BASE_URL}/usuarios/{usuario_id}/historial/{contenido_id}")
    if response.status_code == 200:
        print("El contenido ha sido añadido al historial correctamente.")
    else:
        print(f"Error al añadir contenido al historial: {response.status_code}, {response.json()}")

if __name__ == "__main__":
    while True:
        opcion = menu()
        if opcion == "1":
            consultar_historial()
        elif opcion == "2":
            añadir_a_historial()
        elif opcion == "3":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")
