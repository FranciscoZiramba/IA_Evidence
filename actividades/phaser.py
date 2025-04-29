import pygame
import random
import sys
import numpy as np
import csv  # <-- Añadir este import
import os   # <-- Añadir este import
from sklearn.neural_network import MLPClassifier

# Configuración inicial
WIDTH, HEIGHT = 800, 400
FPS = 30
GRAVITY = 800 / FPS  # Ajustado para frames

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Plataformas")
clock = pygame.time.Clock()

# Clases del juego
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 48))
        self.image.fill((255, 0, 0))  # Rojo como placeholder
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - self.rect.height
        self.velocity_y = 0
        self.on_floor = True
        self.running_frames = []  # Para animación
        
    def update(self):
        # Aplicar gravedad
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y / FPS
        
        # Verificar si está en el suelo
        if self.rect.y >= HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height
            self.velocity_y = 0
            self.on_floor = True
        else:
            self.on_floor = False
            
    def jump(self):
        if self.on_floor:
            self.velocity_y = -270
            self.on_floor = False

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((128, 0, 128))  # Púrpura como placeholder
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 100
        self.rect.y = HEIGHT - self.rect.height
        self.velocity_x = 0
        self.active = False
        
    def update(self):
        if self.active:
            self.rect.x += self.velocity_x / FPS
            if self.rect.x <= 0:
                self.reset()
                
    def reset(self):
        self.rect.x = WIDTH - 100
        self.active = False
        self.velocity_x = 0
        
    def shoot(self):
        self.velocity_x = -1 * random.randint(300, 800)
        self.active = True

class Menu:
    def __init__(self):
        self.active = False
        self.font = pygame.font.SysFont('Arial', 20)
        
    def draw(self):
        if self.active:
            # Fondo del menú
            menu_rect = pygame.Rect(WIDTH//2 - 135, HEIGHT//2 - 90, 270, 180)
            pygame.draw.rect(screen, (50, 50, 50), menu_rect)
            
            # Opciones
            reset_text = self.font.render("Reiniciar Entrenamiento", True, (255, 255, 255))
            auto_text = self.font.render("Modo Automático", True, (255, 255, 255))
            
            screen.blit(reset_text, (WIDTH//2 - reset_text.get_width()//2, HEIGHT//2 - 60))
            screen.blit(auto_text, (WIDTH//2 - auto_text.get_width()//2, HEIGHT//2 + 30))

class Game:
    def __init__(self):
        self.player = Player()
        self.bullet = Bullet()
        self.menu = Menu()
        self.paused = False
        self.auto_mode = False
        self.training_complete = False
        self.training_data = []
        
        # Configuración del archivo CSV
        self.dataset_filename = "training_data.csv"
        self.initialize_csv_file()  # <-- Inicializar el archivo CSV

        # Red neuronal (usando scikit-learn por simplicidad)
        self.nn = MLPClassifier(hidden_layer_sizes=(6, 6), max_iter=10000, learning_rate_init=0.0003)
        
        # Sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.bullet)
        
        # Fondo (simplificado)
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill((0, 0, 50))  # Azul oscuro como placeholder
        
        # Texto de pausa
        self.pause_text = self.menu.font.render("Pausa", True, (255, 255, 255))
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.paused and not self.auto_mode:
                    self.player.jump()
                if event.key == pygame.K_p:
                    self.toggle_pause()
                    
            if event.type == pygame.MOUSEBUTTONDOWN and self.paused:
                self.handle_menu_click(event.pos)
                
        return True
        
    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.menu.active = True
            
    def handle_menu_click(self, pos):
        menu_x1, menu_x2 = WIDTH//2 - 135, WIDTH//2 + 135
        menu_y1, menu_y2 = HEIGHT//2 - 90, HEIGHT//2 + 90
        
        if menu_x1 <= pos[0] <= menu_x2 and menu_y1 <= pos[1] <= menu_y2:
            # Click en la opción de reinicio
            if menu_y1 <= pos[1] <= menu_y1 + 90:
                self.training_complete = False
                self.training_data = []
                self.auto_mode = False
            # Click en la opción de modo automático
            elif menu_y1 + 90 <= pos[1] <= menu_y2:
                if not self.training_complete and len(self.training_data) > 0:
                    print(f"Entrenando con {len(self.training_data)} muestras...")
                    inputs = np.array([data['input'] for data in self.training_data])
                    outputs = np.array([data['output'] for data in self.training_data])
                    self.nn.fit(inputs, outputs)
                    self.training_complete = True
                self.auto_mode = True
                
            self.reset_variables()
            self.paused = False
            self.menu.active = False
            
    def reset_variables(self):
        self.player.rect.x = 50
        self.player.rect.y = HEIGHT - self.player.rect.height
        self.player.velocity_y = 0
        self.bullet.reset()
        
    def update(self):
        if not self.paused:
            # Actualizar sprites
            self.all_sprites.update()
            
            # Mover fondo (simulación)
            # En una implementación real, usaríamos un tile scroll
            
            # Disparar bala si no está activa
            if not self.bullet.active:
                self.bullet.shoot()
                
            # Detectar colisión
            if pygame.sprite.collide_rect(self.player, self.bullet):
                self.toggle_pause()
                
            # Lógica de la red neuronal en modo automático
            if self.auto_mode and self.bullet.active and self.player.on_floor:
                bullet_displacement = self.player.rect.x - self.bullet.rect.x
                bullet_velocity = self.bullet.velocity_x
                
                if self.should_jump([bullet_displacement, bullet_velocity]):
                    self.player.jump()
                    
            # Recolectar datos de entrenamiento
            if not self.auto_mode and self.bullet.active:
                bullet_displacement = self.player.rect.x - self.bullet.rect.x
                bullet_velocity = self.bullet.velocity_x
                
                air_status = 0 if self.player.on_floor else 1
                ground_status = 1 if self.player.on_floor else 0
                
                self.training_data.append({
                    'input': [bullet_displacement, bullet_velocity],
                    'output': [air_status, ground_status]
                })
                
                print(f"Desplazamiento: {bullet_displacement}, Velocidad: {bullet_velocity}, "
                      f"Aire: {air_status}, Suelo: {ground_status}")
    
    def should_jump(self, input_data):
        if not self.training_complete:
            return False
            
        # Predecir con la red neuronal
        prediction = self.nn.predict_proba([input_data])[0]
        air_prob = prediction[0]  # Probabilidad de estar en el aire
        ground_prob = prediction[1]  # Probabilidad de estar en el suelo
        
        print(f"Entrada: {input_data[0]} {input_data[1]}")
        print(f"En el Aire: {air_prob*100:.0f}%, En el suelo: {ground_prob*100:.0f}%")
        
        return air_prob >= ground_prob
        
    def draw(self):
        # Dibujar fondo
        screen.blit(self.background, (0, 0))
        
        # Dibujar sprites
        self.all_sprites.draw(screen)
        
        # Dibujar texto de pausa
        screen.blit(self.pause_text, (WIDTH - 100, 20))
        
        # Dibujar menú si está activo
        self.menu.draw()
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)
    def initialize_csv_file(self):
        """Crea el archivo CSV con los encabezados si no existe"""
        if not os.path.exists(self.dataset_filename):
            with open(self.dataset_filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['displacement', 'velocity', 'air_status', 'ground_status'])

    def save_to_csv(self):
        """Guarda los datos de entrenamiento en el archivo CSV"""
        with open(self.dataset_filename, 'a', newline='') as f:
            writer = csv.writer(f)
            for data in self.training_data:
                writer.writerow([
                    data['input'][0],  # displacement
                    data['input'][1],  # velocity
                    data['output'][0], # air_status (1 si está en el aire)
                    data['output'][1]  # ground_status (1 si está en el suelo)
                ])
        print(f"Se han guardado {len(self.training_data)} registros en {self.dataset_filename}")

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)
        
        # Guardar datos al salir del juego
        if len(self.training_data) > 0:
            self.save_to_csv()  # <-- Guardar datos cuando termina el juego

# Ejecutar el juego
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()