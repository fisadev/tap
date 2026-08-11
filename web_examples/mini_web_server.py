import socket

# creamos un socket que escucha conexiones TCP en el puerto 5000
servidor = socket.create_server(("localhost", 5000))
print("Escuchando en http://localhost:5000")

while True:
    # esperamos a que alguien se conecte, y leemos lo que nos manda
    conexion, direccion = servidor.accept()
    pedido = conexion.recv(4096).decode()
    print(pedido)

    # la primera linea del pedido HTTP es algo como: "GET /hola HTTP/1.1"
    primera_linea = pedido.split("\r\n")[0]
    metodo, uri, version = primera_linea.split(" ")

    # armamos el html de la respuesta
    html = f"<html><body><h1>Me llamaste con metodo {metodo} y uri {uri}</h1></body></html>"

    # y armamos la respuesta HTTP completa: linea de estado, headers, linea en
    # blanco, y recien ahi el contenido
    respuesta = (
        f"HTTP/1.1 200 OK\r\n"
        f"Content-Type: text/html\r\n"
        f"Content-Length: {len(html)}\r\n"
        f"\r\n"
        f"{html}"
    )

    conexion.sendall(respuesta.encode())
    conexion.close()
