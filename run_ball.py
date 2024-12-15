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
    def __init__(self):
        turtle.speed(0)
        turtle.tracer(0)
        turtle.hideturtle()
        turtle.colormode(255)
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
        self.mode_selecter()

    def mode_selecter(self):
        q1 = turtle.textinput(title="THE BALL HELL",prompt="host press 1, join press 2, local press 3 : ")
        match q1:
            case "1":
                self.host = turtle.textinput(title="HOST",prompt="IP")
                self.port = turtle.textinput(title="HOST",prompt="PORT")
                self.host = "192.168.1.101"
                self.port = 25555
                self.connecting()
                self.wait_player()
                self.type_selecter()
                self.wait_player()
                self.turtle_key_my()
            case "2":
                self.host = "192.168.1.101" # Put your ipv4 by check it in cmd and type ipconfig
                self.port = 25555
                self.addr = turtle.textinput(title="JOIN",prompt="Host IP"),turtle.textinput(title="JOIN",prompt="HOST PORT")
                self.addr = ('hongrocker49.thddns.net', 2720)
                self.connecting()
                print(self.addr)
                self.s.sendto("connected".encode("utf-8"),self.addr)
                self.wait_player()
                self.type_selecter()
                self.turtle_key_my()
            case "3":
                p1 = turtle.textinput(title="CHARACTER SELECTION P1",prompt="n or s :")
                p2 = turtle.textinput(title="CHARACTER SELECTION P2",prompt="n or s :")
                self.my_paddle.type = p1
                self.en_paddle.type = p2
                self.turtle_key_my()
                self.turtle_key_en()
        self.my_paddle.correct_type_stat()
        self.en_paddle.correct_type_stat()

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
            print("Only one usage of each socket address",
                  "protocol/network address/port) is normally permitted")

    def desition(self,data):
        if data == "d":
            self.move_left(self.en_paddle)
        elif data == "a":
            self.move_right(self.en_paddle)
        elif data == "s":
            self.fire(self.en_paddle,-1)
        elif data == "w":
            self.fire2(self.en_paddle,-1)
        self.data = 0

    def recv(self):
        try:
            self.data, self.addr = self.s.recvfrom(1024)
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
        self.screen.onkey(lambda :self.fire(self.my_paddle,1), "s")
        self.screen.onkey(lambda :self.fire2(self.my_paddle,1), "w")

    def turtle_key_en(self):
        self.screen.listen()
        self.screen.onkey(lambda :self.move_left(self.en_paddle), "Left")
        self.screen.onkey(lambda :self.move_right(self.en_paddle), "Right")
        self.screen.onkey(lambda :self.fire(self.en_paddle,-1), "Down")
        self.screen.onkey(lambda :self.fire2(self.en_paddle,-1), "Up")

    def drawui(self):
        enl = [-250,420]
        myl = [-250,-450]
        turtle.color((0,0,0))
        turtle.penup()
        turtle.goto(enl)
        turtle.pendown()
        turtle.write(f"HP : {self.en_paddle.bhp}",font=("Arial", 20, "normal"),align="center")
        turtle.penup()
        turtle.goto(myl)
        turtle.pendown()
        turtle.write(f"HP : {self.my_paddle.bhp}",font=("Arial", 20, "normal"),align="center")

    def move_left(self,pad):
        if (pad.location[0] - pad.width/2 - 50) >= -self.border.canvas_width:
            pad.set_location([pad.location[0] - 50, pad.location[1]])
        try:
            if pad.team == "b":
                self.s.sendto("a".encode("utf-8"), self.addr)
        except AttributeError:
            pass

    def move_right(self,pad):
        if (pad.location[0] + pad.width/2 + 50) <= self.border.canvas_width:
            pad.set_location([pad.location[0] + 50, pad.location[1]])
        try:
            if pad.team == "b":
                self.s.sendto("d".encode("utf-8"), self.addr)
        except AttributeError:
            pass

    def fire(self,pad,di):
        b = ball.ball(size=5, x=pad.location[0], y=pad.location[1], \
            vx=0, vy=di*20, color=pad.color, mass=5, team=pad.team,bhp = 5)
        self.ballset.ball.append(b)
        try:
            if pad.team == "b":
                self.s.sendto("s".encode("utf-8"), self.addr)
        except AttributeError:
            pass

    def fire2(self,pad,di):
        now = time.time()
        if now - self.firecooldown <= 5:
            return
        match pad.type:
            case "n":
                b = ball.ball(size=10, x=pad.location[0], y=pad.location[1],\
                    vx=0, vy=di*20, color=pad.color, mass=5, team=pad.team,bhp=10)
                self.ballset.ball.append(b)
                try:
                    if pad.team == "b":
                        self.s.sendto("w".encode("utf-8"), self.addr)
                except AttributeError:
                    pass
                self.firecooldown = time.time()
            case "s":
                for i in range(-2,3):
                    b = ball.ball(size=3, x=pad.location[0], y=pad.location[1],\
                        vx=2*i, vy=di*10, color=pad.color, mass=5, team=pad.team,bhp=2)
                    self.ballset.ball.append(b)
                    try:
                        if pad.team == "b":
                            self.s.sendto("w".encode("utf-8"), self.addr)
                    except AttributeError:
                        pass
                self.firecooldown = time.time()               

    def run(self):
        turtle.clear()
        self.my_paddle.clear()
        self.en_paddle.clear()
        self.border.draw_line()
        self.border.draw_border()
        self.draw()
        self.draw_paddle()
        self.drawui()
        self.ball_ball_hit()
        turtle.update()

    def wait_player(self):
        turtle.write(f"waiting for player",font=("Times New Roman", 100, "normal"),align="center")
        data, self.addr = self.s.recvfrom(1024)
        self.en_paddle.type = data.decode("utf-8")
        print(data)
        turtle.clear()

    def type_selecter(self):
        turtle.write(f"Select your Shape",font=("Times New Roman", 100, "normal"),align="center")
        p1 = turtle.textinput(title="CHARACTER SELECTION P1",prompt="n or s :")
        self.my_paddle.type = p1
        self.s.sendto(p1.encode("utf-8"), self.addr)
        turtle.clear()

    def run_fps_cap(self):
        start1 = time.time()
        start2 = time.time()
        print(self.border.canvas_height, self.border.canvas_width)
        self.firecooldown = time.time()
        try:
            self.s.setblocking(False)
        except AttributeError:
            pass
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
            try:
                self.recv()
            except AttributeError:
                pass
        self.end_screen(t)

    def end_screen(self,t):
        turtle.clear()
        self.my_paddle.clear()
        self.en_paddle.clear()
        turtle.penup()
        turtle.goto(0,-100)
        turtle.color(t.color)
        turtle.pendown()
        if t.team == "b":
            turtle.write(f"YOU ! WIN !",font=("Times New Roman", 100, "normal"),align="center")
        else :
            turtle.write(f"ENEMY ! WIN !",font=("ATimes New Romanrial", 100, "normal"),align="center")
        turtle.done()