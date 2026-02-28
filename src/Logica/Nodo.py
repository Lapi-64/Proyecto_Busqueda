class Nodo:
    
    def __init__(self, x, y, tamaño=50):

        self.x = x
        self.y = y
        self.tamaño = tamaño
        self.visitado = False
        self.es_inicio = False
        self.es_meta = False
        self.es_obstaculo = False
        self.es_pantano = False
        self.es_desierto = False
        self.peso = 1
        self.en_camino = False
        self.posible = False
        self.vecinos = []
        
    def __eq__(self, other):
        return isinstance(other, Nodo) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def get_posicion_pixel(self, offset_x=0, offset_y=0):
        return (self.x * self.tamaño + offset_x, self.y * self.tamaño + offset_y)
    
    def get_rect(self, offset_x=0, offset_y=0):
        import pygame
        pos = self.get_posicion_pixel(offset_x, offset_y)
        return pygame.Rect(pos[0], pos[1], self.tamaño, self.tamaño)
    
    def contiene_punto(self, px, py, offset_x=0, offset_y=0):
        rect = self.get_rect(offset_x, offset_y)
        return rect.collidepoint(px, py)
    
    def reset(self):
        self.visitado = False
        self.en_camino = False
        self.posible = False
        if not self.es_inicio and not self.es_meta and not self.es_obstaculo and not self.es_pantano and not self.es_desierto:
            pass

    def agregar_vecino(self, nodo):
        if nodo not in self.vecinos:
            self.vecinos.append(nodo)

    def remover_vecino(self, nodo):
        if nodo in self.vecinos:
            self.vecinos.remove(nodo)

    def actualizar_vecinos(self, gestor):
        self.vecinos = []
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in direcciones:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < gestor.cols and 0 <= ny < gestor.filas:
                self.vecinos.append(gestor.nodos[ny][nx])

    def get_vecinos(self):
        return list(self.vecinos)
    
    def __repr__(self):
        return f"Nodo({self.x}, {self.y})"
