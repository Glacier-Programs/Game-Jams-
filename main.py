import pygame as pg
import classes

pg.init()

clock = pg.time.Clock()

#screen
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
win = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pg.display.set_caption('Lights Out')
classes.start(SCREEN_WIDTH,SCREEN_HEIGHT)

#player
player = classes.Player(win,[0,0])
jumping = False
canjump = True
jump_max = 100
jump_height = 0
airTime = 0
maxAirTime = 5
touchingPlatform = False

#lantern
lantern = classes.Lantern(win,player,[0,0])

#sprite groups
allSprites = pg.sprite.Group()
allSprites.add(player)
allSprites.add(lantern)

platforms = pg.sprite.Group()
enemies = pg.sprite.Group()

#ground for demo
ground1 = classes.Ground(win,0,[0,350],width=200)
allSprites.add(ground1)
platforms.add(ground1)
ground2 = classes.Ground(win,0,[300,350],width=200)
allSprites.add(ground2)
platforms.add(ground2)

#main
done = False
while not done:
    #fill screen with black
    win.fill((0,0,0))
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    
    #key presses
    pressed = pg.key.get_pressed()
    x,y = 0,0
    if pressed[pg.K_SPACE] and not jumping and touchingPlatform:
        jumping = True
    if pressed[pg.K_a]:
        x -= 10
        print('moved')
    if pressed[pg.K_d]:
        x += 10
    if jumping:
        if jump_height >= jump_max:
            jumping = False
            jump_height = 0
        else:
            y -= 10
            jump_height += 10
    #checks if it should fall
    if not pg.sprite.spritecollideany(player,platforms):
        touchingPlatform = False
    else:
        touchingPlatform = True
        canjump = True
    if not touchingPlatform and not jumping:
        y += 10
    #move stuffs
    player.move([x,y])
    lantern.move()
    
    #draw stuffs
    for entity in allSprites:
        win.blit(entity.surf2,entity.rect)
        print(entity)
    
    #update screen
    pg.display.flip()
    clock.tick(60)

pg.quit()
