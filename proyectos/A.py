import pygame
import heapq
import sys

# Configuraciones iniciales
ANCHO_VENTANA = 600
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Algoritmo A* - Buscador de Caminos")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AZUL = (0, 0, 255)

# Fuente para mostrar texto
pygame.font.init()
FUENTE = pygame.font.SysFont("Arial", 15)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.vecinos = []
        self.costo = 0  # Costo de movimiento
        self.g = float("inf")  # Costo acumulado
        self.h = 0  # Heurística
        self.f = float("inf")  # Costo total (f = g + h)

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_abierto(self):
        self.color = VERDE

    def hacer_cerrado(self):
        self.color = ROJO

    def hacer_camino(self):
        self.color = AZUL

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
        if self.color != BLANCO and self.color != NEGRO:
            # Mostrar valores de f, g y h
            texto_f = FUENTE.render(f"f: {self.f}", True, NEGRO)
            texto_g = FUENTE.render(f"g: {self.g}", True, NEGRO)
            texto_h = FUENTE.render(f"h: {self.h}", True, NEGRO)
            ventana.blit(texto_f, (self.x + 5, self.y + 5))
            ventana.blit(texto_g, (self.x + 5, self.y + 20))
            ventana.blit(texto_h, (self.x + 5, self.y + 35))

    def update_vecinos(self, grid):
        self.vecinos = []
        # Movimientos horizontales y verticales
        for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            f = self.fila + df
            c = self.col + dc
            if 0 <= f < self.total_filas and 0 <= c < self.total_filas:
                vecino = grid[f][c]
                if not vecino.es_pared():
                    self.vecinos.append(vecino)

        # Movimientos diagonales (solo si no hay paredes en las adyacentes)
        for df, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            f = self.fila + df
            c = self.col + dc
            if 0 <= f < self.total_filas and 0 <= c < self.total_filas:
                # Verificar si las casillas adyacentes (horizontal y vertical) están libres
                adyacente1 = grid[self.fila + df][self.col]
                adyacente2 = grid[self.fila][self.col + dc]
                if not adyacente1.es_pared() and not adyacente2.es_pared():
                    vecino = grid[f][c]
                    if not vecino.es_pared():
                        self.vecinos.append(vecino)

def heuristica(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)  # Distancia Manhattan

def algoritmo_a_estrella(dibujar, grid, inicio, fin):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, inicio))
    came_from = {}
    g_score = {nodo: float("inf") for fila in grid for nodo in fila}
    g_score[inicio] = 0
    f_score = {nodo: float("inf") for fila in grid for nodo in fila}
    f_score[inicio] = heuristica(inicio.get_pos(), fin.get_pos())

    open_set_hash = {inicio}

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        actual = heapq.heappop(open_set)[2]
        open_set_hash.remove(actual)

        if actual == fin:
            reconstruir_camino(came_from, fin, dibujar)
            fin.hacer_fin()
            return True

        for vecino in actual.vecinos:
            # Costo de movimiento: 10 para horizontal/vertical, 14 para diagonal
            costo_movimiento = 10 if abs(vecino.fila - actual.fila) + abs(vecino.col - actual.col) == 1 else 14
            temp_g_score = g_score[actual] + costo_movimiento

            if temp_g_score < g_score[vecino]:
                came_from[vecino] = actual
                g_score[vecino] = temp_g_score
                f_score[vecino] = temp_g_score + heuristica(vecino.get_pos(), fin.get_pos())
                if vecino not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[vecino], count, vecino))
                    open_set_hash.add(vecino)
                    vecino.hacer_abierto()

                # Actualizar valores de f, g y h en el nodo
                vecino.g = temp_g_score
                vecino.h = heuristica(vecino.get_pos(), fin.get_pos())
                vecino.f = f_score[vecino]

        dibujar()

        if actual != inicio:
            actual.hacer_cerrado()

        # Mostrar lista abierta y cerrada en consola
        print("Lista abierta:", [nodo.get_pos() for nodo in open_set_hash])
        print("Lista cerrada:", [nodo.get_pos() for nodo in g_score if g_score[nodo] != float("inf") and nodo not in open_set_hash])

        # Pausa para visualizar el proceso
        pygame.time.wait(100)

    return False

def reconstruir_camino(came_from, actual, dibujar):
    while actual in came_from:
        actual = came_from[actual]
        actual.hacer_camino()
        dibujar()
        # Pausa para visualizar el camino
        pygame.time.wait(100)

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

def main(ventana, ancho):
    # Solicitar al usuario el tamaño del tablero
    filas = int(input("Ingrese el tamaño del tablero (nxn): "))
    grid = crear_grid(filas, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, filas, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, filas, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()
                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()
                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, filas, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    for fila in grid:
                        for nodo in fila:
                            nodo.update_vecinos(grid)
                    algoritmo_a_estrella(lambda: dibujar(ventana, grid, filas, ancho), grid, inicio, fin)

                if event.key == pygame.K_c:  # Limpiar la cuadrícula
                    inicio = None
                    fin = None
                    grid = crear_grid(filas, ancho)

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)