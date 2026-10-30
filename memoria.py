"""Memory, juego de memoria con pares de números.

Cambios añadidos:
1. Contar y desplegar el número de pares descubiertos.
2. Detectar cuando todos los cuadros se han destapado.
3. Cambiar el número de casillas del tablero.
"""

# Importamos lo necesario:
# - random: para revolver las fichas
# - turtle: para dibujar en la ventana
# - freegames: para obtener la imagen del carro
from random import *
from turtle import *

from freegames import path

# ---------- Configuración del tablero ----------
# SIZE es el número de casillas por lado (el tablero es de SIZE x SIZE).
# Cambia este número para hacer el tablero más grande o más chico.
# Debe ser un número PAR (2, 4, 6, 8...) para que todas las fichas tengan pareja.
SIZE = 4

# Tamaño de cada casilla en pixeles
TILE = 50

# Total de casillas y total de pares que hay en el tablero
TOTAL = SIZE * SIZE
PAIRS = TOTAL // 2

# Mitad del ancho del tablero; sirve para centrarlo en la pantalla
HALF = SIZE * TILE // 2

# Imagen que aparece debajo de las fichas
car = path('car.gif')

# Lista de fichas: cada número aparece dos veces (para formar pares)
tiles = list(range(PAIRS)) * 2

# Estado del juego:
# - 'mark': la ficha que el jugador tocó primero (None si no hay ninguna)
# - 'pairs': cuántos pares lleva descubiertos
# - 'won': si ya se destaparon todos los cuadros (True) o no (False)
state = {'mark': None, 'pairs': 0, 'won': False}

# Indica si cada ficha está tapada (True) o descubierta (False)
# Al inicio todas están tapadas
hide = [True] * TOTAL


def square(x, y):
    """Dibuja un cuadro blanco con borde negro en la posición (x, y)."""
    up()            # Levanta el lápiz para moverse sin dibujar
    goto(x, y)      # Se mueve a la esquina del cuadro
    down()          # Baja el lápiz para empezar a dibujar
    color('black', 'white')  # Borde negro, relleno blanco
    begin_fill()
    # Dibuja los 4 lados del cuadro
    for count in range(4):
        forward(TILE)
        left(90)
    end_fill()


def index(x, y):
    """Convierte las coordenadas de un clic (x, y) en el número de ficha."""
    # El tablero va de -HALF a HALF; hay SIZE fichas por fila
    return int((x + HALF) // TILE + ((y + HALF) // TILE) * SIZE)


def xy(count):
    """Convierte el número de ficha en sus coordenadas (x, y) en pantalla."""
    # count % SIZE  -> columna de la ficha
    # count // SIZE -> fila de la ficha
    return (count % SIZE) * TILE - HALF, (count // SIZE) * TILE - HALF


def all_revealed():
    """Regresa True si ya no queda ningún cuadro tapado."""
    # hide tiene True en los cuadros tapados.
    # Si ninguno es True, significa que todos se destaparon.
    return not any(hide)


def tap(x, y):
    """Se ejecuta cada vez que el jugador hace clic."""
    # Si el juego ya terminó, ignoramos los clics
    if state['won']:
        return

    # Si el clic fue fuera del tablero, no hacemos nada
    if not (-HALF <= x < HALF and -HALF <= y < HALF):
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

        # Revisamos si con este par ya se destaparon todos los cuadros
        if all_revealed():
            state['won'] = True
            print('¡Ganaste! Destapaste todos los cuadros.')


def draw():
    """Dibuja todo el juego: la imagen, las fichas y el contador."""
    clear()  # Borra lo que había antes en la pantalla

    # Dibuja la imagen del carro en el centro
    goto(0, 0)
    shape(car)
    stamp()

    # Dibuja un cuadro encima de cada ficha que siga tapada
    for count in range(TOTAL):
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
    goto(-HALF, HALF + 5)
    color('black')
    write(f"Pares descubiertos: {state['pairs']} / {PAIRS}",
          font=('Arial', 14, 'normal'))

    # Si ya se destaparon todos los cuadros, mostramos un mensaje de victoria
    if state['won']:
        up()
        goto(0, 0)
        color('red')
        write('¡Ganaste!', align='center', font=('Arial', 40, 'bold'))

    update()               # Refresca la pantalla
    ontimer(draw, 100)     # Vuelve a dibujar cada 100 milisegundos


# ---------- Inicio del juego ----------
shuffle(tiles)               # Revuelve las fichas

# El tamaño de la ventana se ajusta al tamaño del tablero
# (+20 de margen a los lados y +80 de alto para que quepa el contador)
setup(SIZE * TILE + 20, SIZE * TILE + 80, 370, 0)

addshape(car)                # Registra la imagen del carro
hideturtle()                 # Oculta la tortuga (el cursor que dibuja)
tracer(False)                # Desactiva la animación para dibujar más rápido
onscreenclick(tap)           # Cada clic llama a la función tap
draw()                       # Empieza a dibujar el juego
done()                       # Mantiene la ventana abierta
