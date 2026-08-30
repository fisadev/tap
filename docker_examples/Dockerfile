# partimos de una imagen pública que ya tiene python 3.14 instalado
FROM python:3.14

# instalamos uv, para poder instalar las dependencias de nuestro proyecto
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# creamos un directorio para nuestra aplicación y nos movemos a trabajar dentro
RUN mkdir /myweb
WORKDIR /myweb

# copiamos los archivos de configuración de nuestro proyecto a la imagen, e 
# instalamos las dependencias
COPY pyproject.toml /myweb/
RUN uv sync

# copiamos el código de nuestra aplicación y creamos un directorio para 
# almacenar los datos
COPY web.py /myweb/
RUN mkdir /myweb/data

# definimos el comando que hay que correr cuando se levanten nuevos 
# contenedores a partir de esta imagen
CMD ["uv", "run", "web.py"]
