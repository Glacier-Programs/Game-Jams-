from pygame.sprite import Sprite
import pygame as pg

SCREEN_WIDTH = 0
SCREEN_HEIGIHT = 0

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
        #player appearnce (will change later)
        self.surf2 = pg.Surface((width,height))
        self.surf2.fill((255,0,0))
        #hitbox
        self.rect = self.surf2.get_rect()
        #other
        self.sprites = []
        self.vel = [0,0]
    def move(self,vel):
        self.vel = vel
        self.coords[0] += self.vel[0]
        self.coords[1] += self.vel[1]
        self.rect.move_ip(self.vel[0],self.vel[1])
        #collision detection
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

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
            x -= 5
        if self.player.coords[0] > self.coords[0]:
            x += 5
        if self.player.coords[1] - 10 < self.coords[1]:
            y -= 5
        if self.player.coords[1] - 10 > self.coords[1]:
            y += 5
        self.vel = [x,y]
        self.rect.move_ip(self.vel[0],self.vel[1])
        self.coords[0] += x
        self.coords[1] += y + 20
    def set_mode(self):
        if self.mode < 1:
            self.mode += 1
        else:
            self.mode = 0