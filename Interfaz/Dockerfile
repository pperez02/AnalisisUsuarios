# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY Streamflix.py /app/
COPY static /app/static
COPY templates /app/templates

# Instala las dependencias
RUN pip install fastapi uvicorn jinja2 requests python-multipart

# Comando para ejecutar la aplicación
CMD ["uvicorn", "Streamflix:app", "--host", "0.0.0.0", "--port", "8003"]
