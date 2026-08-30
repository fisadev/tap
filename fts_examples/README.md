# Demo: Full Text Search en PostgreSQL

## Preparacion

Un solo comando levanta un Postgres descartable y nos deja adentro de la
consola. Al salir con `\q` el container se borra solo, sin dejar nada:

```bash
docker run --rm -it -e POSTGRES_HOST_AUTH_METHOD=trust postgres:16 \
    bash -c 'docker-entrypoint.sh postgres >/dev/null 2>&1 & until pg_isready -q; do sleep 1; done; psql -U postgres'
```

(conviene bajar la imagen antes de la clase, con `docker pull postgres:16`)

Todo lo que sigue se copia y pega en esa consola.

## 1. La tabla

Creamos una tabla de productos, con un campo extra que junta el texto de los
dos campos que nos interesa buscar, y un indice sobre ese campo:

```sql
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    descripcion TEXT,
    precio NUMERIC,
    texto_indexado tsvector GENERATED ALWAYS AS (
        to_tsvector('spanish', nombre || ' ' || descripcion)
    ) STORED
);

CREATE INDEX productos_busqueda_idx ON productos USING GIN (texto_indexado);
```

El índice "GIN" es el tipo de índice que vimos en los ejemplos de la teoría.

## 2. Los datos

Pegar el contenido de `datos.sql`: 12 productos de un e-commerce de running.

## 3. Las busquedas

Para buscar tenemos que procesar el texto que el usuario ingrese usando `websearch_to_tsquery`: 
esta función se encarga de separar en palabras, extraer las raíces, quitar stopwords, etc.

### "maratón"

Si intentamos usar ILIKE para la búsqueda:

```sql
SELECT id, nombre FROM productos
WHERE nombre ILIKE '%maratón%' OR descripcion ILIKE '%maratón%';
```

Nos trae solo 2 resultados. Otros 3 productos con "maratones" o "maratonista" son ignorados.

Pero en cambio, usando el motor de búsqueda de texto completo:

```sql
SELECT id, nombre FROM productos
WHERE texto_indexado @@ websearch_to_tsquery('spanish', 'maratón');
```

Nos trae 5 productos, todos relevantes.

### "zapatillas para correr maratones"

```sql
SELECT id, nombre FROM productos
WHERE texto_indexado @@ websearch_to_tsquery('spanish', 'zapatillas para correr maratones');
```

Trae las 2 zapatillas maratonistas. 
El "para" se ignoró por ser stopword, y el "correr" está siendo ignorado también porque en 
nuestra db no aporta nada de información (casi todo es para correr).

Si buscamos solo zapatillas maratonistas, vemos lo mismo:

```sql
SELECT id, nombre FROM productos
WHERE texto_indexado @@ websearch_to_tsquery('spanish', 'zapatillas maratonistas');
```
