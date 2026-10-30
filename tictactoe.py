"""Tic Tac Toe - Modificación 3 (versión final)

Determinar cuándo el juego terminó e indicar quién ganó o si se empató.
Incluye las tres modificaciones, marcadas con comentarios:

    MODIFICACIÓN 1: tamaño, color y centrado de X y O.
    MODIFICACIÓN 2: validar si una casilla ya está ocupada.
    MODIFICACIÓN 3: detectar ganador o empate.
"""

from turtle import *

from freegames import line

# MODIFICACIÓN 3 - NUEVO: esquinas (x, y) de las 3 columnas / 3 filas,
# son los mismos valores que devuelve floor().
COORDS = [-200, -67, 66]

# MODIFICACIÓN 3 - NUEVO: las 8 combinaciones ganadoras. Cada una es una
# tupla de 3 casillas (x, y): 3 filas, 3 columnas y 2 diagonales.
GANADORAS = (
    [tuple((cx, cy) for cx in COORDS) for cy in COORDS] +   # filas
    [tuple((cx, cy) for cy in COORDS) for cx in COORDS] +   # columnas
    [tuple((COORDS[i], COORDS[i]) for i in range(3)),       # diagonal /
     tuple((COORDS[i], COORDS[2 - i]) for i in range(3))]   # diagonal \
)


def grid():
    """Draw tic-tac-toe grid."""
    line(-67, 200, -67, -200)
    line(67, 200, 67, -200)
    line(-200, -67, 200, -67)
    line(-200, 67, 200, 67)


def drawx(x, y):
    """Draw X player."""
    # MODIFICACIÓN 1 - NUEVO: color azul y grosor 8
    color('blue')
    width(8)
    # MODIFICACIÓN 1 - NUEVO: centro de la casilla (esquina + 66.5)
    cx = x + 66.5
    cy = y + 66.5
    # MODIFICACIÓN 1 - NUEVO: tamaño de la X
    d = 40
    # MODIFICACIÓN 1 - MODIFICADO: se dibuja alrededor del centro
    line(cx - d, cy - d, cx + d, cy + d)
    line(cx - d, cy + d, cx + d, cy - d)


def drawo(x, y):
    """Draw O player."""
    # MODIFICACIÓN 1 - NUEVO: color rojo y grosor 8
    color('red')
    width(8)
    cx = x + 66.5
    cy = y + 66.5
    # MODIFICACIÓN 1 - NUEVO: radio de la O
    r = 48
    up()
    setheading(0)
    # MODIFICACIÓN 1 - MODIFICADO: circle() dibuja con el centro r unidades
    # arriba de la tortuga, por eso se baja r desde el centro de la casilla
    goto(cx, cy - r)
    down()
    circle(r)
    up()


def floor(value):
    """Round value down to grid with square size 133."""
    return ((value + 200) // 133) * 133 - 200


# MODIFICACIÓN 3 - MODIFICADO: se agrega 'over' para saber si el juego terminó
state = {'player': 0, 'over': False}
players = [drawx, drawo]
simbolos = ['X', 'O']

# MODIFICACIÓN 2 - NUEVO: casillas ya usadas.
# MODIFICACIÓN 3 - MODIFICADO: antes era un set; ahora es un diccionario
# {(x, y): 'X' u 'O'} para saber QUIÉN ocupa cada casilla y poder
# detectar combinaciones ganadoras.
ocupadas = {}

# MODIFICACIÓN 2 - NUEVO: tortuga auxiliar para escribir mensajes
mensaje = None


# MODIFICACIÓN 2 - NUEVO: mostrar un texto debajo del tablero
def escribir(texto, col='black'):
    """Muestra un mensaje debajo del tablero."""
    mensaje.clear()
    mensaje.color(col)
    mensaje.write(texto, align='center', font=('Arial', 16, 'bold'))
    update()


# MODIFICACIÓN 3 - NUEVO: devuelve la combinación ganadora o None
def ganador():
    """Busca tres símbolos iguales en alguna de las 8 combinaciones."""
    for combo in GANADORAS:
        a, b, c = [ocupadas.get(casilla) for casilla in combo]
        if a is not None and a == b == c:
            return combo
    return None


def tap(x, y):
    """Draw X or O in tapped square."""
    # MODIFICACIÓN 3 - NUEVO: si el juego terminó, ignorar los clics
    if state['over']:
        return

    # MODIFICACIÓN 2 - NUEVO: ignorar clics fuera del tablero
    if x < -200 or x > 200 or y < -200 or y > 200:
        return

    # MODIFICACIÓN 3 - MODIFICADO: min(..., 66) evita que un clic en el
    # borde derecho/superior (199-200) caiga en una cuarta casilla inexistente
    x = min(floor(x), 66)
    y = min(floor(y), 66)

    # MODIFICACIÓN 2 - NUEVO: validar si la casilla ya está ocupada
    if (x, y) in ocupadas:
        escribir('¡Casilla ocupada! Elige otra.', 'orange')
        return

    player = state['player']
    draw = players[player]
    draw(x, y)

    # MODIFICACIÓN 2 - NUEVO: registrar la casilla como ocupada
    # MODIFICACIÓN 3 - MODIFICADO: ahora se guarda el símbolo del jugador
    ocupadas[(x, y)] = simbolos[player]

    update()

    # MODIFICACIÓN 3 - NUEVO: verificar si hay un ganador
    combo = ganador()
    if combo:
        # Línea verde que une la primera y la última casilla ganadoras
        (x1, y1), (x2, y2) = combo[0], combo[2]
        color('green')
        width(10)
        line(x1 + 66.5, y1 + 66.5, x2 + 66.5, y2 + 66.5)
        update()
        escribir('¡Ganó ' + simbolos[player] + '!', 'green')
        state['over'] = True
        return

    # MODIFICACIÓN 3 - NUEVO: si las 9 casillas están llenas y nadie ganó
    if len(ocupadas) == 9:
        escribir('¡Empate!', 'purple')
        state['over'] = True
        return

    state['player'] = not player

    # MODIFICACIÓN 2 - NUEVO: indicar de quién es el turno
    escribir('Turno de ' + ('O' if state['player'] else 'X'))


# MODIFICACIÓN 2 - MODIFICADO: ventana más alta (470) para el mensaje
setup(420, 470, 370, 0)
hideturtle()
tracer(False)

# MODIFICACIÓN 2 - NUEVO: crear la tortuga de mensajes y mostrar el turno
mensaje = Turtle(visible=False)
mensaje.up()
mensaje.goto(0, -232)

grid()
escribir('Turno de X')
update()
onscreenclick(tap)
done()
