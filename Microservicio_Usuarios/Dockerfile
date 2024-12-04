# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el código fuente de la API al contenedor
COPY API_Usuarios /app/API_Usuarios
COPY usuarios.db /app/

# Instala las dependencias necesarias
RUN pip install fastapi uvicorn sqlalchemy pydantic "pydantic[email]" typing

# Comando para ejecutar la aplicación
CMD ["uvicorn", "API_Usuarios.main:app", "--host", "0.0.0.0", "--port", "8001"]
