from pygame.sprite import Sprite
from pygame.surface import Surface
import pygame as pg
from random import randint, choice

class Platform(Sprite):
    def __init__(self,surf,coords,width,height,sprite=None):
        super().__init__()
        self.surf = surf
        self.sub = 'platform'
        self.width = width
        self.height = height
        self.lCoords = coords #level coords
        self.rCoords = coords #relative coords
        self.sprite = sprite
    def randomSprite(self,area,Type,reps,height,width,h=True,v=False):
        start = 'imgs/'+area+'-'+Type+'-'
        sprite = Surface((width,height))
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
    def move(self,dx,dy):
        self.lCoords[0] += dx
        self.lCoords[1] += dy
    def render(self):
        if self.sprite == None: print('No Sprite: ', self)
        else: self.surf.blit(self.sprite,self.rCoords)
        
class Ground(Platform):
    def __init__(self,surf,area,coords,width):
        super().__init__(surf,coords,width,50)
        self.sprite = Surface((width,50))
        for i in range(0,width//50):
            img = 'imgs/'+area+'-ground-'+str(randint(1,3)) + '.png'
            self.sprite.blit(pg.image.load(img),(i*50,0))
        
class Wall(Platform):
    def __init__(self,surf,area,coords,height):
        super().__init__(surf,coords,50,height)
        self.sprite = Surface((50,height))
        for i in range(0,height//50):
            img = 'imgs/'+area+'-wall-right-'+str(randint(1,3))+'.png'
            self.sprite.blit(pg.image.load(img),(0,i*50))

class StatPlat(Platform): #stationary platform
    def __init__(self,surf,coords,width,sprite):
        super().__init__(surf,coords,width,20)
        self.sprite = pg.image.load(sprite)
    def render(self):
        self.surf.blit(self.sprite,[self.rCoords[0],self.rCoords[1]-20])

class FallPlat(Platform): #falling platform
    def __init__(self,surf,coords,width,sprite,fallSpeed=10):
        super().__init__(surf,coords,width,50)
        self.sprite = self.constructSprite(sprite,width//50)
        self.fallSpeed = fallSpeed
        self.wasTouched = False
    def render(self):
        if self.wasTouched: self.move(0,-self.fallSpeed)
        if self.coords[1] > 400: self.kill()
        else: self.surf.blit(self.sprite,self.coords)

class PlatformBrain():
    #make this smarter and more dependant on previous platforms
    def getNewPlatformPosition(self,lastPlatformCoords):
        # 400 starts at the very right of the screen
        xPosition = 400
        # 350 is the maximum or else the platform will go through the ground
        yPosition = 0
        if lastPlatformCoords[1] <= 133: # Platform is in the top third
            yPosition = randint(50, 350)
        elif lastPlatformCoords[1] <= 266: # Platform is in the middle third  
            yPosition = randint(150, 300)
        else: # Platform is on the bottom third
            yPosition = randint(225, 300)

        return [xPosition, yPosition]
    def shouldPlatformBeCreated(self, platformCoords):
        lastPlatform = len(platformCoords) - 1
        return platformCoords[lastPlatform][0] <= 250

class Door(Sprite):
    def __init__(self,surf,coords):
        super().__init__()
        self.sub = 'door'
        self.surf = surf
        self.rCoords = coords
        self.lCoords = coords
        self.height,self.width = 50,50
        self.sprite = pg.image.load('imgs/door.png')
    def render(self):
        self.surf.blit(self.sprite,[self.rCoords[0],self.rCoords[1]+1])

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
                self.touchingGround = True
        xScreen = self.coords[0] > 400 or self.coords[0] < 0
        yScreen = self.coords[1] > 400
        if yScreen or xScreen:
            self.respawn([100,100])
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
    def respawn(self,spot):
        self.coords = spot

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
        self.sprite = Surface((20,20))
        self.sprite.fill((255,255,0))
    def move(self):
        x,y = 0,0
        if self.player.coords[0] < self.coords[0]:
            x -= 10
        elif self.player.coords[0] > self.coords[0]:
            x += 10
        if self.player.coords[1] - 40 < self.coords[1]:
            y -= 10
        elif self.player.coords[1] - 40 > self.coords[1]:
            y += 10
        self.vel = [x,y]
        self.coords[0] += x
        self.coords[1] += y
    def set_mode(self,mode):
        self.mode = mode
    def render(self):
        self.player.surf.blit(self.sprite,self.coords)
        #self.light.blit(self.sprite,(100,100))

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
        self.surf.fill((0,0,0))
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
