"""Tic Tac Toe - Modificación 1

Cambiar tamaño y color de la X y la O, y centrarlas en la casilla.
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
    """Draw X player centrada en la casilla, azul y gruesa."""
    color('blue')   # color de la X
    width(8)        # grosor de la X

    # (x, y) es la esquina inferior izquierda de la casilla,
    # así que el centro está medio cuadro (66.5) hacia arriba y a la derecha.
    cx = x + 66.5
    cy = y + 66.5
    d = 40          # tamaño: mitad de la longitud de cada trazo

    line(cx - d, cy - d, cx + d, cy + d)
    line(cx - d, cy + d, cx + d, cy - d)


def drawo(x, y):
    """Draw O player centrada en la casilla, roja y gruesa."""
    color('red')    # color de la O
    width(8)        # grosor de la O

    cx = x + 66.5
    cy = y + 66.5
    r = 48          # tamaño: radio del círculo

    up()
    setheading(0)
    # circle() dibuja el círculo con su centro r unidades ARRIBA de la
    # tortuga, por eso se baja r unidades desde el centro de la casilla.
    goto(cx, cy - r)
    down()
    circle(r)
    up()


def floor(value):
    """Round value down to grid with square size 133."""
    return ((value + 200) // 133) * 133 - 200


state = {'player': 0}
players = [drawx, drawo]


def tap(x, y):
    """Draw X or O in tapped square."""
    x = floor(x)
    y = floor(y)
    player = state['player']
    draw = players[player]
    draw(x, y)
    update()
    state['player'] = not player


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
grid()
update()
onscreenclick(tap)
done()
