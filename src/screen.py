import pygame
import os
from button import Button  
from logic import Logic

# Configuración de pantalla
WIDTH, HEIGHT = 400, 500
CELL_SIZE = 20
GRID_ORIGIN_X = 100
GRID_ORIGIN_Y = 50
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

class Screen:
    def __init__(self, game):
        self.game = game
    
    def handle_events(self, events):
        pass
    
    def update(self):
        pass
    
    def draw(self, screen):
        pass

class MenuScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.fondo = pygame.image.load(os.path.join(ASSETS_DIR, 'fondo.jpg'))
        self.fondo = pygame.transform.scale(self.fondo, (WIDTH, HEIGHT))
        
        pygame.mixer.music.load(os.path.join(ASSETS_DIR, 'music_base.mp3'))
        pygame.mixer.music.play(-1)
        
        self.font = pygame.font.Font(None, 40)
        
        self.play_button = Button(
            image=pygame.transform.scale(pygame.image.load("assets/Play Rect.png"), (200, 75)),
            pos=(WIDTH // 2, HEIGHT // 2 + 50),
            text_input="PLAY",
            font=self.font,
            base_color="Black",
            hovering_color="White"
        )
        
        self.quit_button = Button(
            image=pygame.transform.scale(pygame.image.load("assets/Quit Rect.png"), (200, 75)),
            pos=(WIDTH // 2, HEIGHT // 2 +150),
            text_input="QUIT",
            font=self.font,
            base_color="Black",
            hovering_color="White"
        )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.play_button.checkForInput(mouse_pos):
                    self.game.change_screen(GameScreen(self.game))
                if self.quit_button.checkForInput(mouse_pos):
                    self.game.quit()

    def draw(self, screen):
        screen.blit(self.fondo, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        
        self.play_button.changeColor(mouse_pos)
        self.play_button.update(screen)
        
        self.quit_button.changeColor(mouse_pos)
        self.quit_button.update(screen)

class GameScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.fondo = pygame.image.load(os.path.join(ASSETS_DIR, 'fondo_juego.jpg'))
        self.fondo = pygame.transform.scale(self.fondo, (WIDTH, HEIGHT))
        self.tetris = Logic(20, 10)
        self.clock = pygame.time.Clock()
        self.pressing_down = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit()
            if event.type == pygame.KEYDOWN:
                if self.tetris.state == "start":  
                    if event.key == pygame.K_UP:
                        self.tetris.rotate()
                    if event.key == pygame.K_DOWN:
                        self.pressing_down = True
                    if event.key == pygame.K_LEFT:
                        self.tetris.go_side(-1)
                    if event.key == pygame.K_RIGHT:
                        self.tetris.go_side(1)
                    if event.key == pygame.K_SPACE:
                        self.tetris.go_space()
                    if event.key == pygame.K_c:  # PRESIONAR "C" PARA CAMBIAR LA PIEZA
                        self.tetris.swap_piece()

                if event.key == pygame.K_ESCAPE:
                    self.game.change_screen(MenuScreen(self.game))
            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                self.pressing_down = False


    def update(self):
        if self.tetris.state == "start":
            if self.pressing_down:
                self.tetris.go_down()
            self.tetris.go_down()
    def draw_next_pieces(self, screen):
        font = pygame.font.SysFont('Arial', 20, True)
        next_text = font.render("Next:", True, (255, 255, 255))
        screen.blit(next_text, (320, 50))

        for index, fig in enumerate(self.tetris.next_figures):
            color = self.tetris.get_color(fig.type)
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in fig.image():
                        pygame.draw.rect(screen, color, 
                                        [320 + j * 15, 80 + index * 80 + i * 15, 15, 15])
    def draw(self, screen):
        screen.blit(self.fondo, (0, 0))
        font = pygame.font.SysFont('Arial', 25, True, False)
        score_text = font.render(f"Score: {self.tetris.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Dibujar cuadrícula
        for y in range(self.tetris.height):
            for x in range(self.tetris.width):
                pygame.draw.rect(screen, (50, 50, 50), 
                                [GRID_ORIGIN_X + x * CELL_SIZE, 
                                GRID_ORIGIN_Y + y * CELL_SIZE, 
                                CELL_SIZE, CELL_SIZE], 1)

                if self.tetris.field[y][x] != -1:
                    color = self.tetris.get_color(self.tetris.field[y][x])
                    pygame.draw.rect(screen, color, 
                                    [GRID_ORIGIN_X + x * CELL_SIZE, 
                                    GRID_ORIGIN_Y + y * CELL_SIZE, 
                                    CELL_SIZE, CELL_SIZE])

        # Dibujar figura en movimiento con su color
        if self.tetris.figure is not None:
            color = self.tetris.get_color(self.tetris.figure.type)
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.tetris.figure.image():
                        pygame.draw.rect(screen, color, 
                                        [GRID_ORIGIN_X + (self.tetris.figure.x + j) * CELL_SIZE, 
                                        GRID_ORIGIN_Y + (self.tetris.figure.y + i) * CELL_SIZE, 
                                        CELL_SIZE, CELL_SIZE])

        # Dibujar próximas piezas en la esquina derecha
        self.draw_next_pieces(screen)

        # Mostrar "Game Over"
        if self.tetris.state == "gameover":
            font1 = pygame.font.SysFont('Arial', 50, True, False)
            game_over_text = font1.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (100, 200))

        pygame.display.flip()
        self.clock.tick(60)
