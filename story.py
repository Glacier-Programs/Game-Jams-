from readLevel import read_level
import pygame as pg
import new_classes

#game loop
def story(win):
    player = new_classes.Player([100,100],20,40)
    Lantern = new_classes.Lantern(win,player,player.coords)
    player.set_surf(win)
    level = read_level('lvl2',win)
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
        
        player.move(level,dx,dy)
        
        #blank out screen
        win.fill((255,255,255))
        
        #render
        for sprite in level:
            sprite.render()
        player.render()
        
        #update screen
        pg.display.update()
        pg.time.Clock().tick(60)

if __name__ == '__main__':
    win = pg.display.set_mode((400,400))
    story(win)