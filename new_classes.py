from pygame.sprite import Sprite
from pygame.surface import Surface
import pygame as pg
from random import randint, choice

class Platform(Sprite):
    def __init__(self,surf,coords,width,height,sprite=None):
        super().__init__()
        self.surf = surf
        self.width = width
        self.height = height
        self.lCoords = coords #level coords
        self.rCoords = coords #relative coords
        self.sprite = sprite
    def randomSprite(self,area,Type,reps,h=True,v=False):
        start = 'imgs/'+area+'-'+Type+'-'
        sprite = Surface((50,50))
        if v:
            h = False
        for i in range(0,reps):
            img = start + str(randint(1,3)) + '.png'
            if h: sprite.blit(pg.image.load(img),(i*50,0))
            else: sprite.blit(pg.image.load(img),(0,i*50))
            return sprite
    def constructSprite(self,file,reps,h=True,v=False):
        sprite = pg.Surface((self.width,self.height))
        for i in range(0,reps):
            if h: sprite.blit(pg.image.load(file),(i*50,0))
            else: sprite.blit(pg.image.load(file),(0,i*50))
        return sprite
    def render(self):
        if self.sprite == None: print('No Sprite: ', self)
        else: self.surf.blit(self.sprite,self.rCoords)
        
class Ground(Platform):
    def __init__(self,surf,area,coords,width):
        super().__init__(surf,coords,width,50)
        self.sprite = self.randomSprite(area,'ground',width//50)
        
class Wall(Platform):
    def __init__(self,surf,area,coords,height):
        super().__init__(surf,coords,50,height)
        self.sprite = self.randomSprite(area,'wall-right',height//50)

class StatPlat(Platform): #stationary platform
    def __init__(self,surf,coords,width,sprite):
        super().__init__(surf,coords,width,50)
        self.sprite = self.constructSprite(sprite,width//50)

class FallPlat(Platform): #falling platform
    def __init__(self,surf,coords,width,sprite,fallSpeed=10):
        super().__init__(surf,coords,width,50)
        self.sprite = self.constructSprite(sprite,width//50)
        self.fallSpeed = fallSpeed
        self.wasTouched = False
    def render(self):
        if self.wasTouched: self.coords[1] -= self.fallSpeed
        if self.coords[1] > 400: self.kill()
        else: self.surf.blit(self.sprite,self.coords)

class Door(Sprite):
    def __init__(self,surf,coords):
        self.surf = surf
        self.rCoords = coords
        self.lCoords = coords
        self.height,self.width = 50,50
        self.sprite = pg.image.load('imgs/door.png')
    def render(self):
        self.surf.blit(self.sprite,self.rCoords)

class Player(Sprite):
    def __init__(self,coords,width,height):
        super().__init__()
        self.coords = coords
        self.width = width
        self.height = height
        self.sprite = pg.image.load('imgs/player-female-1.png')
        self.touchingGround = False
        self.toucingWall = False
        self.jumping = False
    def move(self,objs,dx,dy):
        #reset values
        self.touchingGround = False
        self.touchingWall = False
        #gravity
        if not self.touchingGround and not self.jumping:
            if not self.touchingWall: dy += 10
            else: dy += 5
        #check x collision
        self.coords[0] += dx
        for obj in objs:
            if self.collision(obj):
                self.coords[0] -= dx
                self.touchingWall = True
        #check y collision
        self.coords[1] += dy
        for obj in objs:
            if self.collision(obj):
                self.coords[1] -= dy
                self.touchingGround = False
    def set_surf(self,surf):
        self.surf = surf
    def render(self):
        self.surf.blit(self.sprite,self.coords)

    def collision(self,obj):
        xCase = obj.lCoords[0] < self.coords[0]+self.width and obj.lCoords[0]+obj.width > self.coords[0]
        yCase = obj.lCoords[1] < self.coords[1]+self.height and obj.lCoords[1]+obj.height > self.coords[1]
        if xCase and yCase:
            return True
        else:
            return False

class Pixie(Sprite):
    def __init__(self):
        super().__init__()

class Lantern(Sprite):
    def __init__(self,win,player,coords):
        super().__init__()
        self.player = player
        self.coords = coords
        self.lightLevel = 2
        self.light = Light(win,self,1*25)
        self.mode = 0
    def move(self):
        x,y = 0,0
        if self.player.coords[0] < self.coords[0]:
            x -= 10
        elif self.player.coords[0] > self.coords[0]:
            x += 10
        if self.player.coords[1] - 20 < self.coords[1]:
            y -= 10
        elif self.player.coords[1] - 20 > self.coords[1]:
            y += 10
        self.vel = [x,y]
        self.coords[0] += x
        self.coords[1] += y
    def set_mode(self,mode):
        self.mode = mode
    def render(self):
        self.light.blit(self.sprite,(100,100))

class Background(Sprite):
    def __init__(self):
        super().__init__()

class Light(Sprite):
    def __init__(self,win,master,radius):
        super().__init__()
        self.radius = radius
        self.maxRadius = 100
        self.win = win
        self.master = master
        self.sprites = pg.sprite.Group()
        self.surf = pg.Surface((radius*2,radius*2))
        self.rect = self.surf.get_rect()
        self.add_sprites([self.master.player,self.master])
    def add_sprites(self,sprites):
        for sprite in sprites:
            self.sprites.add(sprite)
    def update(self,vel):
        x,y = 0,0
        if self.master.coords != self.coords:
                if self.master.coords[0] > self.coords[0]:
                    if self.master.coords[0] - self.coords[0] < 10:
                        x -= self.master.coords[0] - self.coords[0]
                    else:
                        x -= 10
                elif self.master.coords[0] < self.coords[0]:
                    if self.coords[0] - self.master.coords[0] < 10:
                        x += self.coords[0] - self.master.coords[0]
                    else:
                        x += 10
                if self.master.coords[1] > self.coords[1]:
                    if self.master.coords[1] - self.coords[1] < 10:
                        y += self.master.coords[1] - self.coords[1]
                    else:
                        y += 10
                elif self.coords[1] > self.master.coords[1]:
                    if self.coords[1] - self.master.coords[1] < 10:
                        y -= self.coords[1] - self.master.coords[1]
                    else:
                        y -= 10
        for sprite in self.sprites:
            sprite.move()
        self.rect.move_ip(x,y)
        self.win.blit(self.surf,self.rect)