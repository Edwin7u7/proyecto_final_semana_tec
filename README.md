# proyecto_final_semana_tec
Proyecto final  "Herramientas computacionales : El arte de la programación"

## Edwin Arturo Salgado Santana
## Hector Jesus Carrillo Cano
##



# Juegos
# Pacman
Una versión modificada del clásico juego Pacman desarrollado en Python utilizando la librería freegames e interfaz gráfica turtle.

---

## Modificaciones Realizadas

Se aplicaron diversos cambios sobre la base original del juego para personalizar el mapa, los gráficos y ajustar la dificultad:

### 1. Rediseño del Tablero (tiles)
- Se reestructuró la matriz global de 20x20 casillas para crear nuevos pasillos y bloques de paredes.
- Se mantuvieron los bordes cerrados (0) para evitar que las entidades salgan de la pantalla.
- Se aseguraron los puntos de aparición iniciales para Pacman y los fantasmas sobre rutas transitables (1).

### 2. Cambio de Forma y Color del Alimento
- Forma: Se sustituyó el punto circular tradicional (dot) por un cuadrado relleno de 6x6 píxeles mediante una función square parametrizada.
- Color: Se cambió el color blanco original por un verde brillante ('green') para darle un estilo visual distinto.
- Lógica de recolección: Se actualizó el evento de colisión para que, al comer un alimento, se limpie el área redibujando la celda con el color del pasillo ('blue').

### 3. Incremento en la Velocidad de los Fantasmas
- Mayor paso de movimiento: Se introdujo la variable global GHOST_SPEED = 10, duplicando la distancia de desplazamiento por paso respecto a los 5 píxeles originales.
- Temporizador acelerado: Se redujo el tiempo de actualización del ciclo de juego en ontimer(move, 50), pasando de 100 ms a 50 ms entre fotogramas.
- Manejo de rebotes: Al chocar contra paredes, la reorientación aleatoria de cada fantasma asigna direcciones acordes a su nueva velocidad.

### 4. Comentarios y Documentación en Código
- Se añadieron comentarios explicativos paso a paso a lo largo de todo el script en español, detallando:
  - Estructuras de datos (state, tiles, ghosts).
  - Lógica matemática de conversión de coordenadas (offset).
  - Funciones de validación de colisiones y bucle principal de juego.

---

## Requisitos e Instalación

### Prerrequisitos
- Python 3.x instalado.

### Librerías requeridas
Instala la dependencia freegames ejecutando en tu terminal:

```bash
pip install freegames
# Memoria
Juego de memoria hecho con `turtle` y `freegames`. El jugador destapa casillas de dos en dos; si los números coinciden, el par queda descubierto y se va revelando la imagen del carro que está debajo.
## Requisitos
 
- Python 3
- La librería `freegames`:
```bash
pip install freegames
```
 
## Cómo ejecutarlo
 
```bash
python memory.py
```
 
---
 
## Modificaciones realizadas
 
### 1. Contar y desplegar el número de pares descubiertos
 
- Se agregó el campo `'pairs'` al diccionario `state`, que empieza en `0`.
- En la función `tap()`, cada vez que se encuentra un par se suma 1 a `state['pairs']`. Ese número también se imprime en la consola.
- En la función `draw()`, se escribe arriba del tablero el texto `Pares descubiertos: N / total`.
- Para que el contador cupiera, la ventana se hizo más alta que el tablero.
**Correcciones que se agregaron junto con este cambio:**
 
- Se ignoran los clics **fuera del tablero**. Antes, un clic en la nueva franja del contador causaba un error de índice.
- Se ignoran los clics en **casillas ya descubiertas**. Así un mismo par no se cuenta dos veces.
### 2. Detectar cuando todos los cuadros se han destapado
 
- Se agregó el campo `'won'` a `state`, que empieza en `False`.
- Se creó la función `all_revealed()`, que regresa `True` cuando ya no queda ninguna casilla tapada (`not any(hide)`).
- En `tap()`, después de encontrar un par, se revisa `all_revealed()`. Si es verdad, `state['won']` cambia a `True` y se imprime "¡Ganaste!" en la consola.
- En `draw()`, cuando `state['won']` es `True`, aparece el mensaje **"¡Ganaste!"** en rojo en el centro de la pantalla.
- Una vez ganado el juego, los clics se ignoran.
### 3. Cambiar el número de casillas del tablero
 
- Se agregó la variable `SIZE` al inicio del archivo. Indica cuántas casillas tiene el tablero por lado (el tablero es de `SIZE x SIZE`). Por defecto vale `4`.
- **`SIZE` debe ser un número par** (2, 4, 6, 8...) para que todas las fichas tengan pareja.
- A partir de `SIZE` se calculan otros valores:
| Variable | Significado |
|----------|-------------|
| `TILE`   | Tamaño de cada casilla en pixeles (50) |
| `TOTAL`  | Número total de casillas (`SIZE * SIZE`) |
| `PAIRS`  | Número total de pares (`TOTAL // 2`) |
| `HALF`   | Mitad del ancho del tablero, para centrarlo |
 
- Las listas `tiles` y `hide` ahora se crean con `PAIRS` y `TOTAL` en lugar de los números fijos 32 y 64.
- Las funciones `index()`, `xy()` y `square()` usan `SIZE`, `TILE` y `HALF` en lugar de los valores fijos 8, 50 y 200.
- El contador muestra el total correcto de pares, por ejemplo `/ 8` en un tablero de 4x4.
- El tamaño de la ventana se ajusta automáticamente al tablero.
