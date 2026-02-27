import heapq
import time
from Logica.Nodo import Nodo


def heuristic(a: Nodo, b: Nodo) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_neighbors(gestor, nodo: Nodo):
    vecinos = []
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dx, dy in direcciones:
        nx, ny = nodo.x + dx, nodo.y + dy
        if 0 <= nx < gestor.cols and 0 <= ny < gestor.filas:
            vecinos.append(gestor.nodos[ny][nx])
    return vecinos


def reconstruct_path(came_from, current: Nodo):
    length = 1
    while current in came_from:
        current = came_from[current]
        length += 1
        if not current.es_inicio and not current.es_meta:
            current.en_camino = True
    return length


def a_star(gestor, delay=0.4, draw_func=None):
    start = gestor.inicio
    goal = gestor.meta
    if start is None or goal is None:
        return False

    start_time = time.time()

    open_set = [] 
    counter = 0
    heapq.heappush(open_set, (0, counter, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    open_set_map = {start} 

    while open_set:
        _, _, current = heapq.heappop(open_set)
        open_set_map.discard(current)

        if current == goal:
            length = reconstruct_path(came_from, current)
            elapsed = time.time() - start_time
            return length, elapsed

        if not current.es_inicio and not current.es_meta:
            current.visitado = True
            current.posible = False
            if draw_func:
                draw_func()

        if delay > 0:
            if draw_func:
                import pygame
                pygame.event.pump()
                pygame.time.delay(int(delay * 1000))
            else:
                time.sleep(delay)

        for vecino in get_neighbors(gestor, current):
            if vecino.es_obstaculo:
                continue
            tentative_g = g_score.get(current, float("inf")) + 1

            if tentative_g < g_score.get(vecino, float("inf")):
                came_from[vecino] = current
                g_score[vecino] = tentative_g
                f_score[vecino] = tentative_g + heuristic(vecino, goal)
                if vecino not in open_set_map:
                    vecino.posible = True
                    counter += 1
                    heapq.heappush(open_set, (f_score[vecino], counter, vecino))
                    open_set_map.add(vecino)

    return False
