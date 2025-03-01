import random
from figure import Figure

class Logic:
    SCORE_TABLE = {1: 100, 2: 300, 3: 500, 4: 800}
    COLORS = [
        (0, 255, 255),  # I - Celeste
        (0, 0, 255),    # J - Azul
        (255, 165, 0),  # L - Naranja
        (255, 255, 0),  # O - Amarillo
        (0, 255, 0),    # S - Verde
        (128, 0, 128),  # T - Morado
        (255, 0, 0)     # Z - Rojo
    ]

    def __init__(self, height, width):
        self.level = 1
        self.score = 0
        self.lines_cleared = 0
        self.state = "start"
        self.height = height
        self.width = width
        self.field = [[-1] * width for _ in range(height)]  
        
        self.figure = None
        self.next_figures = [Figure(3, 0), Figure(3, 0)]  # Dos siguientes figuras
        self.hold_figure = None  # Figura guardada
        self.can_swap = True  # Se puede intercambiar solo una vez por turno

        self.new_figure()
        self.counter = 0  
        self.base_speed = 30  
        self.speed = self.base_speed  

         # 🔹 Inicializar lista de próximas figuras (mínimo 2)
        self.next_figures = [Figure(3, 0) for _ in range(2)]  
        self.new_figure()
    def new_figure(self):
        """Genera una nueva figura y actualiza la cola de próximas figuras."""
        self.figure = self.next_figures.pop(0)  # Tomamos la primera figura
        self.next_figures.append(Figure(3, 0))  # Agregamos una nueva figura al final

        if self.intersects():
            self.state = "gameover"

    def swap_figure(self):
        """Intercambia la figura actual con la figura guardada."""
        if self.can_swap:
            if self.held_figure is None:
                self.held_figure = self.figure
                self.new_figure()
            else:
                self.figure, self.held_figure = self.held_figure, self.figure
                self.figure.x, self.figure.y = 3, 0  # Reiniciar posición al cambiar
            self.can_swap = False  # Evita múltiples intercambios en un mismo turno

    def break_lines(self):
        lines = 0
        new_field = [[-1] * self.width for _ in range(self.height)]  
        new_row = self.height - 1  

        for i in range(self.height - 1, -1, -1):
            if -1 in self.field[i]:  
                new_field[new_row] = self.field[i][:]
                new_row -= 1
            else:
                lines += 1  

        self.field = new_field  

        if lines > 0:
            self.score += int(self.SCORE_TABLE.get(lines, 0) * self.level)
            self.lines_cleared += lines

        if self.lines_cleared >= self.level * 10:
            self.level += 1
            self.speed = max(5, self.base_speed - (self.level * 2))

    def go_space(self):
        if self.state == "start":
            while not self.intersects():
                self.figure.y += 1
            self.figure.y -= 1
            self.freeze()

    def go_down(self):
        if self.state == "start":
            self.counter += 1
            if self.counter >= self.speed:
                self.counter = 0
                self.figure.y += 1
                if self.intersects():
                    self.figure.y -= 1
                    self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.type
        self.break_lines()
        self.new_figure()

    def go_side(self, mov_x):
        if self.state == "start":
            old_x = self.figure.x
            self.figure.x += mov_x
            if self.intersects():
                self.figure.x = old_x
    
    def hold_piece(self):
        """Intercambia la pieza actual con la de espera."""
        if not self.can_hold:
            return  

        if self.hold_figure is None:
            self.hold_figure = self.figure  
            self.new_figure()  
        else:
            self.figure, self.hold_figure = self.hold_figure, self.figure  

        self.figure.x, self.figure.y = 3, 0  
        self.can_hold = False  

    def swap_piece(self):
        """Intercambia la pieza actual con la primera en la cola de próximas piezas"""
        if self.figure and self.next_figures:
            self.figure, self.next_figures[0] = self.next_figures[0], self.figure
            # Asegurar que la nueva pieza no colisione inmediatamente
            self.figure.x, self.figure.y = self.width // 2 - 2, 0
            if self.intersects():
                self.figure, self.next_figures[0] = self.next_figures[0], self.figure  # Revertir si hay colisión
    def rotate(self):
        if self.state == "start":
            old_rotation = self.figure.rotation
            self.figure.rotate()
            if self.intersects():
                self.figure.rotation = old_rotation
    def intersects(self):
        """Verifica si la figura actual choca con el tablero o con otras piezas."""
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    x = self.figure.x + j
                    y = self.figure.y + i
                    if x < 0 or x >= self.width or y >= self.height:  
                        return True  # Colisión con los bordes del tablero
                    if y >= 0 and self.field[y][x] != -1:  
                        return True  # Colisión con otra pieza en el tablero
        return False

    def get_color(self, piece_type):
        return self.COLORS[piece_type]
