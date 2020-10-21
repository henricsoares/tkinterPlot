import tkinter as tk
from tkinter import messagebox  # noqa: F401
import math
from typing import List
import random  # noqa: F401
import keyboard  # noqa: F401
from time import sleep  # noqa: F401

window = tk.Tk()
frame = tk.Frame()
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
qtdObj = 32
x, y = 20, 40
aux = False


def tkGraph(Window, dX, dY):
    global window, frame  # lado, cima, dx, dy, my_canvas, difLine,
    frame = tk.Frame(window, background="#3297a8")
    frame.pack(fill=tk.BOTH, expand=True)
    dx = 2*dX
    dy = dY
    propG = dy/dx
    labels = getLabels(dX, dY)
    dims = getD(propG)
    lado, cima = dims[0], dims[1]
    my_canvas = tk.Canvas(frame, width=lado, height=cima, background='white')
    configPlot(my_canvas, lado, cima, labels[0], labels[1])
    return my_canvas


def rotate(points, angle, center):
    angle = math.radians(angle)
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    cx, cy = center
    new_points = []
    for x_old, y_old in points:
        x_old -= cx
        y_old -= cy
        x_new = x_old * cos_val - y_old * sin_val
        y_new = x_old * sin_val + y_old * cos_val
        new_points.append([x_new + cx, y_new + cy])
    return new_points


def getD(propG):
    global lado, cima
    lado, cima = (frame.winfo_screenwidth()), (frame.winfo_screenheight())
    propF = cima/lado
    if propG <= propF:
        while propG <= propF:
            cima -= 1
            propF = cima/lado
    cima = (0.8 * cima)
    lado = cima / propG
    return [lado, cima]


def getLabels(dx, dy):
    xLabels, yLabels = [], []
    dx = dx * 2
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
        else:
            yLabels.append(int(label))
    yLabels[0] = str(yLabels[0]) + ' m'
    return [xLabels, yLabels]


def configPlot(my_canvas, lado, cima, xLabels, yLabels):
    global difLine
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
    lineY3 = my_canvas.create_line(difLine, cima * (.75) - (difLine / 2), lado - difLine, cima * (.75) - (difLine / 2), fill='#5F9EA0', width=2)  # noqa: F841, E501


def resizeCanvas():
    global x, y
    if E1.get() != '' and E2.get() != '':
        x, y = int(E1.get()), int(E2.get())
        if x < .9*y:
            canvas.delete('all')
            prop = y/(2*x)
            dim = getD(prop)
            canvas.config(width=dim[0], height=dim[1])
            labels = getLabels(x, y)
            configPlot(canvas, dim[0], dim[1], labels[0], labels[1])
        else:
            messagebox.showinfo("Dimensões incorretas",
                                "Informe um valor menor para x!")
    else:
        messagebox.showinfo("",
                            "Informe x e y")


def getPos(xp, yp, dx, dy, form):
    propY = (cima - (2 * difLine)) / dy
    propX = (lado - (2 * difLine)) / (2 * dx)
    nx = (lado / 2) + (xp * propX)
    ny = cima - difLine - (yp * propY)
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
    if form == 'trCorner':
        coords = [[lado - difLine - (px/2), difLine + h + px*.05],
                  [lado - difLine + (px/2), difLine + h + px*.05],
                  [lado - difLine, difLine + px*.05]]
        coords = rotate(coords, 45, [lado - difLine, difLine])
        return coords
    if form == 'tlCorner':
        coords = [[h + difLine, difLine + (px/2)],
                  [h + difLine, difLine - (px/2)],
                  [difLine, difLine]]
        coords = rotate(coords, 45, [difLine, difLine])
        return coords
    if form == 'none':
        return [nx, ny]


def tkPlot(x, y, dx, dy, obj):
    cor = cores[obj]
    if (abs(x) <= .95*dx and y <= .95*dy and y >= .05*y):
        coords = getPos(x, y, dx, dy, 'circle')
        id = canvas.create_oval(coords, fill=cor, width=1)  # noqa: E501
        return id
    else:
        px = difLine * .3
        if y > .95*dy and abs(x) <= .95*dx:  # top
            # print('top')
            coords = getPos(x, y, dx, dy, 'top')
            id = canvas.create_polygon(coords,
                                       outline='black', fill=cor,
                                       width=px*.05)
            return id
        if y <= .95*dy and x > .95*dx:  # right
            # print('right')
            coords = getPos(x, y, dx, dy, 'right')
            id = canvas.create_polygon(coords,
                                       outline='black', fill=cor,
                                       width=px*.05)
            return id
        if y <= .95*dy and x < .95*-dx:  # left
            # print('left')
            coords = getPos(x, y, dx, dy, 'left')
            id = canvas.create_polygon(coords,
                                       outline='black', fill=cor,
                                       width=px*.05)
            return id
        if y > .95*dy and x > .95*dx:  # top right corner
            # print('top right corner')
            coords = getPos(x, y, dx, dy, 'trCorner')
            id = canvas.create_polygon(coords,
                                       outline='black', fill=cor,
                                       width=px*.05)
            return id
        if y > .95*dy and x < .95*-dx:  # top left corner
            # print('top left corner')
            coords = getPos(x, y, dx, dy, 'tlCorner')
            id = canvas.create_polygon(coords,
                                       outline='black', fill=cor,
                                       width=px*.05)
            return id


def startPlot():
    global aux, objs, objsCoords
    if not aux:
        aux = True
        for i in range(len(objs)):
            canvas.delete(objs[i])
            window.update()
        objs = []
        objsCoords = []
        for i in range(qtdObj):
            objsCoords.append([random.uniform(-(1.1*x), 1.1*x),
                              random.uniform(y/2, 1.1*y)])
            objs.append(tkPlot(objsCoords[i][0], objsCoords[i][1], x, y, i))

        while aux and not keyboard.is_pressed('q'):
            try:
                for i in range(len(objs)):
                    xx, yy = random.uniform(objsCoords[i][0]*.95,
                                            objsCoords[i][0]*1.05), random.uniform(objsCoords[i][1]*.95,  # noqa: E501
                                                                                   objsCoords[i][1]*1.05)  # noqa: E501
                    canvas.delete(objs[i])
                    window.update()
                    objs[i] = tkPlot(xx, yy, x, y, i)
                window.update()
                sleep(.15)
            except Exception:
                aux = False
    else:
        pass


def stopPlot():
    global aux
    if aux:
        aux = False
    else:
        pass


canvas = tkGraph(window, x, y)
canvas.pack(side=tk.TOP)
dims = getD(y/(2*x))
menu = tk.Canvas(frame, width=dims[0],
                 height=(dims[1]/.8)*.2, background='white')
menu.pack(side=tk.TOP)
B1 = tk.Button(menu, text="Resize", command=resizeCanvas)
B2 = tk.Button(menu, text="Start", command=startPlot)
B3 = tk.Button(menu, text="Stop", command=stopPlot)
E1 = tk.Entry(menu, bd=5, width=4)
E2 = tk.Entry(menu, bd=5, width=4)
L1 = tk.Label(menu, text="X")
L2 = tk.Label(menu, text="Y")
L1.pack(side=tk.LEFT)
E1.pack(side=tk.LEFT)
L2.pack(side=tk.LEFT)
E2.pack(side=tk.LEFT)
B1.pack(side=tk.LEFT)
B3.pack(side=tk.RIGHT)
B2.pack(side=tk.RIGHT)
window.mainloop()
