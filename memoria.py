"""Memory, juego de memoria con pares de números.

Cambio añadido: contar y desplegar el número de pares descubiertos.
"""

# Importamos lo necesario:
# - random: para revolver las fichas
# - turtle: para dibujar en la ventana
# - freegames: para obtener la imagen del carro
from random import *
from turtle import *

from freegames import path

# Imagen que aparece debajo de las fichas
car = path('car.gif')

# Lista de fichas: los números del 0 al 31, cada uno repetido dos veces (64 fichas)
tiles = list(range(32)) * 2

# Estado del juego:
# - 'mark': la ficha que el jugador tocó primero (None si no hay ninguna)
# - 'pairs': cuántos pares lleva descubiertos
state = {'mark': None, 'pairs': 0}

# Indica si cada ficha está tapada (True) o descubierta (False)
# Al inicio todas están tapadas
hide = [True] * 64


def square(x, y):
    """Dibuja un cuadro blanco con borde negro en la posición (x, y)."""
    up()            # Levanta el lápiz para moverse sin dibujar
    goto(x, y)      # Se mueve a la esquina del cuadro
    down()          # Baja el lápiz para empezar a dibujar
    color('black', 'white')  # Borde negro, relleno blanco
    begin_fill()
    # Dibuja los 4 lados del cuadro (cada lado mide 50)
    for count in range(4):
        forward(50)
        left(90)
    end_fill()


def index(x, y):
    """Convierte las coordenadas de un clic (x, y) en el número de ficha (0 a 63)."""
    # El tablero va de -200 a 200; cada ficha mide 50 y hay 8 por fila
    return int((x + 200) // 50 + ((y + 200) // 50) * 8)


def xy(count):
    """Convierte el número de ficha en sus coordenadas (x, y) en pantalla."""
    # count % 8  -> columna de la ficha
    # count // 8 -> fila de la ficha
    return (count % 8) * 50 - 200, (count // 8) * 50 - 200


def tap(x, y):
    """Se ejecuta cada vez que el jugador hace clic."""
    # Si el clic fue fuera del tablero, no hacemos nada
    if not (-200 <= x < 200 and -200 <= y < 200):
        return

    # Averiguamos qué ficha se tocó
    spot = index(x, y)

    # Si esa ficha ya estaba descubierta, la ignoramos
    # (así no se cuenta el mismo par dos veces)
    if not hide[spot]:
        return

    # Ficha que se había tocado antes
    mark = state['mark']

    # Casos en los que NO se forma un par:
    # - es la primera ficha que se toca
    # - se tocó la misma ficha otra vez
    # - las dos fichas tienen números distintos
    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot  # Guardamos esta ficha como la "marcada"
    else:
        # ¡Se encontró un par! Destapamos ambas fichas
        hide[spot] = False
        hide[mark] = False
        state['mark'] = None  # Ya no hay ficha marcada

        # Sumamos 1 al contador de pares y lo mostramos en la consola
        state['pairs'] += 1
        print('Pares descubiertos:', state['pairs'])


def draw():
    """Dibuja todo el juego: la imagen, las fichas y el contador."""
    clear()  # Borra lo que había antes en la pantalla

    # Dibuja la imagen del carro en el centro
    goto(0, 0)
    shape(car)
    stamp()

    # Dibuja un cuadro encima de cada ficha que siga tapada
    for count in range(64):
        if hide[count]:
            x, y = xy(count)
            square(x, y)

    # Si hay una ficha marcada, mostramos su número
    mark = state['mark']

    if mark is not None and hide[mark]:
        x, y = xy(mark)
        up()
        goto(x + 2, y)
        color('black')
        write(tiles[mark], font=('Arial', 30, 'normal'))

    # Muestra el contador de pares arriba del tablero
    up()
    goto(-200, 205)
    color('black')
    write(f"Pares descubiertos: {state['pairs']} / 32",
          font=('Arial', 14, 'normal'))

    update()               # Refresca la pantalla
    ontimer(draw, 100)     # Vuelve a dibujar cada 100 milisegundos


# ---------- Inicio del juego ----------
shuffle(tiles)               # Revuelve las fichas
setup(420, 480, 370, 0)      # Tamaño de la ventana (más alta para que quepa el contador)
addshape(car)                # Registra la imagen del carro
hideturtle()                 # Oculta la tortuga (el cursor que dibuja)
tracer(False)                # Desactiva la animación para dibujar más rápido
onscreenclick(tap)           # Cada clic llama a la función tap
draw()                       # Empieza a dibujar el juego
done()                       # Mantiene la ventana abierta
