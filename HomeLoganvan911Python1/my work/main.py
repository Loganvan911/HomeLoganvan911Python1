# fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
# newlist = []

# for x in fruits:
#   if "e" in x:
#     newlist.append(x)

# print(newlist)

# fruits = ["apple", "banana", "cherry", "kiwi", "mango"]

# newlist = [x for x in fruits if "p" in x]

# print(newlist)

import turtle

t = turtle.Turtle()
t.speed(0)

# Пелюстки
t.color("red")
for i in range(36):
    t.circle(100, 60)
    t.left(120)
    t.circle(100, 60)
    t.left(170)

# Стебло
t.penup()
t.goto(0, -100)
t.pendown()
t.color("green")
t.right(90)
t.forward(200)

turtle.done()

# import turtle

# screen = turtle.Screen()
# screen.bgcolor("white")

# rose = turtle.Turtle()
# rose.speed(0)
# rose.color("red")

# # Квітка
# for i in range(36):
#     rose.circle(100, 60)
#     rose.left(120)
#     rose.circle(100, 60)
#     rose.left(170)

# # Стебло
# rose.penup()
# rose.goto(0, -120)
# rose.setheading(-90)
# rose.pendown()
# rose.color("brown")
# rose.forward(250)

# # Листочок
# rose.left(45)
# rose.begin_fill()
# for _ in range(2):
#     rose.circle(40, 90)
#     rose.left(90)
# rose.end_fill()

# rose.hideturtle()
# turtle.done()