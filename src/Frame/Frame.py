import pygame
import sys
from Logica.Nodo import Nodo

ANCHO_VENTANA = 1000
ALTO_VENTANA = 700
TAMAÑO_CELDA = 50
CANTIDAD_COLUMNAS = (ANCHO_VENTANA - 200) // TAMAÑO_CELDA
CANTIDAD_FILAS = ALTO_VENTANA // TAMAÑO_CELDA
OFFSET_X = 10
OFFSET_Y = 10

COLOR_FONDO = (240, 240, 240)
COLOR_LINEA = (200, 200, 200)
COLOR_CELDA = (255, 255, 255)
COLOR_VISITADO = (173, 216, 230)
COLOR_CAMINO = (0, 255, 0)
COLOR_INICIO = (0, 0, 255)
COLOR_META = (255, 0, 0)
COLOR_OBSTACULO = (0, 0, 0)
COLOR_TEXTO = (50, 50, 50)
COLOR_BOTON = (200, 200, 200)
COLOR_BOTON_HOVER = (180, 180, 180)


class GestorGrid:
    def __init__(self, colum, filas, tamaño_celda):
        self.cols = colum
        self.filas = filas
        self.tamaño_celda = tamaño_celda
        self.nodos = [[Nodo(x, y, tamaño_celda) for x in range(colum)] for y in range(filas)]
        self.modo_actual = "normal"  # normal, inicio, meta, obstaculo
        self.inicio = None
        self.meta = None
        
    def obtener_nodo_en_punto(self, px, py):
        """Obtiene el nodo en una posición de píxeles"""
        px_relativo = px - OFFSET_X
        py_relativo = py - OFFSET_Y
        
        if px_relativo < 0 or py_relativo < 0:
            return None
            
        x = px_relativo // self.tamaño_celda
        y = py_relativo // self.tamaño_celda
        
        if 0 <= x < self.cols and 0 <= y < self.filas:
            return self.nodos[y][x]
        return None
    
    def set_modo(self, modo):
        """Cambia el modo actual"""
        self.modo_actual = modo
    
    def procesar_clic(self, px, py):
        """Procesa un clic del ratón"""
        nodo = self.obtener_nodo_en_punto(px, py)
        if not nodo:
            return
        
        if self.modo_actual == "inicio":
            if self.inicio:
                self.inicio.es_inicio = False
            nodo.es_inicio = True
            self.inicio = nodo
            
        elif self.modo_actual == "meta":
            if self.meta:
                self.meta.es_meta = False
            nodo.es_meta = True
            self.meta = nodo
            
        elif self.modo_actual == "obstaculo":
            if not nodo.es_inicio and not nodo.es_meta:
                nodo.es_obstaculo = not nodo.es_obstaculo
    
    def resetear(self):
        """Resetea el grid"""
        for fila in self.nodos:
            for nodo in fila:
                nodo.reset()
    
    def resetear_todo(self):
        """Resetea el grid completamente"""
        self.inicio = None
        self.meta = None
        for fila in self.nodos:
            for nodo in fila:
                nodo.visitado = False
                nodo.es_inicio = False
                nodo.es_meta = False
                nodo.es_obstaculo = False
                nodo.en_camino = False


class InterfazGrid:
    """Interfaz gráfica del grid"""
    
    def __init__(self, ancho, alto):
        self.pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Editor de Grid - Búsqueda IA")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 24)
        self.fuente_pequeña = pygame.font.Font(None, 18)
        
        self.gestor = GestorGrid(CANTIDAD_COLUMNAS, CANTIDAD_FILAS, TAMAÑO_CELDA)
        self.botones = self._crear_botones()
        self.ejecutando = True
    
    def _crear_botones(self):
        """Crea los botones de la interfaz"""
        botones = {}
        x_inicio = ANCHO_VENTANA - 180
        y_inicio = 20
        ancho_boton = 170
        alto_boton = 35
        espaciado = 10
        
        botones["inicio"] = {
            "rect": pygame.Rect(x_inicio, y_inicio, ancho_boton, alto_boton),
            "texto": "Inicio",
            "accion": lambda: self.gestor.set_modo("inicio"),
            "activo": False
        }
        
        botones["meta"] = {
            "rect": pygame.Rect(x_inicio, y_inicio + alto_boton + espaciado, ancho_boton, alto_boton),
            "texto": "Meta",
            "accion": lambda: self.gestor.set_modo("meta"),
            "activo": False
        }
        
        botones["obstaculo"] = {
            "rect": pygame.Rect(x_inicio, y_inicio + 2*(alto_boton + espaciado), ancho_boton, alto_boton),
            "texto": "Obstáculo",
            "accion": lambda: self.gestor.set_modo("obstaculo"),
            "activo": False
        }
        
        botones["a_star"] = {
            "rect": pygame.Rect(x_inicio, y_inicio + 3*(alto_boton + espaciado), ancho_boton, alto_boton),
            "texto": "A*",
            "accion": lambda: self.ejecutar_algoritmo("a_star"),
            "activo": False
        }
        
        botones["bfs"] = {
            "rect": pygame.Rect(x_inicio, y_inicio + 4*(alto_boton + espaciado), ancho_boton, alto_boton),
            "texto": "BFS",
            "accion": lambda: self.ejecutar_algoritmo("bfs"),
            "activo": False
        }
        
        botones["dfs"] = {
            "rect": pygame.Rect(x_inicio, y_inicio + 5*(alto_boton + espaciado), ancho_boton, alto_boton),
            "texto": "DFS",
            "accion": lambda: self.ejecutar_algoritmo("dfs"),
            "activo": False
        }
        
        botones["dijkstra"] = {
            "rect": pygame.Rect(x_inicio, y_inicio + 6*(alto_boton + espaciado), ancho_boton, alto_boton),
            "texto": "Dijkstra",
            "accion": lambda: self.ejecutar_algoritmo("dijkstra"),
            "activo": False
        }
        
        botones["resetear"] = {
            "rect": pygame.Rect(x_inicio, y_inicio + 7*(alto_boton + espaciado), ancho_boton, alto_boton),
            "texto": "Resetear Todo",
            "accion": lambda: self.gestor.resetear_todo(),
            "activo": False
        }
        
        return botones
    
    def ejecutar_algoritmo(self, algoritmo):
        """Ejecuta el algoritmo especificado"""
        if not self.gestor.inicio or not self.gestor.meta:
            print("Error: Debes establecer un punto de inicio y un punto meta")
            return
        
        # Resetear el estado de búsqueda
        self.gestor.resetear()
        
        # Aquí se ejecutaría el algoritmo seleccionado
        if algoritmo == "a_star":
            print("Ejecutando A*")
        elif algoritmo == "bfs":
            print("Ejecutando BFS")
        elif algoritmo == "dfs":
            print("Ejecutando DFS")
        elif algoritmo == "dijkstra":
            print("Ejecutando Dijkstra")
    
    def procesar_eventos(self):
        """Procesa los eventos de la ventana"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clic izquierdo
                    x, y = evento.pos
                    # Verificar si se hizo clic en algún botón
                    botón_clickeado = False
                    for nombre, boton in self.botones.items():
                        if boton["rect"].collidepoint(x, y):
                            boton["accion"]()
                            botón_clickeado = True
                    
                    # Si no se clickeó un botón, procesar clic en el grid
                    if not botón_clickeado:
                        self.gestor.procesar_clic(x, y)
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.ejecutando = False
    
    def dibujar_grid(self):
        """Dibuja el grid en la pantalla"""
        # Dibujar celdas
        for fila in self.gestor.nodos:
            for nodo in fila:
                rect = nodo.get_rect(OFFSET_X, OFFSET_Y)
                
                # Determinar color según el estado
                if nodo.es_inicio:
                    color = COLOR_INICIO
                elif nodo.es_meta:
                    color = COLOR_META
                elif nodo.es_obstaculo:
                    color = COLOR_OBSTACULO
                elif nodo.en_camino:
                    color = COLOR_CAMINO
                elif nodo.visitado:
                    color = COLOR_VISITADO
                else:
                    color = COLOR_CELDA
                
                pygame.draw.rect(self.pantalla, color, rect)
                pygame.draw.rect(self.pantalla, COLOR_LINEA, rect, 1)
    
    def dibujar_botones(self):
        """Dibuja los botones de la interfaz"""
        for nombre, boton in self.botones.items():
            # Cambiar color si el modo actual coincide (solo para botones de modo)
            if nombre in ["inicio", "meta", "obstaculo"] and nombre == self.gestor.modo_actual:
                color = COLOR_BOTON_HOVER
            else:
                color = COLOR_BOTON
            
            pygame.draw.rect(self.pantalla, color, boton["rect"])
            pygame.draw.rect(self.pantalla, COLOR_LINEA, boton["rect"], 2)
            
            # Dibujar texto
            texto_superficie = self.fuente_pequeña.render(boton["texto"], True, COLOR_TEXTO)
            texto_rect = texto_superficie.get_rect(center=boton["rect"].center)
            self.pantalla.blit(texto_superficie, texto_rect)
    
    def dibujar_info(self):
        """Dibuja información en la pantalla"""
        texto = f"Modo: {self.gestor.modo_actual.upper()}"
        superficie_texto = self.fuente.render(texto, True, COLOR_TEXTO)
        self.pantalla.blit(superficie_texto, (OFFSET_X, ANCHO_VENTANA - 180 + 220))
        
        info_grid = f"Grid: {self.gestor.cols}x{self.gestor.filas}"
        superficie_info = self.fuente_pequeña.render(info_grid, True, COLOR_TEXTO)
        self.pantalla.blit(superficie_info, (OFFSET_X, ANCHO_VENTANA - 180 + 250))
    
    def dibujar(self):
        """Dibuja toda la interfaz"""
        self.pantalla.fill(COLOR_FONDO)
        self.dibujar_grid()
        self.dibujar_botones()
        self.dibujar_info()
        pygame.display.flip()
    
    def ejecutar(self):
        """Ejecuta el loop principal"""
        while self.ejecutando:
            self.procesar_eventos()
            self.dibujar()
            self.reloj.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()
