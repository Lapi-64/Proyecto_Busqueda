import pygame
from Frame.Frame import InterfazGrid, ANCHO_VENTANA, ALTO_VENTANA

pygame.init()


def main():
    interfaz = InterfazGrid(ANCHO_VENTANA, ALTO_VENTANA)
    interfaz.ejecutar()


if __name__ == "__main__":
    main()
