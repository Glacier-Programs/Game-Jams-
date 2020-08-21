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
touchingPlatform = False

#lantern
lantern = classes.Lantern(win,player,[0,0])

#sprite groups
allSprites = pg.sprite.Group()
allSprites.add(player)
allSprites.add(lantern)

platforms = pg.sprite.Group()
enemies = pg.sprite.Group()

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
    if pressed[pg.K_SPACE] and not jumping and canjump:
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
    if not pg.sprite.spritecollideany(player,platforms) and not jumping:
        y += 10
        #canjump = False
    else:
        touchingPlatform = True
        canjump = True
    #move stuffs
    player.move([x,y])
    lantern.move()
    
    #draw stuffs
    for entity in allSprites:
        win.blit(entity.surf2,entity.rect)
    
    #update screen
    pg.display.flip()
    clock.tick(60)

pg.quit()