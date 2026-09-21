import logging
import os
import time

from flask import Flask


app = Flask(__name__)

# la configuración viene de afuera, con variables de entorno (no va en el código!)
GREETING = os.environ.get("GREETING", "Hola desde local!")

# la config más simple posible: loguear de INFO para arriba, a la salida estándar
# (que es lo que el PaaS recolecta y nos muestra)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
# el servidor web loguea una línea por request, que acá nos sobra: solo queremos
# ver sus warnings y errores
logging.getLogger("werkzeug").setLevel(logging.WARNING)


@app.route("/")
def home_page():
    logging.info("Alguien entró a la página principal")
    return f"<h1>{GREETING}</h1><a href='/slow'>Una request lenta</a> | <a href='/error'>Una request que falla</a>"


@app.route("/slow")
def slow():
    logging.warning("Ojo, esta request va a tardar 2 segundos!")
    time.sleep(2)
    logging.info("Listo, terminó la request lenta")
    return "<h1>Perdón, tardé...</h1><a href='/'>Volver</a>"


@app.route("/error")
def error():
    logging.error("No pudimos responder la request, algo falló!")
    raise Exception("Algo salió muy mal!")


# el PaaS nos dice en qué puerto tenemos que escuchar, con la variable PORT
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
