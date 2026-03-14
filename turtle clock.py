import turtle
import time

# Set up the screen
screen = turtle.Screen()
screen.setup(width=1200, height=800)
screen.title("Analog Clock")
screen.bgcolor("white")
screen.tracer(0)

# Draw clock face
def draw_clock_face():
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.pensize(3)
    
    # Draw outer circle
    pen.penup()
    pen.goto(0, -210)
    pen.pendown()
    pen.circle(210)
    
    # Draw hour markers
    pen.penup()
    pen.goto(0, 0)
    for i in range(12):
        pen.forward(190)
        pen.pendown()
        pen.forward(20)
        pen.penup()
        pen.goto(0, 0)
        pen.right(30)

# Create clock hands
hour_hand = turtle.Turtle()
hour_hand.shape("arrow")
hour_hand.color("black")
hour_hand.shapesize(stretch_wid=0.5, stretch_len=5)

minute_hand = turtle.Turtle()
minute_hand.shape("arrow")
minute_hand.color("blue")
minute_hand.shapesize(stretch_wid=0.4, stretch_len=7)

second_hand = turtle.Turtle()
second_hand.shape("arrow")
second_hand.color("red")
second_hand.shapesize(stretch_wid=0.2, stretch_len=8)

# Draw the clock face
draw_clock_face()

# Update clock
def update_clock():
    current_time = time.localtime()
    hour = current_time.tm_hour % 12
    minute = current_time.tm_min
    second = current_time.tm_sec
    
    # Calculate angles
    second_angle = 90 - (second * 6)
    minute_angle = 90 - (minute * 6 + second * 0.1)
    hour_angle = 90 - (hour * 30 + minute * 0.5)
    
    # Update hand positions
    second_hand.setheading(second_angle)
    minute_hand.setheading(minute_angle)
    hour_hand.setheading(hour_angle)
    
    screen.update()
    screen.ontimer(update_clock, 1000)

# Start the clock
update_clock()
turtle.done()