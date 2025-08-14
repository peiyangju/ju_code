import turtle


# 海龟画图
t = turtle.Pen()
colors = ['red', 'yellow', 'blue', 'green', 'lemon chiffon', 'salmon']
t.pencolor(colors[0])
turtle.bgcolor(colors[1])
for x in range(0, 100, 1):
    t.circle(x)
    t.left(91)
