# esto es un ejemplo muy primitivo de cómo se podría hacer código
# async usando solo generadores. No hacer cosas así en prod! Es solo
# educativo
from time import sleep


def estudiar():
    print("e: leer material")
    yield
    print("e: leer material")
    yield
    print("e: leer material")
    yield
    print("e: resaltar ideas importantes")
    print("e: hacer resumen")
    yield
    print("e: recitar")
    yield
    print("e: llorar")


def subir_foto():
    print("subir unos bytes")
    yield
    print("subir unos bytes")
    yield
    print("subir unos bytes")
    yield
    print("subir unos bytes")
    yield
    print("subir unos bytes")


def twitter():
    print("t: abrir la app")
    yield
    print("t: scroll")
    yield
    print("t: scroll")
    yield
    print("t: discutir de política")
    yield
    print("t: postear una foto")
    yield from subir_foto()
    print("t: scroll")
    yield
    print("t: scroll")
    yield
    print("t: indignarme")
    yield
    print("t: scroll")
    yield
    print("t: scroll")
    yield
    print("t: scroll")


def loop(tareas):
    print("Inicio")
    while tareas:
        tarea_actual = tareas.pop(0)

        try:
            next(tarea_actual)
            tareas.append(tarea_actual)
        except StopIteration:
            pass
    print("Fin")


loop([estudiar(), twitter()])
