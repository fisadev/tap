# PaaS Demo

Una web mínima para deployar en un PaaS real. Usamos [Render](https://render.com), que tiene un plan gratuito que no pide tarjeta de crédito (los servicios gratuitos se "duermen" a los 15 minutos sin recibir requests, y tardan cerca de un minuto en despertar en la siguiente).

Ojo: el código de la demo **no está en la raíz del repo**, sino en la subcarpeta `paas_examples/`. Es lo normal cuando un repo tiene varias cosas adentro, y hay que avisarle al PaaS (ver abajo).

La app:

- Muestra un saludo que sale de la variable de entorno `GREETING`.
- Escucha en `0.0.0.0`, en el puerto que le indica el PaaS con la variable `PORT` (en Render, 10000 por defecto).
- Escribe logs a la salida estándar (con el módulo `logging`) en cada vista.
- Tiene `/slow` (tarda 2 segundos) y `/error` (falla con un 500), para tener algo que mirar en logs y métricas.
- Guarda textos en una base de datos Postgres: `/save/loquesea/` guarda, `/things` muestra lo guardado. La tabla se crea sola al arrancar la app.

## Probarla localmente (opcional)

Parados en esta carpeta (`paas_examples/`, la que tiene el Dockerfile):

```
docker build -t my_paas_web .
docker run --rm -p 5000:5000 my_paas_web
```

Sin `DATABASE_URL`, la app arranca igual: andan todas las vistas menos las dos que usan la db.

## Deployarla en Render

1. Crear una cuenta en Render (se puede entrar con GitHub).
2. En Render: New → Web Service → conectar la cuenta de GitHub y elegir el repo si es un repo privado, o usar la opción de Public Repository si es público.
3. Configurar:
   - **Language**: Docker (Render detecta el Dockerfile)
   - **Root Directory**: `paas_examples` ← sin esto, Render busca el Dockerfile en la raíz del repo y el deploy falla.
   - **Tipo de instancia**: Free
4. Deploy Web Service. Render construye la imagen, la corre, y en un rato nos da una URL con HTTPS.

El **Root Directory** hace dos cosas: todo lo demás (el Dockerfile, el contexto del build) se busca relativo a esa carpeta, y los deploys automáticos se disparan solo si el push toca archivos de adentro.

## Agregarle una base de datos

1. En Render: **+ New → Postgres**. Elegir un nombre, la **misma región** que el web service, y **Tipo de instancia**: Free.
2. Cuando esté lista, en la página de la db: sección **Connect → Internal Database URL**, y copiar esa URL.
   (La *internal* solo funciona entre servicios de Render de la misma región, y va por la red privada. La *external* es la que usaríamos para conectarnos desde afuera, por ejemplo desde nuestra máquina.)
3. En el web service: pestaña **Environment** → agregar la variable `DATABASE_URL` con esa URL → click en Save, Rebuild and Deploy.
4. Cuando termine el deploy, probar `/save/loquesea/` y `/things`.

⚠️ La Postgres gratuita de Render **expira a los 30 días** de creada (después hay 14 días para pasarla a un plan pago, y si no se borra). Además solo se puede tener **una** activa por workspace, con 1 GB y sin backups. Sirve para probar, no para algo que queramos conservar.

Cosas para probar una vez deployada:

- **Variables de entorno**: Environment → agregar `GREETING` con otro texto → click en Save, Rebuild and Deploy.
- **Logs**: pestaña Logs, mientras usamos la web (`/`, `/slow`, `/error`).
- **Métricas**: pestaña Metrics: CPU, memoria, bandwith, etc (algunas no se muestran con la instancia gratuita).
- **Deploy automático**: cambiar algo en `web.py`, hacer push a main, y mirar cómo se deploya solo. (Un push que toque solo archivos de afuera de `paas_examples/` no dispara nada.)
- **Rollback**: pestaña Deploys → botón **Rollback** en un deploy anterior. Ojo: al hacer rollback, Render desactiva los deploys automáticos (para que el próximo push no pise la vuelta atrás); se vuelven a activar en Settings.
