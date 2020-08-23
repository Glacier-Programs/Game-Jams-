from pygame.sprite import Sprite
from random import randint
import pygame as pg

SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0

def start(width,height):
    global SCREEN_WIDTH, SCREEN_HEIGHT
    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height
    

class Player(Sprite):
    def __init__(self,surf,coords,width=20,height=20):
        super().__init__()
        self.surf = surf
        self.width = width
        self.height = height
        self.coords = coords
        #player appearence (will change later)
        self.surf2 = pg.Surface((width,height))
        self.surf2.fill((255,0,0))
        #hitbox
        self.rect = self.surf2.get_rect()
        #other
        self.sprites = []
        self.vel = [0,0]
        self.touchingWall = False
    def col_check(self,collidables,direction):
        for collidable in collidables:
            if self.rect.colliderect(collidable.rect):
                if direction[0] > 0:
                    self.rect.right = collidable.rect.left
                    self.touchingWall = True
                elif direction[0] < 0:
                    self.rect.left = collidable.rect.right
                    self.touchingWall = True
                else:
                    self.touchingWall = False

    def move(self,vel,collidables):
        self.vel = vel
        #self.col_check(collidables,[vel[0],0])
        self.coords[0] += self.vel[0]
        #self.col_check(collidables,[0,vel[1]])
        self.coords[1] += self.vel[1]
        self.rect.move_ip(self.vel[0],self.vel[1])
        #collision detection
        if self.rect.left < 0:
            self.rect.left = 0
            self.coords[0] = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.coords[0] = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.coords[1] = SCREEN_HEIGHT

    def respawn(self,coords):
        self.rect.left = coords[0]
        self.rect.top = coords[1]
        self.coords[0] = coords[0]
        self.coords[1] = coords[1]
        
class Lantern(Sprite):
    def __init__(self,surf,player,coords,width=10,height=10):
        super().__init__()
        self.surf = surf
        self.player = player
        self.coords = coords
        self.width = width
        self.height = height
        #sprite
        self.surf2 = pg.Surface((width,height))
        self.surf2.fill((255,255,0))
        self.sprites = []
        #hitbox
        self.rect = self.surf2.get_rect()
        #other
        self.vel = [0,0]
        self.mode = 0 #0 = follow, 1 = stay
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
        self.rect.move_ip(self.vel[0],self.vel[1])
        self.coords[0] += x
        self.coords[1] += y
    def set_mode(self):
        if not mode:
            mode = 1
        else:
            mode = 0

class PlatformBrain():

    # Change this to make it more smart. So it is random but places platforms so they make sense based
    # on the last platform created
    def getNewPlatformPosition(self, lastPlatformCoords):
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

    # If the last platform is a little less then half way through the screen a new one is made
    def shouldPlatformBeCreated(self, platformCoords):
        lastPlatform = len(platformCoords) - 1
        return platformCoords[lastPlatform][0] <= 250

        


class Platform(Sprite):
    def __init__(self,surf,coords,width):
        super().__init__()
        # Set all the variables
        self.surf = surf
        self.coords = coords
        self.width = width
        self.surf2 = pg.Surface((width, 50))
        # Change the fileName to the platform file
        fileName = "imgs/dungeon-ground-1.png"
        self.surf2.blit(pg.image.load(fileName), (0, 0))

        self.rect = self.surf2.get_rect()
        self.rect.left = coords[0]
        self.rect.top = coords[1]

    # This just moves the rect
    def move(self, moveRate): 
        self.rect.move_ip(-moveRate, 0)

class Float(Sprite):
    def __init__(self,surf,coords,width=10,height=10):
        super().__init__()
        self.surf = surf
        self.coords = coords
        self.width = width
        self.surf2 = pg.Surface((width,height))
        self.rect = self.surf2.get_rect()
        self.rect.top = coords[1]
        self.rect.left = coords[0]

class Ground(Sprite):
    def __init__(self,surf,area,coords,width=400): # area: 0 - dungeon, 1 - castle main, 2 - Castle spire, 3 - outside
        super().__init__()
        self.surf = surf
        self.coords = coords
        self.width = width
        #make background
        self.surf2 = pg.Surface((width, 50))
        if area == 0:
            temp = 'imgs/dungeon-ground-'
        elif area == 1:
            temp = 'imgs/hall-ground-'
        elif area == 2:
            temp = 'imgs/spire-ground-'
        elif area == 3:
            temp = 'imgs/out-ground-'
        for i in range(0,width//50):
            img = temp+str(randint(1,3)) + '.png'
            self.surf2.blit(pg.image.load(img),(i*50,0))
        self.rect = self.surf2.get_rect()
        self.rect.left = coords[0]
        self.rect.top = coords[1]

    # This is to check whether something touches the ground
    def touchingGround(self, playerCoords):
        # 20 is for the player Height
        x = playerCoords[0]
        y = playerCoords[1] + 20
        xRange = x >= self.coords[0] and x <= self.coords[0] + self.width
        yRange = y <= self.coords[1] and y >= self.coords[1] - 5 # 5 is the margin where the player stays on the ground
        if xRange and yRange:
            return True
        return False

class Wall(Sprite):
    def __init__(self,surf,area,side,coords,height = 400): # same areas as ground
        super().__init__()
        self.surf = surf
        self.side = side
        self.coords = coords
        self.height = height
        self.width = 50
        self.surf2 = pg.Surface((self.width,height))
        if side:
            sade = 'left' # side add (for img file name)
        else:
            sade = 'right'
        if area == 0:
            temp = 'imgs/dungeon-wall-'+sade+'-'
        elif area == 1:
            temp = 'imgs/hall-wall-'+sade+'-'
        elif area == 2:
            temp = 'imgs/spire-wall-'+sade+'-'
        elif area == 3:
            temp = 'imgs/out-wall-'+sade+'-'
        for i in range(0,height//50):
            img = temp+str(randint(1,3))+'.png'
            self.surf2.blit(pg.image.load(img),(0,i*50))
        self.rect = self.surf2.get_rect()
        self.rect.left = coords[0]
        self.rect.top = coords[1]
    
    def onTopWall(self, playerCoords):
        # 20 is for the player Height
        x = playerCoords[0]
        y = playerCoords[1] + 20
        xRange = x >= self.coords[0] and x <= self.coords[0] + self.width
        yRange = y <= self.coords[1] and y >= self.coords[1] - 5 # 5 is the margin where the player stays on the wall
        if xRange and yRange:
            return True
        return False

    def onSideWall(self, playerCoords):
        x = playerCoords[0]
        y = playerCoords[1]
        # 5 is the margin to how close the player is to the wall
        if x+20 >= self.coords[0] - 5 and x+20 <= self.coords[0] and y > self.coords[1]:
            return [True, False]
        if x <= self.coords[0] + self.width + 5 and x >= self.coords[0] + self.width and y > self.coords[1]:
            return [False, True]
        return [False, False]

class Background(Sprite):
    pass

class Light(Sprite):
    def __init__(self,win,master,coords,radius):
        super().__init__()
        self.radius = radius
        self.win = win
        self.master = master
        self.coords = coords
        self.surf = pg.Surface((radius*2,radius*2))
        self.rect = self.surf.get_rect()
    def move(self,vel):
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
        self.rect.move_ip(x,y)
        self.win.blit(self.surf,self.rect)
