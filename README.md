# proyecto_final_semana_tec
Proyecto final  "Herramientas computacionales : El arte de la programación"

## Edwin Arturo Salgado Santana
##
##



# Juegos
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
