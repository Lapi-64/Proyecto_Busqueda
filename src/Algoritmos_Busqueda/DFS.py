import time
from Logica.Nodo import Nodo
def reconstruct_path(came_from, current: Nodo):

    length = 1
    while current in came_from:
        current = came_from[current]
        length += 1
        if not current.es_inicio and not current.es_meta:
            current.en_camino = True
    return length


def dfs(gestor, delay=0.4, draw_func=None):
    start = gestor.inicio
    goal = gestor.meta
    if start is None or goal is None:
        return False

    start_time = time.time()

    stack = [start]
    came_from = {}
    visited = {start}
    start.posible = True

    while stack:
        current = stack.pop()

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

        for vecino in current.get_vecinos():
            if vecino.es_obstaculo or vecino in visited:
                continue
            
            came_from[vecino] = current
            visited.add(vecino)
            vecino.posible = True
            stack.append(vecino)

    return False
