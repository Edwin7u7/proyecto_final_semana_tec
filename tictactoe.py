"""Tic Tac Toe - Modificación 2

Validar si una casilla ya se encuentra ocupada.
(Incluye la modificación 1: X y O con color, tamaño y centradas.)

Los comentarios "MODIFICACIÓN 2" marcan lo nuevo respecto a tictactoe_1.py.
"""

from turtle import *

from freegames import line


def grid():
    """Draw tic-tac-toe grid."""
    line(-67, 200, -67, -200)
    line(67, 200, 67, -200)
    line(-200, -67, 200, -67)
    line(-200, 67, 200, 67)


def drawx(x, y):
    """Draw X player (modificación 1)."""
    color('blue')
    width(8)
    cx = x + 66.5
    cy = y + 66.5
    d = 40
    line(cx - d, cy - d, cx + d, cy + d)
    line(cx - d, cy + d, cx + d, cy - d)


def drawo(x, y):
    """Draw O player (modificación 1)."""
    color('red')
    width(8)
    cx = x + 66.5
    cy = y + 66.5
    r = 48
    up()
    setheading(0)
    goto(cx, cy - r)
    down()
    circle(r)
    up()


def floor(value):
    """Round value down to grid with square size 133."""
    return ((value + 200) // 133) * 133 - 200


state = {'player': 0}
players = [drawx, drawo]

# MODIFICACIÓN 2 - NUEVO: conjunto con las casillas ya usadas.
# Cada casilla se identifica por la esquina (x, y) que devuelve floor().
ocupadas = set()

# MODIFICACIÓN 2 - NUEVO: tortuga auxiliar para escribir mensajes
# debajo del tablero (se crea más abajo, antes de iniciar el juego).
mensaje = None


# MODIFICACIÓN 2 - NUEVO: función para mostrar un texto debajo del tablero.
def escribir(texto, col='black'):
    """Muestra un mensaje debajo del tablero."""
    mensaje.clear()
    mensaje.color(col)
    mensaje.write(texto, align='center', font=('Arial', 16, 'bold'))
    update()


def tap(x, y):
    """Draw X or O in tapped square."""
    # MODIFICACIÓN 2 - NUEVO: ignorar clics fuera del tablero
    if x < -200 or x > 200 or y < -200 or y > 200:
        return

    x = floor(x)
    y = floor(y)

    # MODIFICACIÓN 2 - NUEVO: validar si la casilla ya está ocupada.
    # Si lo está, se avisa y se sale sin dibujar ni cambiar de turno.
    if (x, y) in ocupadas:
        escribir('¡Casilla ocupada! Elige otra.', 'orange')
        return

    player = state['player']
    draw = players[player]
    draw(x, y)

    # MODIFICACIÓN 2 - NUEVO: registrar la casilla como ocupada
    ocupadas.add((x, y))

    update()
    state['player'] = not player

    # MODIFICACIÓN 2 - NUEVO: indicar de quién es el turno
    escribir('Turno de ' + ('O' if state['player'] else 'X'))


# MODIFICACIÓN 2 - MODIFICADO: ventana más alta (470 en lugar de 420)
# para que quepa el mensaje debajo del tablero.
setup(420, 470, 370, 0)
hideturtle()
tracer(False)

# MODIFICACIÓN 2 - NUEVO: crear la tortuga de mensajes y mostrar el primer turno
mensaje = Turtle(visible=False)
mensaje.up()
mensaje.goto(0, -232)

grid()
escribir('Turno de X')
update()
onscreenclick(tap)
done()
