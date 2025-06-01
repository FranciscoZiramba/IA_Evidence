import pygame
import sys

# Colores
BLANCO = (255, 255, 255)
GRIS = (128, 128, 128)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)

class Casilla:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.g = 0  # Costo acumulado desde el inicio
        self.h = 0  # Distancia estimada a la meta
        self.f = 0  # Valor total (g + h)
        self.padre = None  # Casilla desde la cual se llegó

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

class TableroApp:
    def __init__(self, n, tamano_ventana=600):
        self.n = n  # Tamaño del tablero (n x n)
        self.tamano_ventana = tamano_ventana  # Tamaño de la ventana
        self.tamano_casilla = tamano_ventana // n  # Tamaño de cada casilla
        self.tablero = [[0 for _ in range(n)] for _ in range(n)]  # Matriz del tablero
        self.punto_partida = None  # Almacenar el punto de partida
        self.punto_meta = None  # Almacenar el punto de meta
        self.numero_meta = None  # Número de la casilla meta
        self.seleccionando_partida = False  # Estado para seleccionar el punto de partida
        self.seleccionando_meta = False  # Estado para seleccionar el punto de meta
        self.lista_abierta = []  # Lista de casillas abiertas
        self.lista_cerrada = []  # Lista de casillas cerradas
        self.camino = []  # Camino final
        self.ejecutando = False  # Estado para controlar la ejecución del algoritmo

        # Inicializar Pygame
        pygame.init()
        self.ventana = pygame.display.set_mode((tamano_ventana, tamano_ventana + 100))
        pygame.display.set_caption(f"Tablero {n}x{n}")
        self.fuente = pygame.font.Font(None, 24)

    def dibujar_tablero(self):
        # Dibujar el tablero
        for i in range(self.n):
            for j in range(self.n):
                x = j * self.tamano_casilla
                y = i * self.tamano_casilla
                color = BLANCO if self.tablero[i][j] == 0 else GRIS
                if any(casilla.i == i and casilla.j == j for casilla in self.lista_cerrada):  # Casillas evaluadas
                    color = ROJO
                pygame.draw.rect(self.ventana, color, (x, y, self.tamano_casilla, self.tamano_casilla))
                pygame.draw.rect(self.ventana, NEGRO, (x, y, self.tamano_casilla, self.tamano_casilla), 1)
                if self.tablero[i][j] == 3:  # Punto de partida
                    pygame.draw.rect(self.ventana, ROJO, (x, y, self.tamano_casilla, self.tamano_casilla))
                elif self.tablero[i][j] == 5:  # Punto de meta
                    pygame.draw.rect(self.ventana, VERDE, (x, y, self.tamano_casilla, self.tamano_casilla))
                elif (i, j) in self.camino:  # Camino final
                    pygame.draw.rect(self.ventana, AMARILLO, (x, y, self.tamano_casilla, self.tamano_casilla))

                # Dibujar el número de la casilla
                numero = i * self.n + j + 1  # Calcular el número de la casilla
                texto = self.fuente.render(str(numero), True, NEGRO)
                self.ventana.blit(texto, (x + 5, y + 5))  # Posicionar el número en la esquina superior izquierda

                # Dibujar valores de F, G y H si la casilla está en la lista cerrada o abierta
                casilla_actual = next((c for c in self.lista_cerrada + self.lista_abierta if c.i == i and c.j == j), None)
                if casilla_actual:
                    texto_g = self.fuente.render(f"G: {casilla_actual.g}", True, NEGRO)
                    texto_h = self.fuente.render(f"H: {casilla_actual.h}", True, NEGRO)
                    texto_f = self.fuente.render(f"F: {casilla_actual.f}", True, NEGRO)
                    self.ventana.blit(texto_g, (x + 5, y + 20))
                    self.ventana.blit(texto_h, (x + 5, y + 35))
                    self.ventana.blit(texto_f, (x + 5, y + 50))

        # Dibujar botones
        pygame.draw.rect(self.ventana, VERDE, (0, self.tamano_ventana, self.tamano_ventana // 3, 50))
        pygame.draw.rect(self.ventana, AZUL, (self.tamano_ventana // 3, self.tamano_ventana, self.tamano_ventana // 3, 50))
        pygame.draw.rect(self.ventana, (255, 165, 0), (2 * self.tamano_ventana // 3, self.tamano_ventana, self.tamano_ventana // 3, 50))
        texto_punto_partida = self.fuente.render("Punto de partida", True, NEGRO)
        texto_comenzar = self.fuente.render("Comenzar", True, NEGRO)
        texto_meta = self.fuente.render("Seleccionar Meta", True, NEGRO)
        self.ventana.blit(texto_punto_partida, (20, self.tamano_ventana + 10))
        self.ventana.blit(texto_comenzar, (self.tamano_ventana // 3 + 20, self.tamano_ventana + 10))
        self.ventana.blit(texto_meta, (2 * self.tamano_ventana // 3 + 20, self.tamano_ventana + 10))

    def calcular_distancia(self, casilla_a, casilla_b):
        # Distancia de Manhattan (para movimientos ortogonales)
        return 10 * (abs(casilla_a.i - casilla_b.i) + abs(casilla_a.j - casilla_b.j))

    def encontrar_camino(self):
        if not self.punto_partida or not self.punto_meta:
            return

        # Inicializar listas
        inicio = Casilla(*self.punto_partida)
        meta = Casilla(*self.punto_meta)
        self.lista_abierta = [inicio]
        self.lista_cerrada = []
        self.camino = []
        self.ejecutando = True

        # Guardar el número de la casilla meta
        self.numero_meta = meta.i * self.n + meta.j + 1

        while self.lista_abierta and self.ejecutando:
            # Obtener la casilla con el valor F más bajo
            casilla_actual = min(self.lista_abierta, key=lambda x: x.f)

            # Imprimir listas abierta y cerrada en base a la numeración de las casillas
            lista_abierta_numeros = [c.i * self.n + c.j + 1 for c in self.lista_abierta]
            lista_cerrada_numeros = [c.i * self.n + c.j + 1 for c in self.lista_cerrada]
            print("Lista abierta:", lista_abierta_numeros)
            print("Lista cerrada:", lista_cerrada_numeros)

            # Si llegamos a la meta, reconstruir el camino y detener la ejecución
            if casilla_actual.i == meta.i and casilla_actual.j == meta.j:
                print("Meta encontrada en la casilla:", self.numero_meta)
                self.camino = []
                while casilla_actual:
                    self.camino.append((casilla_actual.i, casilla_actual.j))
                    casilla_actual = casilla_actual.padre
                self.camino.reverse()

                # Pintar el camino y actualizar pantalla
                self.dibujar_tablero()
                pygame.display.flip()

                # Detener ejecución correctamente
                self.lista_abierta.clear()
                self.lista_cerrada.clear()
                self.ejecutando = False
                return  # Salir del bucle while

            # Mover la casilla actual a la lista cerrada
            self.lista_abierta.remove(casilla_actual)
            self.lista_cerrada.append(casilla_actual)

            # Evaluar vecinos
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue  # Ignorar la casilla actual
                    ni, nj = casilla_actual.i + di, casilla_actual.j + dj
                    if 0 <= ni < self.n and 0 <= nj < self.n and self.tablero[ni][nj] == 0:
                        vecino = Casilla(ni, nj)
                        if vecino in self.lista_cerrada:
                            continue

                        # Calcular valores G, H y F
                        movimiento = 14 if di != 0 and dj != 0 else 10
                        g_temp = casilla_actual.g + movimiento
                        h_temp = self.calcular_distancia(vecino, meta)
                        f_temp = g_temp + h_temp

                        # Si el vecino ya está en la lista abierta y tiene un valor G menor, ignorarlo
                        if vecino in self.lista_abierta and g_temp > vecino.g:
                            continue

                        # Actualizar valores y padre
                        vecino.g = g_temp
                        vecino.h = h_temp
                        vecino.f = f_temp
                        vecino.padre = casilla_actual

                        # Agregar a la lista abierta si no está ya
                        if vecino not in self.lista_abierta:
                            self.lista_abierta.append(vecino)

            # Actualizar la pantalla
            self.dibujar_tablero()
            pygame.display.flip()
            pygame.time.delay(200)  # Retardo para visualización progresiva

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if y < self.tamano_ventana:  # Clic en el tablero
                    i = y // self.tamano_casilla
                    j = x // self.tamano_casilla
                    if self.seleccionando_partida:
                        if self.tablero[i][j] == 0:  # Verificar que la casilla no esté deshabilitada
                            if self.punto_partida:
                                # Restaurar el estado anterior del punto de partida
                                i_prev, j_prev = self.punto_partida
                                self.tablero[i_prev][j_prev] = 0
                            # Asignar el nuevo punto de partida
                            self.punto_partida = (i, j)
                            self.tablero[i][j] = 3
                            self.seleccionando_partida = False
                    elif self.seleccionando_meta:
                        if self.tablero[i][j] == 0:  # Verificar que la casilla no esté deshabilitada
                            if self.punto_meta:
                                # Restaurar el estado anterior del punto de meta
                                i_prev, j_prev = self.punto_meta
                                self.tablero[i_prev][j_prev] = 0
                            # Asignar el nuevo punto de meta
                            self.punto_meta = (i, j)
                            self.tablero[i][j] = 5
                            self.numero_meta = i * self.n + j + 1  # Guardar el número de la casilla meta
                            self.seleccionando_meta = False
                    else:
                        # Marcar o desmarcar casilla
                        if self.tablero[i][j] == 0:
                            self.tablero[i][j] = 1
                        elif self.tablero[i][j] == 1:
                            self.tablero[i][j] = 0
                else:  # Clic en los botones
                    if x < self.tamano_ventana // 3:  # Botón "Punto de partida"
                        self.seleccionando_partida = True
                        self.seleccionando_meta = False
                    elif x < 2 * self.tamano_ventana // 3:  # Botón "Comenzar"
                        if self.punto_partida and self.punto_meta and not self.ejecutando and not self.camino:
                            self.encontrar_camino()
                    else:  # Botón "Seleccionar Meta"
                        self.seleccionando_meta = True
                        self.seleccionando_partida = False

    def ejecutar(self):
        while True:
            self.ventana.fill(BLANCO)
            self.dibujar_tablero()
            self.manejar_eventos()
            pygame.display.flip()

def main():
    # Pedir al usuario el tamaño del tablero
    n = int(input("Ingrese el tamaño del tablero (n x n): "))

    # Crear y ejecutar la aplicación
    app = TableroApp(n)
    app.ejecutar()

if __name__ == "__main__":
    main()