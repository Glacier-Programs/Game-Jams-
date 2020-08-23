from readLevel import read_level
import pygame as pg
import new_classes

#game loop
def story(win):
    player = new_classes.Player([100,100],20,40)
    jump_height = 10
    jump_max = 100
    jump_height = 0
    airTimeList = [0,20] # current , max
    
    lantern = new_classes.Lantern(win, player, player.coords)
    player.set_surf(win)
    
    level = read_level('lvl2',win)
    # Collidables are platforms, walls, ground, etc.
    collidables = []
    # Interacts are doors, etc
    interact = []
    for part in level:
        if part.sub == 'platform':
            collidables.append(part)
        else:
            interact.append(part)
        
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pg.quit()
                quit()
        dx,dy = 0,0
        #keys
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            dx -= 10
        elif keys[pg.K_d]:
            dx += 10
        if keys[pg.K_SPACE] and (not player.jumping and player.touchingGround or player.touchingWall):
            player.jumping = True
        if keys[pg.K_w]:
            for obj in interact:
                xCase = obj.lCoords[0] < player.coords[0]+player.width and obj.lCoords[0]+obj.width > player.coords[0]
                yCase = obj.lCoords[1] < player.coords[1]+player.height and obj.lCoords[1]+obj.height > player.coords[1]
                #print(xCase,yCase)
                if xCase and yCase:
                    print('opened')
                    if obj.sub == 'door':
                        done = True
        if keys[pg.K_r]:
            # Latern goes into tracking mode 
            lantern.mode = 0
            lantern.trackingCoords = player.coords
            pass
        #unpressed
        
        #mousy mouse
        mouse = pg.mouse
        if mouse.get_pressed()[0]:
            pos = mouse.get_pos()
            if not lantern.mode:
                # Latern goes in Stay Mode
                lantern.mode = 1
                lantern.trackingCoords = pos
                pass
        
        #jumping
        if player.jumping:
            if jump_height >= jump_max:
                player.jumping = False
                jump_height = 0
            else:
                dy -= 10
                jump_height += 10
        
        #coyote / airtime
        if not player.touchingGround and not player.jumping:
            if airTimeList[0] <= airTimeList[1]:
                airTimeList[0] += 1
            else: dy += 5
        
        player.move(collidables,dx,dy)
        lantern.move()

        #blank out screen
        win.fill((0,0,0))
        
        #render
        for sprite in level:
            sprite.render()
        player.render()
        lantern.render()
        
        #update screen
        pg.display.update()
        pg.time.Clock().tick(60)

if __name__ == '__main__':
    win = pg.display.set_mode((400,400))
    story(win)
    pg.quit()
