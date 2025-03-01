import sys
import pygame

# Agregar la carpeta 'src' al path de Python
sys.path.append("src")

from src.screen import MenuScreen

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 400, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

class Game:
    def __init__(self):
        self.running = True
        self.screen = MenuScreen(self)
        self.clock = pygame.time.Clock()  # Controlar la velocidad del bucle

    def change_screen(self, new_screen):
        self.screen = new_screen

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit()

            self.screen.handle_events(events)
            self.screen.update()
            self.screen.draw(SCREEN)

            pygame.display.update()  # Agregar actualización de pantalla
            self.clock.tick(60)  # Limitar a 60 FPS

if __name__ == "__main__":
    game = Game()
    game.run()
