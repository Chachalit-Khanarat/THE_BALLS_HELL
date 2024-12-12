import turtle
import ball
import random
import math
import time
import paddle
import threading

class balldb():
    def __init__(self):
        self.ball = []
        self.border = border()

    def create(self, ball_num):
        b = border()
        for i in range(ball_num):
            # size = random.uniform(0.01, 0.1) * b.canvas_width
            size = 0.05 * b.canvas_width
            x = random.randrange(-250,300,50)
            y = int(b.canvas_height - size - 20)
            vx = 0
            vy = (5*random.uniform(-1.0, 0.1))
            ball_color = ((255,0,0))
            mass =  (4/3) * math.pi * (size**3) * 2
            tball = ball.ball(x=x, y=y, vx=vx, vy=vy, size=size, color=ball_color, mass=mass,team="r")
            self.ball.append(tball)

class border():
    def __init__(self):
        self.canvas_width = turtle.screensize()[1]
        self.canvas_height = turtle.screensize()[0]

    def draw_border(self):
        turtle.penup()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(10)
        turtle.pendown()
        turtle.setheading(0)
        turtle.color((0, 0, 0))
        for i in range(2):
            turtle.forward(2*self.canvas_width)
            turtle.left(90)
            turtle.forward(2*self.canvas_height)
            turtle.left(90)

    def draw_line(self):
        turtle.pensize(2)
        turtle.penup()
        turtle.color((255,100,100))
        for i in range(-self.canvas_width+50,self.canvas_width,50):
            turtle.goto(i,-self.canvas_height)
            turtle.pendown()
            turtle.setheading(90)
            turtle.forward(2*self.canvas_height)
            turtle.penup()


class run():
    def __init__(self, num_ball):
        turtle.speed(0)
        turtle.tracer(0)
        turtle.hideturtle()
        turtle.colormode(255)
        self.num = num_ball
        self.ballset =  balldb()
        self.ballset.create(self.num)
        self.dt = 0.5
        self.border = border()
        self.frame = 0
        Jimmy = turtle.Turtle()
        Kendo = turtle.Turtle()
        self.my_paddle = paddle.Paddle(50, 50, (0,200,255), Jimmy, "b")
        self.my_paddle.set_location([0, -350])
        self.en_paddle = paddle.Paddle(50, 50, (255,100,0), Kendo, "r", head=-90)
        self.en_paddle.set_location([0, 350])
        self.screen = turtle.Screen()
        self.plist = [self.my_paddle,self.en_paddle]

    def draw(self):
        for i in self.ballset.ball:
            i.draw_ball() 
            i.wall_hit(self.border.canvas_width,self.border.canvas_height)
            i.move_ball(self.dt)
            if i.bhp <= 0:
                self.ballset.ball.pop(self.ballset.ball.index(i))
    
    def draw_paddle(self):
        for i in self.plist:
            if i.bhp > 0:
                i.draw()

    def ball_ball_hit(self):
        for i in self.ballset.ball:
            for j in self.ballset.ball:
                if i == j:
                    continue
                if i.ball_hit(j):
                    if j.bhp - i.bhp <= 0 and i.bhp - j.bhp <= 0:
                        self.ballset.ball.pop(self.ballset.ball.index(i))
                        self.ballset.ball.pop(self.ballset.ball.index(j))
                    elif i.bhp - j.bhp <= 0:
                        self.ballset.ball.pop(self.ballset.ball.index(i))
                        j.bhp -= i.bhp
                    elif j.bhp - i.bhp <= 0:
                        self.ballset.ball.pop(self.ballset.ball.index(j))
                        i.bhp -= j.bhp
                    break

    def ball_paddle_hit(self):
        for i in self.ballset.ball:
            if i.paddle_hit(self.my_paddle):
                self.ballset.ball.pop(self.ballset.ball.index(i))
                self.my_paddle.bhp -= i.bhp
            elif i.paddle_hit(self.en_paddle):
                self.ballset.ball.pop(self.ballset.ball.index(i))
                self.en_paddle.bhp -= i.bhp

        if self.my_paddle.bhp <= 0:
            return self.en_paddle
        if self.en_paddle.bhp <= 0:
            return self.my_paddle
        
        return None

    # move_left and move_right handlers update paddle positions
    def move_left(self,pad):
        if (pad.location[0] - pad.width/2 - 50) >= -self.border.canvas_width:
            pad.set_location([pad.location[0] - 50, pad.location[1]])

    # move_left and move_right handlers update paddle positions
    def move_right(self,pad):
        if (pad.location[0] + pad.width/2 + 50) <= self.border.canvas_width:
            pad.set_location([pad.location[0] + 50, pad.location[1]])

    def fire(self,pad,di,team,colour):
        mass =(4/3) * math.pi * (5**3) * 2
        b = ball.ball(size=5, x=pad.location[0], y=pad.location[1], vx=0, vy=di*20, color=colour, mass=mass, team=team,bhp = 1)
        b.wt = 2
        self.ballset.ball.append(b)

    def fire2(self,pad,di,team,colour):
        mass =(4/3) * math.pi * (5**3) * 2
        b = ball.ball(size=10, x=pad.location[0], y=pad.location[1], vx=0, vy=di*20, color=colour, mass=mass, team=team,bhp=2)
        b.wt = 2
        self.ballset.ball.append(b)
            
    def run(self):
        turtle.clear()
        self.my_paddle.clear()
        self.en_paddle.clear()
        self.border.draw_line()
        self.border.draw_border()
        self.draw()
        self.draw_paddle()
        self.ball_ball_hit()
        turtle.update()
    
    def run_fps_cap(self):
        self.screen.listen()
        self.screen.onkey(lambda : self.move_left(self.my_paddle), "a")
        self.screen.onkey(lambda :self.move_right(self.my_paddle), "d")
        self.screen.onkey(lambda :self.fire(self.my_paddle,1,"b",(0,255,200)), "s")
        self.screen.onkey(lambda :self.fire2(self.my_paddle,1,"b",(0,255,200)), "w")
        self.screen.onkey(lambda :self.move_left(self.en_paddle), "Left")
        self.screen.onkey(lambda :self.move_right(self.en_paddle), "Right")
        self.screen.onkey(lambda :self.fire(self.en_paddle,-1,"r",(255,20,20)), "Down")
        self.screen.onkey(lambda :self.fire2(self.en_paddle,-1,"r",(255,20,20)), "Up")
        start1 = time.time()
        start2 = time.time()
        print(self.border.canvas_height, self.border.canvas_width)
        while True:
            end = time.time()
            try:
                if abs(start1 - end) >= 1/120:
                    self.run()
                    t = self.ball_paddle_hit()
                    if t:
                        break
                    self.frame += 1
                    if abs(start2 - end) >= 1:
                        print(self.frame)
                        self.frame = 0
                        start2 = time.time()
                    start1 = time.time()
            except TypeError:
                print("error")
        print(t)
        turtle.done()


# num_balls = int(input("Number of balls to simulate: "))
num_balls = 0
st = run(num_balls)
st.run_fps_cap()

# hold the window; close it by clicking the window close 'x' mark

