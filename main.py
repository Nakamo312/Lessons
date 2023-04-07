from pygame import *
from pygame import time
from random import randint
init()

WEIGHT = 700
HEIGHT = 500

YELLOW = (255,255,0)
RED= (255,0,0)

level_1 = ['**************',
           '* $          *',
           '*********    *',
           '*            *',
           '*            *',
           '*            *',
           '*            *',
           '*            *',
           '*         | @*',
           '**************']
level_2 = ['**************',
           '* $ *     |  *',
           '*   *    *   *',
           '*   *    *   *',
           '*   *    *   *',
           '*   *    *   *',
           '*   *    *   *',
           '*   *    *   *',
           '* |     |*  @*',
           '**************']
level_3 = ['**************',
           '* $      *|@ *',
           '*****    *   *',
           '*        *   *',
           '* |  *****   *',
           '*        *   *',
           '******** *   *',
           '*            *',
           '* |     |*   *',
           '**************']           
levels = [level_1, level_2,level_3]         
window = display.set_mode((WEIGHT, HEIGHT))
display.set_caption('Concept')

background = transform.scale(image.load("Sprites/1273.jpg").convert_alpha(),(WEIGHT, HEIGHT))


you_win = font.SysFont('verdana', 70).render("YOU WIN!", True, YELLOW)
you_lose = font.SysFont('verdana', 70).render("YOU LOSE!", True, RED)



class Map():
    def __init__(self,texture_wall,texture_final,texture_monster,level):
        self.map = level
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
                elif self.map[i][j] == '$':
                    self.player = Hero(50*j,50*i,50,50,'Sprites/kisspng-skeleton-2d-computer-graphics-sprite-two-dimension-5b004d06f2c287.2692903915267463749944.png')             
    def reset(self, surface):
        self.walls.draw(surface)
        self.portal.draw(surface)
        self.monsters.draw(surface)
        self.monsters.update(self.walls,self.player)


        
                 
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
        self.speeds = [[0,5],[-5,0],[0,-5],[5,0]]
        self.direction = 0
        self.bullets = sprite.Group()
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
    def fire(self):
        self.bullets.add(Bullet(self.rect.x, self.rect.y, 20, 20, 'Sprites/bullet.png',self.speeds[self.direction]))


class Bullet(GameSpite):
    def __init__(self,x, y, w, h,picture,direction):
        super().__init__(x, y, w, h, picture)
        self.speed_x = direction[0]
        self.speed_y = direction[1]
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if sprite.spritecollide(self, land.walls,False):
            self.kill()
        elif sprite.spritecollide(self, land.monsters,False):
            self.kill()  



class Monster(GameSpite):
    def __init__(self,x, y, w, h,picture):
        super().__init__(x, y, w, h, picture)
        self.speeds = [[0,5],[-5,0],[0,-5],[5,0]] #UP LEFT DOWN RIGHT
        self.direction = 0
        self.speed_x,self.speed_y = self.speeds[self.direction][0],self.speeds[self.direction][1]
    def update(self,walls,player):
        if sprite.spritecollide(self, walls,False):
            self.rect.y -= self.speed_y 
            self.rect.x -= self.speed_x
            self.speed_x,self.speed_y = self.speeds[self.direction][0],self.speeds[self.direction][1]
            if self.direction != (len(self.speeds) -1):
                self.direction += 1
                print(self.direction)
            else:
                self.direction = 0
        rand = randint(0,1000)
        if rand == 5:
            self.speed_y *= -1
        elif rand == 9:
            self.speed_x *= -1 
        elif rand == 10:
            self.speed_x,self.speed_y = self.speeds[self.direction][0],self.speeds[0][1] 
        elif rand == 15:
            self.speed_x,self.speed_y = self.speeds[self.direction][0],self.speeds[2][1]
        elif rand == 20:
            self.speed_x,self.speed_y = self.speeds[self.direction][0],self.speeds[1][1] 
        elif rand == 15:
            self.speed_x,self.speed_y = self.speeds[self.direction][0],self.speeds[3][1]    
        if self.rect.y == player.rect.y:
            if  player.rect.x >= self.rect.x:
                self.speed_x,self.speed_y = self.speeds[3][0],self.speeds[3][1]
            if  player.rect.x < self.rect.x: 
                self.speed_x = -5
                self.speed_y = 0

        if self.rect.x == player.rect.x:
            if  player.rect.y >= self.rect.y:
                self.speed_x,self.speed_y = self.speeds[0][0],self.speeds[0][1]
            if  player.rect.y < self.rect.y: 
                self.speed_x = 0
                self.speed_y = -5       

        self.rect.y += self.speed_y 
        self.rect.x += self.speed_x
        if sprite.spritecollide(self, player.bullets,False):
            self.kill()

 #картинку поменять
    



clock = time.Clock()
land = Map("Sprites/realistic-red-color-brick-wall-seamless-pattern_251819-2333.jpg","Sprites/final.png","Sprites/ghost.png",levels[0]) # картинку свою 
run = True
finish = False
lv = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN: #UP LEFT DOWN RIGHT
            if e.key == K_w:
                land.player.speed_y = -5
            elif e.key == K_s:
                land.player.speed_y = 5

            elif e.key == K_d:
                land.player.speed_x = 5

            elif e.key == K_a:
                land.player.speed_x = -5


            if e.key == K_UP:    
                land.player.direction = 2
            elif e.key == K_DOWN:    
                land.player.direction = 0
            elif e.key == K_RIGHT:    
                land.player.direction = 3
            elif e.key == K_LEFT:    
                land.player.direction = 1            
            if e.key == K_SPACE:
                land.player.fire()     
            if e.key == K_SPACE and finish == True:                
                land = Map("Sprites/realistic-red-color-brick-wall-seamless-pattern_251819-2333.jpg","Sprites/final.png","Sprites/ghost.png",levels[0]) # картинку свою 
                run = True
                finish = False   
        elif e.type == KEYUP:
            if e.key == K_w:
                land.player.speed_y = 0
            elif e.key == K_s:
                land.player.speed_y = 0
            elif e.key == K_d:
                land.player.speed_x = 0
            elif e.key == K_a:
                land.player.speed_x = 0
    if finish == False:
        display.set_caption(str(int(clock.get_fps())))               
        #window.blit(background, (0, 0))
        window.fill((0, 0, 0))
        land.reset(window)
        land.player.bullets.draw(window)
        land.player.bullets.update()
        land.player.draw(window)
        display.update()
        clock.tick(60)
        if sprite.collide_rect(land.player, land.portal):
            lv += 1
            if lv != len(levels):
                land = Map("Sprites/realistic-red-color-brick-wall-seamless-pattern_251819-2333.jpg","Sprites/final.png","Sprites/ghost.png",levels[lv]) 
            else:        
                window.blit(you_win,(WEIGHT/2-150, HEIGHT/2-50))
                display.update()
                finish = True
        if sprite.spritecollide(land.player, land.monsters,False):
            window.blit(you_lose,(WEIGHT/2-150, HEIGHT/2-50))
            display.update()
            finish = True                
        if sprite.spritecollide(land.player, land.walls,False):
            land.player.rect.x =  pred_x
            land.player.rect.y = pred_y
        else:
            pred_x = land.player.rect.x
            pred_y = land.player.rect.y        
            land.player.move()             

    else:
        lv = 0
        display.update()           
          