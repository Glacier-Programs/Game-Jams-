import pygame as pg
import story

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

win = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pg.display.set_caption('Lights Out')

#fonts
fonts = {'buttons':pg.font.SysFont('dejavuserif',40),'title':pg.font.SysFont('lato',60),'header':pg.font.SysFont('lato',30),'text':pg.font.SysFont('dejavuserif',20)}

#clock
clock = pg.time.Clock()

#music
pg.mixer.music.load('sfx/mus.wav')
pg.mixer.music.play(-1)


class Button:
    def __init__(self,surf,text,coords,width,height,colour=(0,0,0),bg=(122,122,122)):
        self.surf = surf
        self.text = text
        self.coords = coords
        self.width = width
        self.height = height
        self.colour = colour
        self.bg = bg
        if bg != None: self.textSurf = fonts['buttons'].render(text,False,colour,bg)
        else: self.textSurf = fonts['buttons'].render(text,False,colour)
    def in_bounds(self,coords):
        xCase = self.coords[0] < coords[0] and self.coords[0] + self.width > coords[0]
        yCase = self.coords[1] < coords[1] and self.coords[1] + self.height > coords[1]
        if xCase and yCase:
            return True
        else:
            return False
    def render(self):
        self.surf.blit(self.textSurf,self.coords)
    def add_function(self,func):
        self.func = func

class CircleBtn(Button):
    def __init__(self,surf,text,coords,width,height,colour=(0,0,0),bg=(122,122,122)):
        self.drawTo = surf
        self.container = pg.surface.Surface((width,height))
        self.container.fill((122,122,122))
        super().__init__(self.container,text,coords,width,height,colour,bg)
        self.rect = self.textSurf.get_rect()
        self.circle = pg.draw.ellipse(self.container,bg,self.rect)
        self.container.blit(self.textSurf,self.rect)
    def render(self):
        self.drawTo.blit(self.container,self.coords)

class Text:
    def __init__(self,surf,Type,text,coords,width,height,colour=(0,0,0),bg=False):
        self.surf = surf
        self.text= text
        self.Type = Type
        self.coords = coords
        self.width = width
        self.height = height
        self.colour = colour
        self.bg = bg
        if bg: self.textSurf = fonts[Type].render(text,False,colour,bg)
        else: self.textSurf = fonts[Type].render(text,False,colour)
    def render(self):
        self.surf.blit(self.textSurf,self.coords)

def start():
    global done
    def Start():
        level_select()
    def openCredits():
        Credits()
        
    #text
    top = Text(win,'title','Lights Out',[75,20],150,40)
    Texts = [top]
    
    #buttons
    start = Button(win,'Start',[150,100],150,40)
    start.add_function(Start)
    creditsBtn = Button(win,'Credits',[125,150],200,40)
    creditsBtn.add_function(openCredits)
    buttons = [start,creditsBtn]
    
    done = False
    while not done:
        win.fill((255,255,255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pg.quit()
                quit()
        
        #mousy mouse
        mouse = pg.mouse
        if mouse.get_pressed()[0]:
            pos = mouse.get_pos()
            print(pos)
            for button in buttons:
                if button.in_bounds(pos):
                    print('clicked')
                    button.func()
        
        #render buttons
        for button in buttons:
            button.render()
        
        #render text
        for text in Texts:
            text.render()

        pg.display.update()
        pg.time.Clock().tick(60)

def Credits():
    def Return():
        global Done
        Done = True
    global Done
    #make text
    title = Text(win,'title','Credits',[100,20],200,60)
    programHeader = Text(win,'header','Programming',[120,100],100,50)
    programText = Text(win,'text','Adam Kollgard - Jared Dewey',[50,150],100,20)
    musicHeader = Text(win,'header','Music',[160,180],50,50)
    musicText = Text(win,'text','Travis Hahn',[140,220],100,20)
    artHeader = Text(win,'header','Art',[180,240],25,50)
    artText = Text(win,'text','Jared Dewey',[140,280],50,20)
    texts = [title,programHeader,programText,musicHeader,musicText,artHeader,artText]
    #make buttons
    returnBtn = Button(win,'Return',[125,350],200,40,bg=None)
    returnBtn.add_function(Return)
    buttons = [returnBtn]
    Done = False
    while not Done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Done = True
                pg.quit()
                quit()
                return True
        mouse = pg.mouse
        if mouse.get_pressed()[0]:
            pos = mouse.get_pos()
            for button in buttons:
                if button.in_bounds(pos):
                    button.func()
        #render
        win.fill((100,100,100))
        for button in buttons:
            button.render()
        for text in texts:
            text.render()
        pg.display.update()
        pg.time.Clock().tick(60)

def level_select():
    #buttons
    l1 = CircleBtn(win,'D-1',[50,50],80,50)
    l1.add_function(lambda: story.story(win,'lvls/lvl1'))
    l2 = CircleBtn(win,'D-2',[130,50],80,50)
    l2.add_function(lambda: story.story(win,'lvls/lvl2'))
    l3 = CircleBtn(win,'D-3',[210,50],80,50)
    l3.add_function(lambda: story.story(win,'lvls/lvl3'))
    l4 = CircleBtn(win,'D-4',[290,50],80,50)
    l4.add_function(lambda: story.story(win,'lvls/lvl4'))
    buttons = [l1,l2,l3,l4]
    Done = False
    while not Done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                done = True
                quit()
        #mousy mouse
        mouse = pg.mouse
        if mouse.get_pressed()[0]:
            for button in buttons:
                if button.in_bounds(mouse.get_pos()):
                    button.func()
        #render
        win.fill((255,255,255))
        for button in buttons:
            button.render()
        pg.display.flip()
        pg.time.Clock().tick(60)

if __name__ == '__main__':
    start()
