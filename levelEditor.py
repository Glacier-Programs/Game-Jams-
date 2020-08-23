import tkinter as tk

win = tk.Tk()
win.geometry('500x500')

guideLines = []

matrix = []
selected = 'floor'
theme = 'dungeon'

matrix2obj = {'g':'ground','w':'wall','s':'start','e':'end','u':'power','f':'fall','p':'platform'}

def set_matrix():
    global matrix
    for i in range(0,8):
        alist = []
        for i in range(0,8):
            alist.append(None)
        matrix.append(alist)

def show_blocks():
    global guideLines
    can.delete(guideLines)
    guideLines = []
    for i in range(0,7):
        guideLines.append(can.create_line(0,50+i*50,400,50+i*50,fill='black'))
        guideLines.append(can.create_line(50+i*50,0,50+i*50,400,fill='black'))

def set_theme():
    global theme
    if theme == 'dungeon':
        theme = 'hall'
    elif theme == 'hall':
        theme = 'spire'
    elif theme == 'spire':
        theme = 'outside'
    else:
        theme = 'dungeon'
    themeBtn.configure(text='Theme: ' + theme)

def set_eraser():
    global selected
    selected = 'eraser'

def floor():
    global selected
    selected = 'floor'
    
def wall():
    global selected
    selected = 'wall'

def start():
    global selected
    selected = 'start'

def end():
    global selected
    selected = 'end'

def power():
    global selected
    selected = 'power'

def fall():
    global selected
    selected = 'fall'

def plat():
    global selected
    selected = 'plat'

def save():
    print('saved')
    file = open(entry.get(),'w+')
    file.write(theme+'\n')
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix[i])):
            if matrix[i][j]:
                string = matrix2obj[matrix[i][j]] + '('
                string += str(i)+','+str(j)+')\n'
                file.write(string)

def onClick(event):
    global matrix
    x,y = event.x, event.y
    spot = [x//50,y//50]
    print(spot)
    if selected == 'eraser':
        matrix[spot[0]][spot[1]] = None
        can.create_rectangle(spot[0]*50,spot[1]*50,spot[0]*50+50,spot[1]*50+50,fill='white')
    elif selected == 'floor':
        matrix[spot[0]][spot[1]] = 'g'
        can.create_rectangle(spot[0]*50,spot[1]*50,spot[0]*50+50,spot[1]*50+50,fill='black')
    elif selected == 'wall':
        matrix[spot[0]][spot[1]] = 'w'
        can.create_rectangle(spot[0]*50,spot[1]*50,spot[0]*50+50,spot[1]*50+50,fill='grey')
    elif selected == 'start':
        matrix[spot[0]][spot[1]] = 's'
        can.create_rectangle(spot[0]*50,spot[1]*50,spot[0]*50+50,spot[1]*50+50,fill='red')
    elif selected == 'end':
        matrix[spot[0]][spot[1]] = 'e'
        can.create_rectangle(spot[0]*50,spot[1]*50,spot[0]*50+50,spot[1]*50+50,fill='brown')
    elif selected == 'power':
        matrix[spot[0]][spot[1]] = 'u'
        can.create_rectangle(spot[0]*50,spot[1]*50,spot[0]*50+50,spot[1]*50+50,fill='blue')
    elif selected == 'fall':
        matrix[spot[0]][spot[1]] = 'f'
        can.create_rectangle(spot[0]*50,spot[1]*50,spot[0]*50+50,spot[1]*50+50,fill='purple')
    elif selected == 'plat':
        matrix[spot[0]][spot[1]] = 'p'
        can.create_rectangle(spot[0]*50,spot[1]*50,spot[0]*50+50,spot[1]*50+50,fill='green')

leftbar = tk.Frame(win)
themeBtn = tk.Button(leftbar,text='Theme: Dungeon',command=set_theme)
themeBtn.pack(side=tk.TOP)
tk.Button(leftbar,text='Eraser',command=set_eraser).pack(side=tk.TOP)
tk.Button(leftbar,text='Floor',command=floor).pack(side=tk.TOP)
tk.Button(leftbar,text='Wall',command=wall).pack(side=tk.TOP)
tk.Button(leftbar,text='Platform',command=plat).pack(side=tk.TOP)
tk.Button(leftbar,text='start',command=start).pack(side=tk.TOP)
tk.Button(leftbar,text='end',command=end).pack(side=tk.TOP)
tk.Button(leftbar,text='power up',command=power).pack(side=tk.TOP)
tk.Button(leftbar,text='fall',command=fall).pack(side=tk.TOP)
entry = tk.Entry(leftbar)
entry.pack(side=tk.TOP)
tk.Button(leftbar,text='save',command=save).pack(side=tk.TOP)
leftbar.pack(side=tk.LEFT)

can = tk.Canvas(win,width=400,height=400,bg='white')
can.pack()
can.bind('<Button-1>',onClick)

set_matrix()
show_blocks()

win.mainloop()