# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY API_Contenidos /app/API_Contenidos
COPY contenidos.db /app/

# Instala las dependencias
RUN pip install fastapi uvicorn sqlalchemy pydantic

# Comando para ejecutar la aplicación
CMD ["uvicorn", "API_Contenidos.main:app", "--host", "0.0.0.0", "--port", "8000"]
