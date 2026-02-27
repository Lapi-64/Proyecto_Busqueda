class Nodo:
    
    def __init__(self, x, y, tamaño=50):

        self.x = x
        self.y = y
        self.tamaño = tamaño
        self.visitado = False
        self.es_inicio = False
        self.es_meta = False
        self.es_obstaculo = False
        self.en_camino = False
        
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
        if not self.es_inicio and not self.es_meta and not self.es_obstaculo:
            pass
    
    def __repr__(self):
        return f"Nodo({self.x}, {self.y})"
