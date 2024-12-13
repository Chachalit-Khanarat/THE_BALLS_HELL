class Paddle:
    def __init__(self, width, height, color, my_turtle, team, bhp = 10, head=0):
        self.width = width
        self.height = height
        self.location = [0, 0]
        self.color = color
        self.my_turtle = my_turtle
        self.my_turtle.penup()
        self.my_turtle.setheading(0)
        self.my_turtle.hideturtle()
        self.team = team
        self.head = head
        self.bhp = bhp

    def set_location(self, location):
        self.location = location
        self.my_turtle.goto(self.location[0], self.location[1])

    def draw(self):
        self.my_turtle.color(self.color)
        self.my_turtle.goto(self.location[0], self.location[1])
        self.my_turtle.setheading(self.head*2)
        self.my_turtle.right(90)
        self.my_turtle.forward(self.width/2)
        self.my_turtle.left(90)
        self.my_turtle.forward(self.width/2)
        self.my_turtle.pendown()
        self.my_turtle.begin_fill()
        for _ in range(3):
            self.my_turtle.left(120)
            self.my_turtle.forward(self.width)
        self.my_turtle.end_fill()
        self.my_turtle.penup()
        self.my_turtle.goto(self.location[0], self.location[1])

    def clear(self):
        self.my_turtle.clear()

    def __repr__(self):
        return f"Team : {(self.team).upper()}"
