import pygame as pg
import new_classes
import menu

pg.init()
menu.init({'buttons':pg.font.SysFont('dejavuserif',40),'title':pg.font.SysFont('lato',60),'header':pg.font.SysFont('lato',30),'text':pg.font.SysFont('dejavuserif',20)})

clock = pg.time.Clock()

#screen
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
win = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pg.display.set_caption('Lights Out')

#player
player = new_classes.Player([0,0],20,40)
player.set_surf(win)
jumping = False
canjump = True
jump_max = 100
jump_height = 0
airTimeList = [0,20] # current , max
touchingPlatform = False
touchingWall = False

# Lantern
#lantern = new_classes.Lantern(win,player,[0,0])

# Sprite groups
allSprites = pg.sprite.Group()
allSprites.add(player)
#allSprites.add(lantern)

platforms = pg.sprite.Group()
enemies = pg.sprite.Group()
hfloats = pg.sprite.Group()
vfloats = pg.sprite.Group()

# Ground
ground = [new_classes.Ground(win,'dungeon',[0,350],200), new_classes.Ground(win,'dungeon',[300,350],200)]
allSprites.add(ground[0])
allSprites.add(ground[1])

# platform
MOVE_RATE = 1
brain = new_classes.PlatformBrain()

platformCoords = [[400, 275]]
allPlatForms = [new_classes.Ground(win,'dungeon',platformCoords[0],50)]
allSprites.add(allPlatForms[0])
platforms.add(allPlatForms[0])

# Wall
wall = [new_classes.Wall(win,'dungeon',[150,250],100)]
allSprites.add(wall[0])
platforms.add(wall)

#main menu
done = menu.start(win)

#game
while not done:
    #fill screen with black
    win.fill((0,0,0))
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    '''     
    # Checks if touching ground
    # Go through all Ground new_classes and sees if they collide with the player.
    isTouchingGround = False
    for i in range(0, len(ground)):
        if ground[i].touchingGround(player.coords):
            touchingPlatform = True
            canJump = True
            isTouchingGround = True
            # Once we touch one ground we can not touch any other ground so we break
            break
        else:
            touchingPlatform = False

    # Checks if touching platforms if we are not touching ground
    if not isTouchingGround:
        counter = 0
        # 20 is for the player Height
        playX = player.coords[0]
        playY = player.coords[1] + 20
        for i in range(0, len(platformCoords)):
            # 50 is the platform Width
            # 5 is the margin where the player can stay on the platform
            xRange = playX + 20 >= platformCoords[i][0] and playX <= platformCoords[i][0] + 50
            yRange = playY <= platformCoords[i][1] and playY >= platformCoords[i][1] - 5
            counter += 1
            if xRange and yRange:
                touchingPlatform = True
                canjump = True
                break
            else:
                touchingPlatform = False

    # 0 is touching the left side and 1 is touching the right side
    isTouchingWall = [False, False]
    # Checks if touching a wall
    for i in range(0, len(wall)):
        # If the player is ontop of the wall
        if wall[i].onTopWall(player.coords):
            touchingPlatform = True
            canJump = True
            break
        # If the player is next to the wall
        isTouchingWall = wall[i].onSideWall(player.coords)
        if isTouchingWall[0] or isTouchingWall[1]:
            break'''

    
    # I moved this chunk of code to have the touchingWall variable easier to access
    #key presses
    pressed = pg.key.get_pressed()
    x,y = 0,0
    if pressed[pg.K_SPACE] and (not jumping and player.touchingGround or player.touchingWall):
        player.jumping = True
    if pressed[pg.K_a] and not player.touchingWall:
        x -= 5
    if pressed[pg.K_d] and not player.touchingWall:
        x += 5
    if player.jumping:
        if jump_height >= jump_max:
            player.jumping = False
            jump_height = 0
        else:
            y -= 20
            jump_height += 10
        
    #airtime / coyote time
    if not touchingPlatform and not jumping:
        if airTimeList[0] <= airTimeList[1]:
            airTimeList[0] += 1
        else: y += 10
    
    # Checks if player fell to death
    '''if player.rect.bottom >= 400:
       player.respawn([0,0])'''
    
    #format list for player collision
    collidables = [allPlatForms[i] for i in range(0,len(allPlatForms))]
    for i in range(0,len(ground)):
        collidables.append(ground[i])
    for i in range(0,len(wall)):
        collidables.append(wall[i])
    
    player.move(collidables,x,y)
    #lantern.move()
    
    # Moves platforms
    for i in range(0, len(platformCoords)):
        platformCoords[i][0] -= MOVE_RATE
        allPlatForms[i].move(MOVE_RATE,0)

    # Check if we should make a new platform with brain if so make one
    if brain.shouldPlatformBeCreated(platformCoords):
        # Here we get the new positions for the platform
        lastPlatform = platformCoords[len(platformCoords) - 1]
        positions = brain.getNewPlatformPosition(lastPlatform)
        # We add the new platform to the coordinates and platformClass
        platformCoords.append(positions)
        allPlatForms.append(new_classes.Platform(win, positions, 50))

        index = len(platformCoords) - 1
        # Here we add them to the sprite
        allSprites.add(allPlatForms[index])
        platforms.add(allPlatForms[index])

    #draw stuffs
    for entity in allSprites:
        entity.render()
    
    #update screen
    pg.display.flip()
    clock.tick(60)

pg.quit()
