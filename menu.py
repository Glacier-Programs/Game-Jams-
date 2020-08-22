import pygame as pg

fonts = None
done = False
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
        self.textSurf = fonts['buttons'].render(text,False,colour,bg)
    def in_bounds(self,coords):
        xCase = self.coords[0] < coords[0] and self.coords[0] + self.width > coords[0]
        yCase = self.coords[1] < coords[1] and self.coords[1] + self.height > coords[1]
        if xCase and yCase:
            return True
    def render(self):
        self.surf.blit(self.textSurf,self.coords)
    def add_function(self,func):
        self.func = func

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
        global done
        done = True
    
    #text
    top = Text(win,'title','Lights Out',[75,20],150,40)
    Texts = [top]
    
    #buttons
    start = Button(win,'Start',[150,100],150,40)
    start.add_function(Start)
    buttons = [start]
    
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
    #make text
    texts = []
    #make buttons
    buttons = []
    global done
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                return True
        mouse = pg.mouse
        if mouse.get_pressed()[0]:
            for button in buttons:
                if button.in_bounds():
                    button.func()
        #render
        win.fill((100,100,100))
        for button in buttons:
            button.render()
        for text in texts:
            text.render()
        pg.time.Clock().tick(60)