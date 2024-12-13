import turtle
import ball
import random
import math
import time
import paddle
import threading
import socket

class balldb():
    def __init__(self):
        self.ball = []
        self.border = border()

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
        self.host = "127.0.0.1"
        self.port = 25555
        self.addr = "127.0.0.1"

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

    def connecting(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.s.bind((self.host, self.port))
        except OSError:
            print("Only one usage of each socket address (protocol/network address/port) is normally permitted")

    def desition(self,data):
        if data == "d":
            self.move_left(self.en_paddle)
        elif data == "a":
            self.move_right(self.en_paddle)
        elif data == "s":
            self.fire(self.en_paddle,-1,"r",(255,20,20))
        elif data == "w":
            self.fire2(self.en_paddle,-1,"r",(255,20,20))
        self.data = 0

    def recv(self):
        try:
            self.data, addr = self.s.recvfrom(1024)
            print(addr, self.addr)
            if addr != self.addr:
                return
        except BlockingIOError:
            self.data = 0
            return
        self.data = self.data.decode('utf-8')
        print("From connected user: " + self.data)
        self.desition(self.data)

    def turtle_key_my(self):
            self.screen.listen()
            self.screen.onkey(lambda : self.move_left(self.my_paddle), "a")
            self.screen.onkey(lambda :self.move_right(self.my_paddle), "d")
            self.screen.onkey(lambda :self.fire(self.my_paddle,1,"b",(0,255,200)), "s")
            self.screen.onkey(lambda :self.fire2(self.my_paddle,1,"b",(0,255,200)), "w")
            self.screen.onkey(self.recv, " ")
    
    def turtle_key_en(self):
            self.screen.onkey(lambda :self.move_left(self.en_paddle), "Left")
            self.screen.onkey(lambda :self.move_right(self.en_paddle), "Right")
            self.screen.onkey(lambda :self.fire(self.en_paddle,-1,"r",(255,20,20)), "Down")
            self.screen.onkey(lambda :self.fire2(self.en_paddle,-1,"r",(255,20,20)), "Up")


    # move_left and move_right handlers update paddle positions
    def move_left(self,pad):
        if (pad.location[0] - pad.width/2 - 50) >= -self.border.canvas_width:
            pad.set_location([pad.location[0] - 50, pad.location[1]])
        self.s.sendto("a".encode("utf-8"), self.addr)

    # move_left and move_right handlers update paddle positions
    def move_right(self,pad):
        if (pad.location[0] + pad.width/2 + 50) <= self.border.canvas_width:
            pad.set_location([pad.location[0] + 50, pad.location[1]])
            self.s.sendto("d".encode("utf-8"), self.addr)

    def fire(self,pad,di,team,colour):
        mass =(4/3) * math.pi * (5**3) * 2
        b = ball.ball(size=5, x=pad.location[0], y=pad.location[1], vx=0, vy=di*20, color=colour, mass=mass, team=team,bhp = 1)
        b.wt = 2
        self.ballset.ball.append(b)
        self.s.sendto("s".encode("utf-8"), self.addr)

    def fire2(self,pad,di,team,colour):
        mass =(4/3) * math.pi * (5**3) * 2
        b = ball.ball(size=10, x=pad.location[0], y=pad.location[1], vx=0, vy=di*20, color=colour, mass=mass, team=team,bhp=2)
        b.wt = 2
        self.ballset.ball.append(b)
        self.s.sendto("w".encode("utf-8"), self.addr)
            
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

    def wait_player(self):
        turtle.write(f"waiting for player",font=("Arial", 100, "normal"),align="center")
        data, self.addr = self.s.recvfrom(1024)
        self.s.setblocking(False)
    
    def run_fps_cap(self):
        self.turtle_key_my()
        start1 = time.time()
        start2 = time.time()
        print(self.border.canvas_height, self.border.canvas_width)
        self.s.setblocking(False)
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
            self.recv()
        turtle.clear()
        self.my_paddle.clear()
        self.en_paddle.clear()
        turtle.goto(0,-150)
        turtle.write(f"{t} ! WIN !",font=("Arial", 100, "normal"),align="center")
        turtle.done()
        c.close()

# num_balls = int(input("Number of balls to simulate: "))
num_balls = 0
st = run(num_balls)
q1 = input("host press 1, join press 2, local press 3 :")
if q1 == "1":
    # st.host = input("your ipv6: ")
    # st.port = int(input("port : "))
    st.host = "192.168.1.101"
    st.port = 25555
    st.connecting()
    st.wait_player()

elif q1 == "2":
    st.host = "192.168.1.106"
    st.port = 25555
    st.addr = ('hongrocker49.thddns.net', 2720) #input("server ip : "), int(input("server port : "))
    st.connecting()
    print(st.addr)
    st.s.sendto("connected".encode("utf-8"),st.addr)

st.run_fps_cap()


