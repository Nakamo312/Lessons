from pygame import *
from pygame import time
WEIGHT = 700
HEIGHT = 500

table = ['**************',
         '*   *     |  *',
         '*   *    *   *',
         '*   *    *   *',
         '*   *    *   *',
         '*   *    *   *',
         '*   *    *   *',
         '*   *    *   *',
         '* |     |*  @*',
         '**************']
window = display.set_mode((WEIGHT, HEIGHT))
display.set_caption('Concept')

background = transform.scale(image.load("Sprites/1273.jpg").convert_alpha(),(WEIGHT, HEIGHT))

class Map():
    def __init__(self,texture_wall,texture_final,texture_monster):
        self.map = table
        self.walls = sprite.Group()
        self.monsters = sprite.Group()
        self.texture_wall = texture_wall
        self.texture_final = texture_final
        self.texture_monster = texture_monster
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == '*':
                    self.walls.add(GameSpite(50*j, 50*i, 50, 50, self.texture_wall))
                elif self.map[i][j] == '@':
                    self.portal = GameSpite(50*j, 50*i, 50, 50, self.texture_final)
                elif self.map[i][j] == '|':
                    self.monsters.add(Monster(50*j, 50*i, 50, 50, self.texture_monster))         
    def reset(self, surface):
        self.walls.draw(surface)
        self.portal.draw(surface)
        self.monsters.draw(surface)
        self.monsters.update(self.walls)


        
                 
class GameSpite(sprite.Sprite):
    def __init__(self, x, y, w, h, picture):
        super().__init__()
        self.image = transform.scale(image.load(picture).convert_alpha(),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self,surface):
        surface.blit(self.image,(self.rect.x, self.rect.y))

class Hero(GameSpite):
    def __init__(self,x, y, w, h,picture):
        super().__init__(x, y, w, h, picture)
        self.speed_x = 0
        self.speed_y = 0
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

class Monster(GameSpite):
    def __init__(self,x, y, w, h,picture):
        super().__init__(x, y, w, h, picture)
        self.speed_y = 5
    def update(self,walls):
        if sprite.spritecollide(self, walls,False):
            self.speed_y*= -1
        self.rect.y += self.speed_y 
       

 #картинку поменять
    



clock = time.Clock()
player = Hero(50,50,50,50,'Sprites/kisspng-skeleton-2d-computer-graphics-sprite-two-dimension-5b004d06f2c287.2692903915267463749944.png')
land = Map("Sprites/realistic-red-color-brick-wall-seamless-pattern_251819-2333.jpg","Sprites/final.png","Sprites/ghost.png") # картинку свою 
run = True
finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_w:
                player.speed_y = -5
            elif e.key == K_s:
                player.speed_y = 5
            elif e.key == K_d:
                player.speed_x = 5
            elif e.key == K_a:
                player.speed_x = -5 
        elif e.type == KEYUP:
            if e.key == K_w:
                player.speed_y = 0
            elif e.key == K_s:
                player.speed_y = 0
            elif e.key == K_d:
                player.speed_x = 0
            elif e.key == K_a:
                player.speed_x = 0
        if finish == False:
            if sprite.collide_rect(player, land.portal):
                finish = True
            if sprite.spritecollide(player, land.monsters,False):
                finish = True    
            if sprite.spritecollide(player, land.walls,False):
                player.rect.x =  pred_x
                player.rect.y = pred_y
            else:
                pred_x = player.rect.x
                pred_y = player.rect.y        
                player.move()             
            display.set_caption(str(int(clock.get_fps())))               
            #window.blit(background, (0, 0))
            window.fill((0, 0, 0))
            land.reset(window)
            player.draw(window)
            display.update()
            clock.tick(60)
        else:
            print('Вы выиграли!')    
