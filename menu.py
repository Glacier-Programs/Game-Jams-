import pygame as pg
import story

fonts = None
done = False
returnMe = None 
def init(Fonts):
    global fonts
    fonts = Fonts

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

def start(win):
    global done
    def Start():
        #level_select(win)
        story.story(win)
    def openCredits():
        Credits(win)
        
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
                return True
        
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

def Credits(win):
    def Return():
        global Done
        Done = False
    #make text
    title = Text(win,'title','Credits',[100,20],200,60)
    programHeader = Text(win,'header','Programing',[100,100],100,50)
    programText = Text(win,'text','Adam Kollgard - Jared Dewey',[50,160],100,20)
    musicHeader = Text(win,'header','Music',[150,190],50,50)
    musicText = Text(win,'text','Travis Hahn',[100,260],100,20)
    texts = [title,programHeader,programText,musicHeader,musicText]
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

def level_select(win):
    #buttons
    buttons = [CircleBtn(win,'D-1',[100,100],80,50)]
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
            pass
        #render
        win.fill((0,0,0))
        for button in buttons:
            button.render()
        pg.display.flip()
        pg.time.Clock().tick(60)
