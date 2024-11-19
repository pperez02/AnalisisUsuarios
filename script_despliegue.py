import subprocess

# Define las APIs y los puertos
apis = [
    {"name": "API_Contenidos", "path": "Microservicio_Contenidos.API_Contenidos.main:app", "port": 8000},
    {"name": "API_Usuarios", "path": "Microservicio_Usuarios.API_Usuarios.main:app", "port": 8001},
    {"name": "API_Interacciones", "path": "Microservicio_Interacciones.API_Interacciones.main:app", "port": 8002},
]

processes = []

try:
    # Lanza cada API en un proceso separado
    for api in apis:
        print(f"Iniciando {api['name']} en el puerto {api['port']}...")
        process = subprocess.Popen(
            ["uvicorn", api["path"], "--reload", "--port", str(api["port"])],
        )
        processes.append(process)
    
    # Mantén el script corriendo mientras las APIs están activas
    for process in processes:
        process.wait()

except KeyboardInterrupt:
    # Manejo de interrupción para detener todos los procesos
    print("\nDeteniendo APIs...")
    for process in processes:
        process.terminate()
