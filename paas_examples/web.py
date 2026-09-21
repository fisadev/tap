import logging
import os
import time

import psycopg
from flask import Flask


app = Flask(__name__)

# la configuración viene de afuera, con variables de entorno (no va en el código!)
GREETING = os.environ.get("GREETING", "Hola desde local!")
DATABASE_URL = os.environ.get("DATABASE_URL")

# la config más simple posible: loguear de INFO para arriba, a la salida estándar
# (que es lo que el PaaS recolecta y nos muestra)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
# el servidor web loguea una línea por request, que acá nos sobra: solo queremos
# ver sus warnings y errores
logging.getLogger("werkzeug").setLevel(logging.WARNING)


def run_sql(sql, *params):
    """Corre una query en la db, y devuelve sus resultados (si tiene)."""
    # abrimos y cerramos una conexión por consulta: lo más simple posible (una app
    # real usaría un pool de conexiones)
    with psycopg.connect(DATABASE_URL) as connection, connection.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall() if cursor.description else []


# la tabla se crea sola al arrancar la app, si todavía no existe
if DATABASE_URL:
    run_sql("CREATE TABLE IF NOT EXISTS things (id SERIAL PRIMARY KEY, thing TEXT)")


@app.route("/")
def home_page():
    logging.info("Alguien entró a la página principal")
    return f"""<h1>{GREETING}</h1>
        <a href='/slow'>Una request lenta</a> |
        <a href='/error'>Una request que falla</a> |
        <a href='/save/hola/'>Guardar algo en la db</a> |
        <a href='/things'>Ver lo guardado</a>"""


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


@app.route("/save/<thing>/")
def save(thing):
    logging.info("Guardando en la db: %s", thing)
    run_sql("INSERT INTO things (thing) VALUES (%s)", thing)
    logging.info("%s guardado en la db", thing)
    return f"<h1>Guardado: {thing}</h1><a href='/things'>Ver lo guardado</a>"


@app.route("/things")
def things():
    logging.info("Contando cosas guardadas")
    rows = run_sql("SELECT thing FROM things ORDER BY id")
    logging.info("Mostrando %s cosas guardadas", len(rows))
    saved = "".join(f"<li>{thing}</li>" for (thing,) in rows)
    return f"<h1>Cosas guardadas</h1><ul>{saved}</ul><a href='/'>Volver</a>"


# el PaaS nos dice en qué puerto tenemos que escuchar, con la variable PORT
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
