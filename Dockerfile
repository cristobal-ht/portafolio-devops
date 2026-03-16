#1. Usar imagen de python oficial, la version ligera
FROM python:3.9-slim
#2. Crear una carpeta dentro del contenedor para la app
WORKDIR /app
#3. copiar el archivo Python al contenedor
# Se utilizan las comillas si el archivo tieneun espacio en el nombre"
COPY . .
#4. agregar las librerias que utilice
RUN pip install flask
#5. Indicarle a docker como ejecutar el programa
CMD ["python", "paginaweb.py"]