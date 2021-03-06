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
    def relMove(self,dx,dy):
        self.rCoords[0] += dx
        self.rCoords[1] += dy
    def renderToLight(self,light):
        lightCoords = [ self.lCoords[0] - light.coords[0],
            self.lCoords[1] - light.coords[1]]
        if light.up: lightCoords[1] += light.upCompensation
        if light.right: lightCoords[0] += light.rightCompensation
        light.blit(self.sprite,lightCoords)
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
        self.sprite = pg.image.load('imgs/platform.png')
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
    def relMove(dx,dy):
        self.rCoords[0] += dx
        self.rCoords[1] += dy
    def render(self):
        self.surf.blit(self.sprite,[self.rCoords[0],self.rCoords[1]+1])
    def renderToLight(self,light):
        lightCoords = [ self.lCoords[0] - light.coords[0],
                        self.lCoords[1] - light.coords[1]]
        if light.up: lightCoords[1] += light.upCompensation
        if light.right: lightCoords[0] += light.rightCompensation
        light.blit(self.sprite,lightCoords)

class Player(Sprite):
    def __init__(self,coords,width,height):
        super().__init__()
        self.sub = 'player'
        self.coords = coords
        self.width = width
        self.height = height
        self.sprite = pg.image.load('imgs/player-female-1.png')
        self.touchingGround = False
        self.toucingWall = False
        self.jumping = False
        self.lightCoords = [0,0]
    def moveToLantern(self, lanternCoords):
        # Add/Subtract 5 to create a margin so it does not flash back and forth.
        # Move x direction
        xAlign, yAlign = False, False
        if self.coords[0] < lanternCoords[0] - 5: # Move right
            self.coords[0] += 10
        elif self.coords[0] > lanternCoords[0] + 5: # Move Left
            self.coords[0] -= 10
        else:
            xAlign = True
        # Move y direction
        if self.coords[1] > lanternCoords[1] + 5: # Move up
            self.coords[1] -= 10
        elif self.coords[1] < lanternCoords[1] - 5: # Move down
            self.coords[1] += 10
        else:
            yAlign = True
        # If they are both aligned then we stop grappling resulting in False
        return not (xAlign and yAlign)
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
    def relMove(self,dx,dy):
        self.rCoords[0] += dx
        self.rCoords[1] += dy
    def render(self): 
        self.surf.blit(self.sprite,self.coords)
    def renderToLight(self,light):
        lightCoords = [ self.coords[0] - light.coords[0],
            self.coords[1] - light.coords[1]]
        if light.right: lightCoords[0] += light.rightCompensation
        light.blit(self.sprite,lightCoords)
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
        self.sub = 'lantern'
        self.playerGrappling = False
        # You can not set it equal to coord or else it will be equal to playerCoords
        self.coords = [coords[0], coords[1]]
        self.lightLevel = 2
        self.light = Light(win,self,self.lightLevel*25)
        #depletion
        self.maxDeplete = 100
        self.deplete = 0
        # Mode 0: Tracking Mode | Mode 1: Stay Mode
        self.mode = 0
        self.sprite = Surface((20,20))
        self.sprite.fill((255,255,0))
        self.surf = win
        self.trackingCoords = player.coords
    def checkGrapplingHook(self, playPos):
        # 20 is the lightbox width and height
        xCase = playPos[0] > self.coords[0] and playPos[0] < self.coords[0] + 20
        yCase = playPos[1] > self.coords[1] and playPos[1] < self.coords[1] + 20
        self.playerGrappling = xCase and yCase
    def moveCoords(self, x, y):
        self.coords[0] += x
        self.coords[1] += y
    def move(self):
        laternSpeed = 5
        # 40 is the distance between the lantern and the player
        x = self.trackingCoords[0]
        y = self.trackingCoords[1] - 40
        if x - 5 > self.coords[0]: # Lantern moves right
            self.coords[0] += laternSpeed
        elif x + 5 < self.coords[0]: # Lantern moves left
            self.coords[0] -= laternSpeed
        if y - 5 > self.coords[1]: # Lantern moves Down
            self.coords[1] += laternSpeed
        elif y + 5 < self.coords[1]: # Lantern moves Up
            self.coords[1] -= laternSpeed
        if self.mode == 1:
            if self.deplete // 10 < self.maxDeplete:
                self.deplete += 1
    def set_mode(self,mode):
        self.mode = mode
    def render(self):
        self.surf.blit(self.sprite, self.coords)
        self.light.update()
    def renderToLight(self,light):
        light.blit(self.sprite,(90,90))

class Background(Sprite):
    def __init__(self):
        super().__init__()

class Light(Surface):
    def __init__(self,win,master,radius):
        #set variables
        super().__init__((200,200)) #change this if maxRadius changes
        self.radius = radius
        self.maxRadius = 100
        self.win = win
        self.master = master
        #co-ordinates
        self.coords = [master.coords[0]-100,master.coords[1]-100]
        self.chase = master.coords
        #adjust offset from going right / down / grappling
        self.right = False
        self.rightCompensation = -10
        self.up = False
        self.upCompensation = -10
        #set up what will be used to draw
        self.sprites = pg.sprite.Group()
        self.add_sprites([self.master])
    def add_sprites(self,sprites):
        for sprite in sprites:
            self.sprites.add(sprite)
    def remove_sprite(self,sprite):
        self.sprites.remove(sprite)
    def update(self):
        x,y = 0,0
        self.right, self.up = False,False
        print('m',self.master.coords)
        print('l',self.coords)
        chaseX = self.chase[0]-100
        chaseY = self.chase[1]-100
        if [chaseX,chaseY] != self.coords:
                # offset in order to make the lantern its center
                if chaseX > self.coords[0]:
                    if self.master.coords[0] - self.coords[0] < 10:
                        x += chaseX - self.coords[0]
                    else:
                        x += 10
                elif chaseX < self.coords[0]:
                    if self.coords[0] - chaseX < 10:
                        x -= self.coords[0] - chaseX
                    else:
                        x -= 10
                if chaseY > self.coords[1]:
                    if chaseY - self.coords[1] < 10:
                        y += chaseY - self.coords[1]
                    else:
                        y += 10
                elif chaseY < self.coords[1]:
                    if self.coords[1] - chaseY < 10:
                        y -= self.coords[1] - chaseY
                    else:
                        y -= 10
        self.fill((15,111,225))
        
        if x > 0:
            self.right = True
        if y < 0:
            self.right = True
    
        for sprite in self.sprites:
            if sprite != self.master:
                sprite.renderToLight(self)
        self.master.renderToLight(self)
        #light depletion
        border_size = self.master.deplete // 10
        spot = 200-border_size
        self.blit(Surface((200,border_size)),(0,0)) # top
        self.blit(Surface((border_size,200)),(0,0)) # left
        self.blit(Surface((200,border_size)),(0,spot)) # bottom
        self.blit(Surface((border_size,200)),(spot,0)) # right
        #other stuffs
        self.coords[0] += x
        self.coords[1] += y
        self.win.blit(self,self.coords)
        
class Power(Sprite):
    def __init__(self,surf,coords):
        super().__init__()
        self.sub = 'power'
        self.surf = surf
        self.rCoords = coords
        self.lCoords = coords
        self.height,self.width = 75,50
        self.sprite = pg.image.load('imgs/powerUp.png')
        # This keeps track of where power is in the level list. So we can delete it later
        self.levelIndex = 0
        self.used = False

    def isTouchingPowerUp(self, playCoords, width, height):
        # This skips over it if we have gotten rid of it.
        if self.used:
            return False
        xCase = playCoords[0]+width > self.lCoords[0] and playCoords[0] < self.lCoords[0] + self.width
        yCase = playCoords[1]+height > self.lCoords[1] and playCoords[1] < self.lCoords[1] + self.height    
        return xCase and yCase

    def render(self):
        self.surf.blit(self.sprite,[self.rCoords[0],self.rCoords[1]+1])
    
    def renderToLight(self,light):
        lightCoords = [ self.lCoords[0] - light.coords[0],
            self.lCoords[1] - light.coords[1]]
        if light.up: lightCoords[1] += light.upCompensation
        if light.right: lightCoords[0] += light.rightCompensation
        light.blit(self.sprite,lightCoords)
