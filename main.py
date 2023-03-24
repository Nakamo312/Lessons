from pygame import *

WEIGHT = 700
HEIGHT = 500

table = ['**************',
         '*   *        *',
         '*   *    *   *',
         '*   *    *   *',
         '*   *    *   *',
         '*   *    *   *',
         '*   *    *   *',
         '*   *    *   *',
         '*        *   *',
         '**************']

class Map():
    def __init__(self,texture):
        self.map = table
        self.walls = sprite.Group()
        self.texture = texture
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == '*':
                    self.walls.add(GameSpite(50*j, 50*i, 50, 50, self.texture))
    def reset(self, surface):
        self.walls.update(surface)
        
                 
class GameSpite(sprite.Sprite):
    def __init__(self, x, y, w, h, picture):
        super().__init__()
        self.image = transform.scale(image.load(picture),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self,surface):
        surface.blit(self.image,(self.rect.x, self.rect.y))







background = transform.scale(image.load("D:/Projects/Landscapes_Textures/1273.jpg"),(WEIGHT, HEIGHT)) #картинку поменять

    

    

window = display.set_mode((WEIGHT, HEIGHT))
display.set_caption('Concept')
land = Map("D:/Projects/Landscapes_Textures/realistic-red-color-brick-wall-seamless-pattern_251819-2333.jpg") # картинку свою 
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    window.blit(background, (0, 0))
    land.reset(window)
    display.update()
