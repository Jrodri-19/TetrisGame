import random

class Figure:
    SHAPES = [
    [[1,5,9,13],[4,5,6,7]],                     #I
    [[0,4,5,6],[1,2,5,9],[4,5,6,10],[1,5,8,9]],     #J
    [[1,4,5,6],[1,5,6,9],[4,5,6,9],[1,4,5,9]],      #T
    [[2,4,5,6],[1,5,9,10],[4,5,6,8],[0,1,5,9]],     #L
    [[1,2,5,6]],                                 #O
    [[1,2,4,5],[0,4,5,9]],                          #S
    [[0,1,5,6],[1,4,5,8]],                          #Z
    ]
    
    COLORS = [
        (0, 255, 255),   # Cyan (Línea)
        (255, 255, 0),   # Amarillo (Cuadrado)
        (128, 0, 128),   # Púrpura (T)
        (255, 165, 0),   # Naranja (L)
        (0, 0, 255),     # Azul (L invertida)
        (0, 255, 0),     # Verde (S)
        (255, 0, 0)      # Rojo (Z)
    ]
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.SHAPES) - 1)
        self.rotation = 0
        self.color = self.COLORS[self.type]
    
    def rotate(self):
        """ Rota la figura en 90 grados """
        self.rotation = (self.rotation + 1) % len(self.SHAPES[self.type])
    
    def image(self):
        """ Devuelve la forma actual de la figura """
        return self.SHAPES[self.type][self.rotation]

