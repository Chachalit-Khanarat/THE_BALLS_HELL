import turtle
import random
import math
import ball
import time
from numba import cuda, float32

class balldb():
    def __init__(self):
        self.ball = []
        self.border = border()

    def create(self, ball_num):
        b = border()
        for i in range(ball_num):
            size = 0.05 * b.canvas_width
            x = random.randint(int(-1*b.canvas_width + size), int(b.canvas_width - size))
            y = random.randint(int(-1*b.canvas_height + size), int(b.canvas_height - size))
            vx = 2 * random.uniform(-1.0, 1.0)
            vy = 2 * random.uniform(-1.0, 1.0)
            ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            mass = (4/3) * math.pi * (size**3) * 2
            tball = ball.ball(ball_color, size, x, y , vx, vy, mass)
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
        turtle.color((0, 0, 0))
        for i in range(2):
            turtle.forward(2*self.canvas_width)
            turtle.left(90)
            turtle.forward(2*self.canvas_height)
            turtle.left(90)

@cuda.jit
def update_ball_velocity(x, y, vx, vy, dt, canvas_width, canvas_height):
    idx = cuda.grid(1)
    if idx < x.size:
        if x[idx] + vx[idx] * dt > canvas_width or x[idx] + vx[idx] * dt < -canvas_width:
            vx[idx] *= -1
        if y[idx] + vy[idx] * dt > canvas_height or y[idx] + vy[idx] * dt < -canvas_height:
            vy[idx] *= -1
        x[idx] += vx[idx] * dt
        y[idx] += vy[idx] * dt

class run():
    def __init__(self, num_ball):
        turtle.speed(0)
        turtle.tracer(0)
        turtle.hideturtle()
        turtle.colormode(255)
        self.num = num_ball
        self.ballset = balldb()
        self.ballset.create(self.num)
        self.dt = 1
        self.border = self.ballset.border
        self.x = cuda.to_device([ball.x for ball in self.ballset.ball])
        self.y = cuda.to_device([ball.y for ball in self.ballset.ball])
        self.vx = cuda.to_device([ball.vx for ball in self.ballset.ball])
        self.vy = cuda.to_device([ball.vy for ball in self.ballset.ball])
        self.threadsperblock = 32
        self.blockspergrid = (self.num + (self.threadsperblock - 1)) // self.threadsperblock
    
    def draw(self):
        for ball in self.ballset.ball:
            ball.draw_ball()
    
    def run(self):
        start = time.time()
        while True:
            turtle.clear()
            self.border.draw_border()
            self.draw()
            update_ball_velocity[self.blockspergrid, self.threadsperblock](self.x, self.y, self.vx, self.vy, self.dt, self.border.canvas_width, self.border.canvas_height)
            cuda.synchronize()
            end = time.time()
            if end - start >= 1:
                start = time.time()
            turtle.update()

# Set the number of balls to simulate
num_balls = 5
st = run(num_balls)
st.run()

# Hold the window; close it by clicking the window close 'x' mark
turtle.done()
