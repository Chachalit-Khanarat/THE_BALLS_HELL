import turtle
import math

class ball():
    def __init__(self, color, size, x, y , vx, vy, mass, team, bhp = 0):
        self.color = color
        self.size = size
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.wt = bhp
        self.team = team
        self.bhp = bhp

    def draw_ball(self):
        turtle.penup()
        turtle.color(self.color)
        turtle.fillcolor(self.color)
        turtle.goto(self.x,self.y)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(self.size)
        turtle.end_fill()

    def move_ball(self,dt):
        self.x += self.vx*dt
        self.y += self.vy*dt

    def wall_hit(self, canvas_width, canvas_height):
        if abs(self.x) >= (canvas_width - self.size):
            self.vx = -self.vx
            self.bhp -= 1
            return True

        if abs(self.y) >= (canvas_height - self.size):
            self.vy = -self.vy
            self.bhp -= 1
            return True
        
        return False
    
    def paddle_hit(self,paddle):
        if (self.size + (paddle.width/2) >= self.distance_paddle(paddle)) and self.team != paddle.team:
            print(self.size + (paddle.width/2), self.distance_paddle(paddle))
            print(self)
            return True
        return False
    
    def distance(self, that):
        x1 = self.x
        y1 = self.y
        x2 = that.x
        y2 = that.y
        d = math.sqrt((y2-y1)**2 + (x2-x1)**2)
        return d
    
    def distance_paddle(self, paddle):
        x1 = self.x
        y1 = self.y
        x2 = paddle.location[0]
        y2 = paddle.location[1]
        d = math.sqrt((y2-y1)**2 + (x2-x1)**2)
        return d

    def ball_hit(self, that):
        if (self.distance(that) <= self.size + that.size) and self.team != that.team:
            return True
        return False

    def __repr__(self):
        return f"hp : {self.bhp}, team {self.team}"




