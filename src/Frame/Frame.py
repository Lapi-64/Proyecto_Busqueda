import pygame
import sys
from tkinter import messagebox
from Logica.Nodo import Nodo

from Algoritmos_Busqueda.A_Star import a_star
from Algoritmos_Busqueda.BFS import bfs
from Algoritmos_Busqueda.DFS import dfs
from Algoritmos_Busqueda.Dijkstra import dijkstra

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
COLOR_POSIBLE = (0, 255, 0)
COLOR_VISITADO = (255, 0, 0)
COLOR_CAMINO = (255, 255, 0)
COLOR_INICIO = (0, 0, 255)
COLOR_META = (128, 0, 128)
COLOR_OBSTACULO = (0, 0, 0)
COLOR_TEXTO = (50, 50, 50)
COLOR_BOTON = (200, 200, 200)
COLOR_BOTON_SELECCION = (180, 180, 180)


class GestorGrid:
    def __init__(self, colum, filas, tamaño_celda):
        self.cols = colum
        self.filas = filas
        self.tamaño_celda = tamaño_celda
        self.nodos = [[Nodo(x, y, tamaño_celda) for x in range(colum)] for y in range(filas)]
        self.modo_actual = "normal"
        self.inicio = None
        self.meta = None
        
    def obtener_nodo_en_punto(self, px, py):
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
        self.modo_actual = modo
    
    def procesar_clic(self, px, py):
        nodo = self.obtener_nodo_en_punto(px, py)
        if not nodo:
            return

        nodo.en_camino = False
        
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
        for fila in self.nodos:
            for nodo in fila:
                nodo.reset()
    
    def reiniciar(self):
    
        self.inicio = None
        self.meta = None
        for fila in self.nodos:
            for nodo in fila:
                nodo.visitado = False
                nodo.es_inicio = False
                nodo.es_meta = False
                nodo.es_obstaculo = False
                nodo.en_camino = False
                nodo.posible = False


class InterfazGrid:
    
    def __init__(self, ancho, alto):
 
        self.pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Editor de Grid - Búsqueda IA")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 24)
        self.fuente_pequeña = pygame.font.Font(None, 18)
        
        self.gestor = GestorGrid(CANTIDAD_COLUMNAS, CANTIDAD_FILAS, TAMAÑO_CELDA)
        self.botones = self._crear_botones()
        self.alert_msg = None
        self.alert_timer = 0
        self.ejecutando = True
    
    def _crear_botones(self):

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
        
        botones["reiniciar"] = {
            "rect": pygame.Rect(x_inicio, y_inicio + 7*(alto_boton + espaciado), ancho_boton, alto_boton),
            "texto": "Reiniciar",
            "accion": lambda: self.gestor.reiniciar(),
            "activo": False
        }
        
        return botones
    
    def ejecutar_algoritmo(self, algoritmo):
        if not self.gestor.inicio or not self.gestor.meta:
            print("Error: Debes establecer un punto de inicio y un punto meta")
            return
        
        self.gestor.resetear()
        
        # resultado será False o (longitud, tiempo)
        resultado = False
        nombre = algoritmo.upper() if algoritmo != "a_star" else "A*"

        if algoritmo == "a_star":
            print("Ejecutando A*")
            resultado = a_star(self.gestor, delay=0.1, draw_func=self.dibujar)
        elif algoritmo == "bfs":
            print("Ejecutando BFS")
            resultado = bfs(self.gestor, delay=0.1, draw_func=self.dibujar)
        elif algoritmo == "dfs":
            print("Ejecutando DFS")
            resultado = dfs(self.gestor, delay=0.1, draw_func=self.dibujar)
        elif algoritmo == "dijkstra":
            print("Ejecutando Dijkstra")
            resultado = dijkstra(self.gestor, delay=0.1, draw_func=self.dibujar)

        if resultado:
            length, elapsed = resultado
            mensaje = f"Ruta calculada: {length} celdas en {elapsed:.2f} s"
            self._mostrar_alerta(mensaje)
            messagebox.showinfo(f"{nombre} - Resultado", mensaje)
        else:
            messagebox.showerror(f"{nombre} - Sin Ruta", "No se encontró una ruta hacia la meta.")
    
    def procesar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: 
                    x, y = evento.pos
                    botón_clickeado = False
                    for nombre, boton in self.botones.items():
                        if boton["rect"].collidepoint(x, y):
                            boton["accion"]()
                            botón_clickeado = True
                    
                    if not botón_clickeado:
                        self.gestor.procesar_clic(x, y)
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.ejecutando = False
    
    def dibujar_grid(self):
        for fila in self.gestor.nodos:
            for nodo in fila:
                rect = nodo.get_rect(OFFSET_X, OFFSET_Y)
                
                if nodo.es_inicio:
                    color = COLOR_INICIO
                elif nodo.es_meta:
                    color = COLOR_META
                elif nodo.es_obstaculo:
                    color = COLOR_OBSTACULO
                elif nodo.en_camino:
                    color = COLOR_CAMINO
                elif nodo.posible:
                    color = COLOR_POSIBLE
                elif nodo.visitado:
                    color = COLOR_VISITADO
                else:
                    color = COLOR_CELDA
                
                pygame.draw.rect(self.pantalla, color, rect)
                pygame.draw.rect(self.pantalla, COLOR_LINEA, rect, 1)
    
    def dibujar_botones(self):
        for nombre, boton in self.botones.items():
            if nombre in ["inicio", "meta", "obstaculo"] and nombre == self.gestor.modo_actual:
                color = COLOR_BOTON_SELECCION
            else:
                color = COLOR_BOTON
            
            pygame.draw.rect(self.pantalla, color, boton["rect"])
            pygame.draw.rect(self.pantalla, COLOR_LINEA, boton["rect"], 2)
            
            texto_superficie = self.fuente_pequeña.render(boton["texto"], True, COLOR_TEXTO)
            texto_rect = texto_superficie.get_rect(center=boton["rect"].center)
            self.pantalla.blit(texto_superficie, texto_rect)
    
    def dibujar_info(self):
        texto = f"Modo: {self.gestor.modo_actual.upper()}"
        superficie_texto = self.fuente.render(texto, True, COLOR_TEXTO)
        self.pantalla.blit(superficie_texto, (OFFSET_X, ANCHO_VENTANA - 180 + 220))
        
        info_grid = f"Grid: {self.gestor.cols}x{self.gestor.filas}"
        superficie_info = self.fuente_pequeña.render(info_grid, True, COLOR_TEXTO)
        self.pantalla.blit(superficie_info, (OFFSET_X, ANCHO_VENTANA - 180 + 250))
    
    def dibujar(self):
        self.pantalla.fill(COLOR_FONDO)
        self.dibujar_grid()
        self.dibujar_botones()
        self.dibujar_info()
        if self.alert_msg and self.alert_timer > 0:
            self._dibujar_alerta(self.alert_msg)
        pygame.display.flip()

    def _mostrar_alerta(self, texto, duracion=120):
        """Configura un mensaje visible en pantalla durante unas iteraciones."""
        self.alert_msg = texto
        self.alert_timer = duracion

    def _dibujar_alerta(self, texto):
       
        warning_rect = pygame.Rect(OFFSET_X, OFFSET_Y, 300, 30)
        pygame.draw.rect(self.pantalla, (255, 220, 220), warning_rect)
        texto_surf = self.fuente.render(texto, True, COLOR_TEXTO)
        self.pantalla.blit(texto_surf, (warning_rect.x + 5, warning_rect.y + 5))
    
    def ejecutar(self):
        while self.ejecutando:
            self.procesar_eventos()
            if self.alert_timer > 0:
                self.alert_timer -= 1
                if self.alert_timer == 0:
                    self.alert_msg = None
            self.dibujar()
            self.reloj.tick(60)
        
        pygame.quit()
        sys.exit()
