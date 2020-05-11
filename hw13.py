import tkinter as tk
import random
def rand_color():
    return random.choice(["orange", "yellow",
                          "green", "blue", "purple"])

#==========================================
# Purpose: main class contain gameloop
# Instance variables: there is none
# Methods: __init__ creat board for the game
#init create all thing that needs to be restart.
#gameloop keep the game runing until it satisfie some condition
#gameloopclean clean game loop
#restart restart the game whrn r is pressed
#==========================================

class SnakeGUI():
    def __init__(self):
        self.win = tk.Tk()
        self.canvas = tk.Canvas(width = 660,height = 660)
        self.canvas.pack()
        self.board = self.canvas.create_rectangle(30, 30, 630, 630)
        self.init()
    def init(self):

        self.snake = Snake(330,330,rand_color(),self.canvas)
        self.ESnake = ENESnake(210,210,'black',self.canvas)
        self.food = Food(self.canvas)
        self.win.bind('<Down>',self.snake.go_down)
        self.win.bind('<Up>',self.snake.go_up)
        self.win.bind('<Right>',self.snake.go_right)
        self.win.bind('<Left>',self.snake.go_left)
        self.win.bind('r',self.restart)
        self.ESnake.move(self.food.x,self.food.y)
        self.gameloop()
        self.canvas.mainloop()
    def gameloop(self):
        self.S = self.snake.move(self.food.x,self.food.y)
        self.E = self.ESnake.move(self.food.x,self.food.y)
        snakelocation = self.snake.get_location()
        esnakelocation = self.ESnake.get_location()
        check = ''
        for i in snakelocation:
            for j in esnakelocation:
                if self.canvas.coords(i) == self.canvas.coords(j):
                    check = 'hit'

        if self.S == True or self.E == True:
            self.food.eaten()
            
        if self.S== 'hit' or self.E == 'hit' or check == 'hit':
            #print('hit')
            self.snake.GameOver()

            
            
        else:
            self.canvas.after(100, self.gameloop)

         
    def gameloopclean(self):
        self.canvas.delete(self.S)
        self.canvas.delete(self.E)

        

    def restart(self,event):
        #print('hi')
        self.snake.clean()
        self.ESnake.clean()
        self.food.clean()
        self.gameloopclean()
        self.init() 
        
#==========================================
# Purpose: create a snake that follows plsyers move
# Instance variables: startingx starting x position   startingY starting y position color- color of snake canvas
# Methods: __set velocity to x, create one rec
#move monitar player's keyboard and move, check if it eat a food or fit run in to ieself
#get_location getsnake's head location 
#go_left vreast a rec at the left side when > is presses. so is go_down,go_up and go_right
#GameOver pause the game create a text indates player's score
# clean clean everthing that has been drawn by this function 
#==========================================

class Snake:
    def __init__(self,startingX,startingY,color,canvas):
        self.x = startingX
        self.y = startingY
        self.color = color
        self.canvas = canvas
        self.vx = 0
        self.vy = 0
        self.segments = []
        self.snake = self.canvas.create_rectangle(self.x, self.y, int(self.x+30), int(self.y-30),fill = self.color)
        self.segments.insert(0,self.snake)

    def move(self,x_location,y_location):
        self.x = int(self.x+self.vx)
        self.y = int(self.y+self.vy)

        
        self.snake = self.canvas.create_rectangle(self.x, self.y, int(self.x+30), int(self.y-30),fill = self.color)
        x0, y0, x1, y1 = self.canvas.bbox(self.snake)
        if x0 <0 or x0>599 or y0<0 or y0 >601:
            return 'hit'
        else:
            self.segments.insert(0,self.snake)
        
        #print(x0,y0,x1,y1)
        if len(self.segments) >2:
            for i in range(1,len(self.segments)):
                if self.canvas.coords(self.segments[0]) == self.canvas.coords(self.segments[i]):
                    return 'hit'

            

        if x_location != self.x or y_location !=self.y:

            last_deleted = self.segments.pop(-1)
            self.canvas.delete(last_deleted)
            
        else:
            return True
    def get_location(self):
        return self.segments

    def go_down(self,event):
        self.vx = 0
        self.vy = 30
    def go_up(self,event):
        self.vx = 0
        self.vy = -30
    def go_right(self,event):
        self.vx = 30
        self.vy = 0
    def go_left(self,event):
        self.vx = -30
        self.vy = 0
    def GameOver(self):
        score = len(self.segments)
        TT = 'Game Over! Your score was: ' +str(score)
        self.tex = self.canvas.create_text(200,200, text=TT)
    def clean(self):
        for i in self.segments:
            self.canvas.delete(i)
        try:
            self.canvas.delete(self.snake)
            
        except:
            pass
        try:
            self.canvas.delete(self.tex)
        except:
            pass

        self.segments.clear()

        
    

        






#================part1==============
#==========================================
# Purpose: remdonly draw food on the screen and redraw if its eaten
# Instance variables: canvas draw
# Methods: __init__ generate a red oval on the screen with remdon location 
#eaten createa  new food when the old one is eaten 
#clean clean all the food 
#==========================================

class Food():
    def __init__(self,canvas):
        self.x = int(30*random.randint(2,20))
        self.y = int(30*random.randint(2,20))
        self.canvas = canvas
        self.foods = []
        self.color = 'Red'
        self.circle = self.canvas.create_oval(self.x,self.y,int(self.x+30),int(self.y-30),fill = self.color)
        self.foods.insert(0,self.circle)
    def eaten(self):
        self.x = int(30*random.randint(2,20))
        self.y = int(30*random.randint(2,20))
        self.circle = self.canvas.create_oval(self.x,self.y,int(self.x+30),int(self.y-30),fill = self.color)
        self.foods.insert(0,self.circle)
        last_deleted = self.foods.pop(-1)
        self.canvas.delete(last_deleted)
    def clean(self):
        for i in self.foods:
            self.canvas.delete(i)
        self.foods.clear()



#==========================================
# Purpose: create an AI enemy snake
# Instance variables:startingx starting x position   startingY starting y position color- color of snake canvas
# Methods:  __init__ set velocity to 30 and draw a rec at set location 
#move always move towards food at 30 pixle speed
#get_location retrun the location of the snake's head
#clean clean everything that's create by this funtion. 
#==========================================


class ENESnake:
    def __init__(self,startingX,startingY,color,canvas):
        self.x = startingX
        self.y = startingY
        self.color = color
        self.canvas = canvas
        self.vx = 30
        self.vy = 30
        self.segments = []
        self.Esnake = self.canvas.create_rectangle(self.x, self.y, int(self.x+30), int(self.y-30),fill = self.color)
        self.segments.insert(0,self.Esnake)

    def move(self,x_location,y_location):


        if self.x < x_location:

            self.x = int(self.x+self.vx)
        elif self.x >x_location:
            self.x = int(self.x-self.vx)
        elif self.y < y_location:

            self.y = int(self.y+self.vy)
        elif self.y > y_location:
            self.y = int(self.y-self.vy)

        

        self.Esnake = self.canvas.create_rectangle(self.x, self.y, int(self.x+30), int(self.y-30),fill = self.color)
        self.segments.insert(0,self.Esnake)
        #print(x0,y0,x1,y1)
##        if len(self.segments) >2:
##            for i in range(1,len(self.segments)):
##                if self.canvas.coords(self.segments[0]) == self.canvas.coords(self.segments[i]):
##                    return 'hit'
##                else:
##                    pass
        if x_location != self.x or y_location !=self.y:

            last_deleted = self.segments.pop(-1)
            self.canvas.delete(last_deleted)        
        else:
            return True
    def get_location(self):
        return self.segments

 

    def clean(self):
        for i in self.segments:
            self.canvas.delete(i)
        try:
            self.canvas.delete(self.tex)
        except:
            pass
        self.segments.clear()










SnakeGUI()





