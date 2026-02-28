# Proyecto Búsqueda IA

Ventana interactiva para algoritmos de búsqueda.

## Algoritmos Implementados

### 1. **BFS (Búsqueda en Amplitud)**

Búsqueda **no informada** que explora el espacio por niveles. Garantiza encontrar el camino más corto (en número de pasos), pero es ineficiente porque explora celdas en todas las direcciones sin considerar la meta.

### 2. **DFS (Búsqueda en Profundidad)**

Búsqueda **no informada** que avanza lo máximo posible en una dirección antes de retroceder. No garantiza el camino más corto.

### 3. **Dijkstra**

Búsqueda **informada** que encuentra el camino de menor costo considerando pesos en los nodos. Explora primero los nodos con menor costo acumulado desde el inicio.

### 4. **A\* (A-Estrella)**

Búsqueda **informada** que combina el costo desde el inicio con una estimación heurística hacia la meta. Es la más eficiente porque guía la búsqueda directamente hacia el objetivo.

## ¿Por qué A\* visita menos nodos que BFS?

BFS expande los nodos como un círculo que crece uniformemente desde el inicio, sin saber donde esta la meta BFS debe explorar todos los nodos dibujando ese circulo, en cambio A\* usa la distancia Manhattan (|dx| + |dy|) para estimar cuántos pasos faltan hasta la meta. Esto hace que priorice explorar celdas que están en la dirección correcta. Por ello, A\* es más eficiente porque la heurística le permite "saber" qué dirección seguir, mientras que BFS debe explorar uniformemente en todas las direcciones.

### Controles

1. **Inicio**: Marca el punto de partida
2. **Meta**: Marca el punto destino
3. **Obstáculo**: Dibuja paredes
4. **Pantano**: Terreno con peso 5 - más lento
5. **Desierto**: Terreno con peso 10 - mucho más lento
6. **A\* / BFS / DFS / Dijkstra**: Ejecuta el algoritmo seleccionado
7. **Reiniciar**: Limpia la búsqueda actual

### Colores

- Azul: Punto de inicio
- Púrpura: Punto meta
- Negro: Obstáculos
- Verde oscuro: Pantano
- Naranja: Desierto
- Rojo: Nodos visitados
- Amarillo: Camino solución
  - Amarillo oscuro: Camino en pantano
  - Amarillo muy oscuro: Camino en desierto
- Verde: Posibles nodos a explorar

## Requisitos

- Python 3.12.10
- pygame 2.6.1
- tkinter(iene con python)

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python src/Main.py
```
