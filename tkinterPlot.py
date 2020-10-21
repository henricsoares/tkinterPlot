import tkinter as tk
import random  # noqa: F401
from typing import List
from time import sleep  # noqa: F401
import canReadRadar as crr  # noqa: F401
import keyboard  # noqa: F401
import math
from tkinter import messagebox  # noqa: F401
window = tk.Tk()
cores = ('#000000', '#808080', '#0000FF', '#00BFFF',
         '#800080', '#8B008B', '#B0C4DE', '#800000',
         '#A52A2A', '#FF7F50', '#FF0000', '#FF4500',
         '#FF8C00', '#FFA500', '#00FFFF', '#40E0D0',
         '#008B8B', '#7FFFD4', '#5F9EA0', '#2F4F4F',
         '#00FF7F', '#90EE90', '#006400', '#008000',
         '#32CD32', '#00FF00', '#FFDAB9', '#8B4513',
         '#D2691E', '#D8BFD8', '#D8BFD8', '#DEB887')
objs: List[int] = []
objsCoords: List[list] = []
difLine = 0
# window.attributes('-fullscreen', True)


def tkGraph(Window, dX, dY):
    global lado, cima, dx, dy, my_canvas, difLine, window
    window.state('zoomed')
    # window.attributes('-fullscreen', True)
    frame = tk.Frame(window, background="#3297a8")
    frame.pack(fill=tk.BOTH, expand=True)
    xLabels, yLabels = [], []
    dy = dY
    dx = dX * 2
    propG = dy/dx
    if dx % 2 != 0:
        xLabels.append(-1 * dx/2)
        xLabels.append(-1 * (dx/4))
        xLabels.append(0)
        xLabels.append(dx/4)
        xLabels.append(str(dx/2) + ' m')
    else:
        xLabels.append(int(-1 * dx/2))
        xLabels.append(int(-1 * (dx/4)))
        xLabels.append(int(0))
        xLabels.append(int(dx/4))
        xLabels.append(str(int(dx/2)) + ' m')
    for i in range(6):
        label = round((dy - ((dy/4) * i)), 2)
        difLabel = label - int(label)
        if(difLabel != 0.0):
            yLabels.append(label)
            # print(difLabel)
        else:
            yLabels.append(int(label))
    yLabels[0] = str(yLabels[0]) + ' m'
    lado, cima = (frame.winfo_screenwidth()), (frame.winfo_screenheight())
    propF = cima/lado
    if propG <= propF:
        while propG <= propF:
            cima -= 1
            propF = cima/lado
    cima = (0.85 * cima)
    lado = cima / propG
    my_canvas = tk.Canvas(frame, width=lado, height=cima, background='white')
    my_canvas.pack(side=tk.TOP)
    difLine = 0.075 * cima
    a, b, c, d = [difLine, difLine], [lado - difLine, difLine], [lado - difLine, cima - difLine], [difLine, cima - difLine]  # noqa: E501
    my_canvas.create_line(a, b, c, d, a, fill='black', width=2)
    stepX = (b[0] - a[0]) / 4
    stepY = (d[1] - a[1]) / 4
    for i in range(5):
        my_canvas.create_line([difLine + (i * stepX), d[1], difLine + (i * stepX), d[1] + (difLine / 3)], fill='black', width=2)  # noqa: E501
        my_canvas.create_line([a[0], difLine + (i * stepY), a[0] - (difLine / 3), difLine + (i * stepY)], fill='black', width=2)  # noqa: E501
        my_canvas.create_text(difLine + (i * stepX), d[1] + (0.7 * difLine), fill="black", font="Arial 10 bold", text=xLabels[i])  # noqa: E501
        my_canvas.create_text(a[0] - (0.5 * difLine), (difLine * .75) + (i * stepY), fill="black", font="Arial 10 bold", text=yLabels[i])  # noqa: E501
    tg = math.tan(45 * math.pi / 180)
    coY = cima - (tg * ((lado / 2) - difLine)) - difLine
    points = [difLine, coY,
              lado/2, cima - difLine,
              lado - difLine, coY,
              lado - difLine, difLine,
              difLine, difLine,
              difLine, coY]
    my_canvas.create_polygon(points, outline='black',
                             fill='#28d8ff', width=2)
    lineX1 = my_canvas.create_line(lado/2, difLine, lado/2, cima - difLine, fill='#5F9EA0', width=2)  # noqa: F841, E501
    lineX2 = my_canvas.create_line(lado * (.25) + (difLine / 2), difLine, lado * (.25) + (difLine / 2), cima - difLine, fill='#5F9EA0', width=2)  # noqa: F841, E501
    lineX3 = my_canvas.create_line(lado * (.75) - (difLine / 2), difLine, lado * (.75) - (difLine / 2), cima - difLine, fill='#5F9EA0', width=2)  # noqa: F841, E501
    lineY1 = my_canvas.create_line(difLine, cima/2, lado - difLine, cima/2, fill='#5F9EA0', width=2)  # noqa: F841, E501
    lineY2 = my_canvas.create_line(difLine, cima * (.25) + (difLine / 2), lado - difLine, cima * (.25) + (difLine / 2), fill='#5F9EA0', width=2)  # noqa: F841, E501
    lineY3 = my_canvas.create_line(difLine, cima * (.75) - (difLine / 2), lado - difLine, cima * (.75) - (difLine / 2), fill='#5F9EA0', width=2)  # noqa: F841, E501'''
    return my_canvas


def getPos(x, y, form):
    propY = (cima - (2 * difLine)) / dy
    propX = (lado - (2 * difLine)) / (2 * dx)
    nx = (lado / 2) + (x * propX)
    ny = cima - difLine - (y * propY)
    px = difLine * .3
    h = px * (math.sqrt(3) / 2)
    if form == 'circle':
        coords = [nx - (difLine/10), ny - (difLine/10),
                  nx + (difLine/10), ny + (difLine/10)]
        return coords
    if form == 'top':
        coords = [nx - (px/2), difLine + h + px*.05,  # left down
                  nx + (px/2), difLine + h + px*.05,  # right down # noqa: E501
                  nx, difLine + px*.05,  # top
                  nx - (px/2), difLine + h + px*.05]
        return coords
    if form == 'right':
        coords = [(lado) - h - difLine, ny - (px/2),
                  (lado) - h - difLine, ny + (px/2),
                  (lado) - difLine, ny,
                  (lado) - h - difLine, ny - (px/2)]
        return coords
    if form == 'left':
        coords = [h + difLine, ny + (px/2),
                  h + difLine, ny - (px/2),
                  difLine, ny,
                  h + difLine, ny + (px/2)]
        return coords
    if form == 'none':
        return [nx, ny]


def tkPlot(x, y, obj):
    if (abs(x*2) <= .95*dx and y <= .95*dy and y >= .05*y):
        x = x * 2
        coords = getPos(x, y, 'circle')
        cor = cores[obj]
        id = my_canvas.create_oval(coords, fill=cor, width=1)  # noqa: E501
        return id
    else:
        cor = cores[obj]
        px = difLine * .3
        if y > .95*dy and abs(x*2) <= .95*dx:  # top
            # print('top')
            x = x * 2
            coords = getPos(x, y, 'top')
            id = my_canvas.create_polygon(coords,
                                          outline='black', fill=cor,
                                          width=px*.05)
            return id
        if y <= .95*dy and (x*2) > .95*dx:  # right
            # print('right')
            coords = getPos(x, y, 'right')
            id = my_canvas.create_polygon(coords,
                                          outline='black', fill=cor,
                                          width=px*.05)
            return id
        if y <= .95*dy and (2*x) < (.95*-dx):  # left
            # print('left')
            coords = getPos(x, y, 'left')
            id = my_canvas.create_polygon(coords,
                                          outline='black', fill=cor,
                                          width=px*.05)
            return id


qtdObj = 32  # number of objects
xl, yl = 20, 40  # x and y assis limits
graph = tkGraph(window, xl, yl)  # calling the function

for i in range(qtdObj):
    objsCoords.append([random.uniform(-(1.1*xl), 1.1*xl),
                      random.uniform(yl/2, 1.1*yl)])
    objs.append(tkPlot(objsCoords[i][0], objsCoords[i][1], i))
aux = True
while aux and not keyboard.is_pressed('q'):
    try:
        for i in range(len(objs)):
            xx, yy = random.uniform(objsCoords[i][0]*.95,
                                    objsCoords[i][0]*1.05), random.uniform(objsCoords[i][1]*.95,  # noqa: E501
                                                                           objsCoords[i][1]*1.05)  # noqa: E501
            graph.delete(objs[i])
            window.update()
            objs[i] = tkPlot(xx, yy, i)
        window.update()
        sleep(.2)
    except Exception:
        aux = False

# qtdObj = int(input("Quantidade de objetos (máx. 32): "))
'''qtdObj = 32
graph = tkGraph(window, 10, 20)
print((crr.connect(qtdObj))[1])
for _ in range(qtdObj):  # initializing objects
    objs.append(tkPlot(1, 1))  # in the top left corner position

while not keyboard.is_pressed('q'):  # plotting data from can
    try:
        data = crr.read(True)  # read X and Y values from can
        for i in range(qtdObj):
            x = data[1][i]
            y = data[2][i]
            coords = getPos(x, y)
            x, y = coords[0], coords[1]
            coords = [x - (difLine/10), y - (difLine/10),
                      x + (difLine/10), y + (difLine/10)]
            graph.coords(objs[i], coords)  # update the objects position
            window.update()  # update the window
    except Exception:
        aux = False  # close the program if something is wrong
print((crr.release())[1])'''

'''tkGraph(window, 50, 80)
tkPlot(0, 79.9)'''
window.mainloop()
