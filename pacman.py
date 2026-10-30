"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.
"""

from random import choice
from turtle import *
from freegames import floor, vector

# Estado global del juego para almacenar la puntuación
state = {'score': 0}

# Instancias de Turtle ocultas:
# 'path' se usa para dibujar el mapa/tablero y el alimento
# 'writer' se usa para renderizar el puntaje en la pantalla
path = Turtle(visible=False)
writer = Turtle(visible=False)

# Vector de movimiento inicial de Pacman (se mueve 5 unidades a la derecha)
aim = vector(5, 0)

# Posición inicial de Pacman en el sistema de coordenadas
pacman = vector(-40, -80)

# Lista con los fantasmas: cada elemento contiene [Posición Inicial, Vector de Dirección]
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

# fmt: off
# Matriz del tablero de 20x20 casillas (400 elementos en total)
# 0 = Pared sólida (bloque gris/azul)
# 1 = Pasillo con alimento (cuadrado verde)
# 2 = Pasillo ya comido / despejado
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0,
    0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0,
    0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0,
    0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0,
    0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0,
    0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: on


def square(x, y, size=20):
    """Dibuja un cuadrado relleno de un tamaño determinado en la posición (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    # Dibuja los cuatro lados del cuadrado
    for count in range(4):
        path.forward(size)
        path.left(90)

    path.end_fill()


def offset(point):
    """Calcula el índice equivalente en la lista 'tiles' para un punto (x, y) de la pantalla."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    """Verifica si una coordenada propuesta es transitable (no es pared ni está fuera de límites)."""
    index = offset(point)

    # Si el tile en ese punto es pared (0), no es válido
    if tiles[index] == 0:
        return False

    # Evalúa la esquina opuesta del sprite (19 píxeles más adelante)
    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    # Valida que el movimiento esté alineado a la rejilla de 20 píxeles
    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Dibuja la estructura inicial del tablero y el nuevo alimento (cuadrados verdes)."""
    bgcolor('black')

    # Recorre los 400 elementos del tablero
    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            # Convierte el índice de la lista a coordenadas de pantalla (x, y)
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            
            # Dibuja la pared/pasillo en azul
            path.color('blue')
            square(x, y, 20)

            # Dibuja el alimento: un cuadrado pequeño de color verde (tamaño 6x6 píxeles)
            if tile == 1:
                path.color('green')
                square(x + 7, y + 7, 6)


def move():
    """Actualiza la posición de Pacman, los fantasmas, la puntuación y el estado del juego."""
    # Actualiza la puntuación en la pantalla
    writer.undo()
    writer.write(state['score'])

    clear()  # Limpia los dibujos del fotograma anterior

    # Avanza a Pacman si la posición siguiente es válida
    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    # Si Pacman está sobre un alimento (1), lo come y suma puntos
    if tiles[index] == 1:
        tiles[index] = 2  # Cambia a piso comido
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        path.color('blue')
        square(x, y, 20)  # Redibuja el cuadro azul sin el alimento verde

    # Dibuja a Pacman (punto amarillo)
    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    # Mueve cada uno de los fantasmas
    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            # Si choca contra una pared, elige una dirección al azar
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        # Dibuja al fantasma (punto rojo)
        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()  # Refresca la ventana con los nuevos dibujos

    # Detección de colisión entre Pacman y cualquier fantasma
    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return  # Termina el juego si un fantasma atrapa a Pacman

    # Programa la ejecución del siguiente fotograma en 100 milisegundos
    ontimer(move, 100)


def change(x, y):
    """Cambia la dirección del movimiento de Pacman si el camino es válido."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


# Configuración de la ventana y eventos iniciales
setup(420, 420, 370, 0)
hideturtle()
tracer(False)  # Desactiva la animación automática para renderizar fotogramas manualmente

# Configura el texto del marcador
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])

# Mapeo de controles por teclado (flechas de dirección)
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')

# Arranca el juego dibujando el mundo y ejecutando el bucle de movimiento
world()
move()
done()
