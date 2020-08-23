import pygame as pg
import new_classes
pg.init()

def read_level(file,surf):
    file = open(file,'r')
    file = file.read().split('\n')
    area = file[0]
    print(file)
    returnMe = []
    for obj in file:
        objType = obj.split('(')
        if len(objType) > 1:
            beta_coords = objType[1].split(')')
            alpha_coords = beta_coords[0].split(',')
            coords = [int(alpha_coords[0])*50,int(alpha_coords[1])*50]
            objType = objType[0]
        
            if objType == 'ground':
                returnMe.append(new_classes.Ground(surf,area,coords,50))
            elif objType == 'wall':
                returnMe.append(new_classes.Wall(surf,area,coords,50))
            elif objType == 'platform':
                returnMe.append(new_classes.StatPlat(surf,[coords[0],coords[1]],50,'imgs/platform.png'))
            elif objType == 'end':
                returnMe.append(new_classes.Door(surf,[coords[0],coords[1]+10]))
    return returnMe

if __name__ == '__main__':
    win = pg.display.set_mode((400,400))
    level = read_level('lvl1',win)
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
        for part in level:
            part.render()
        pg.display.flip()
    pg.quit()