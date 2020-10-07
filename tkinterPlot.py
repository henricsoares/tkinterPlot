import tkinter as tk
import random  # noqa: F401
from typing import List
from time import sleep  # noqa: F401
import canReadRadar as crr  # noqa: F401
import keyboard  # noqa: F401
janela = tk.Tk()
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


def tkGraph(window, dX, dY):
    global lado, cima, dx, dy, my_canvas, difLine, janela
    window.state('zoomed')
    # janela.attributes('-fullscreen', True)
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
            print(difLabel)
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
    my_canvas.pack(side=tk.BOTTOM)
    '''lineX1 = my_canvas.create_line(lado/2, difLine, lado/2, cima - difLine, fill='#5F9EA0', width=2)  # noqa: F841, E501
    lineX2 = my_canvas.create_line(lado * (.25) + (difLine / 2), difLine, lado * (.25) + (difLine / 2), cima - difLine, fill='#5F9EA0', width=2)  # noqa: F841, E501
    lineX3 = my_canvas.create_line(lado * (.75) - (difLine / 2), difLine, lado * (.75) - (difLine / 2), cima - difLine, fill='#5F9EA0', width=2)  # noqa: F841, E501
    lineY1 = my_canvas.create_line(difLine, cima/2, lado - difLine, cima/2, fill='#5F9EA0', width=2)  # noqa: F841, E501
    lineY2 = my_canvas.create_line(difLine, cima * (.25) + (difLine / 2), lado - difLine, cima * (.25) + (difLine / 2), fill='#5F9EA0', width=2)  # noqa: F841, E501
    lineY3 = my_canvas.create_line(difLine, cima * (.75) - (difLine / 2), lado - difLine, cima * (.75) - (difLine / 2), fill='#5F9EA0', width=2)  # noqa: F841, E501'''
    return my_canvas


def getPos(x, y):
    if (abs(x) < dx and y < dy and y > 0):
        propY = (cima - (2 * difLine)) / dy
        propX = (lado - (2 * difLine)) / (2 * dx)
        nx = (lado / 2) + (x * propX)
        ny = cima - difLine - (y * propY)
        return [nx, ny]
    else:
        nx, ny = lado + 1, cima + 1
        print("object out of range")
        return [nx, ny]


def tkPlot(x, y):
    if (abs(x) < dx and y < dy and y > 0):
        x = x * 2
        pos = getPos(x, y)
        nx, ny = pos[0], pos[1]
        cor = cores[len(objs)]
        id = my_canvas.create_oval(nx - (difLine/7), ny - (difLine/7), nx + (difLine/7), ny + (difLine/7), fill=cor, width=0)  # noqa: E501
        return id
    else:
        cor = cores[len(objs)]
        id = my_canvas.create_oval(lado + 1, cima + 1, lado + 1, cima + 1, fill=cor, width=0)  # noqa: E501
        print("object out of range")


'''qtdObj = int(input('Quantidade de objetos:'))

for i in range(qtdObj):
    objsCoords.append([random.uniform(-7.9, 7.9), random.uniform(0.1, 4.9)])
    objs.append(tkPlot(objsCoords[i][0], objsCoords[i][1]))

aux = True
while aux:
    try:
        for i in range(len(objs)):
            xx, yy = objsCoords[i][0], objsCoords[i][1]
            coords = getPos(xx, yy)
            xx, yy = coords[0], coords[1]
            xx = random.uniform(xx - 7.5, xx + 7.5)
            yy = random.uniform(yy - 7.5, yy + 7.5)
            coords = [xx - 7.5, yy - 7.5,
                      xx + 7.5, yy + 7.5]
            graph.coords(objs[i], coords)
        janela.update()
        sleep(.2)
    except Exception:
        aux = False'''

qtdObj = int(input("Quantidade de objetos (máx. 32): "))
print(crr.connect(qtdObj))
graph = tkGraph(janela, 50, 80)
for _ in range(qtdObj):
    '''data = crr.read(True)
    x, y = data[1][0], data[2][0]
    objs.append(tkPlot(x, y))'''
    objs.append(tkPlot(1, 1))

while not keyboard.is_pressed('q'):
    try:
        for i in range(qtdObj):
            data = crr.read(True)
            x = data[1][i]
            y = data[2][i]
            coords = getPos(x, y)
            x, y = coords[0], coords[1]
            coords = [x - 7.5, y - 7.5,
                      x + 7.5, y + 7.5]
            graph.coords(objs[i], coords)
        # sleep(.2)
    except Exception:
        # print('algo errado')
        aux = False
    janela.update()
print(crr.release())

'''tkGraph(janela, 50, 80)
tkPlot(0, 79.9)
janela.mainloop()'''
