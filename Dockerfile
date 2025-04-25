# Uso de imagen de python 3.11-slim
FROM python:3.11-slim

# Se define el directorio de tabajo de la imagen
WORKDIR /app

COPY requirements.txt .

# Se instalan las dependencias y librerias necesarias
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5600

ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASS=${DB_PASS}

# Se copian los archivos necesarios a la imagen
COPY . .

# Se define el entrypoint de la imagen
ENTRYPOINT [ "python" ]

# Se ejecuta el comando para iniciar la aplicacion
CMD [ "./app.py" ]




