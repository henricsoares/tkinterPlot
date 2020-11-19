import tkinter as tk
from tkinter import messagebox
import math
from typing import List
import random
from time import sleep
import canReadRadar as crr


class App(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.winfo_toplevel().title("Python Radar")
        self.frame = tk.Frame(master, background="#3297a8")
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.lado, self.cima = (self.frame.winfo_screenwidth()), (self.frame.winfo_screenheight())  # noqa: E501
        self.difLine = 0.075 * self.cima
        self.px = self.difLine * .3
        self.cores = ('#000000', '#808080', '#0000FF', '#00BFFF',
                      '#800080', '#8B008B', '#B0C4DE', '#800000',
                      '#A52A2A', '#FF7F50', '#FF0000', '#FF4500',
                      '#FF8C00', '#FFA500', '#00FFFF', '#40E0D0',
                      '#008B8B', '#7FFFD4', '#5F9EA0', '#2F4F4F',
                      '#00FF7F', '#90EE90', '#006400', '#008000',
                      '#32CD32', '#00FF00', '#FFDAB9', '#8B4513',
                      '#D2691E', '#D8BFD8', '#D8BFD8', '#DEB887')
        self.objs: List[int] = []
        self.objsCoords: List[list] = []
        self.x, self.y = 20, 40
        self.qtdObj = 32
        self.aux = False
        self.conecction = tk.BooleanVar()
        self.plotting = tk.BooleanVar()
        self.canvas = self.tkGraph()
        self.menu = tk.Canvas(self.frame, width=self.lado,
                              height=(self.cima/.8)*.2,
                              background='#3297a8', bd=0, highlightthickness=0)
        self.B1 = tk.Button(self.menu, text="Resize",
                            command=self.resizeCanvas)
        self.start = tk.Radiobutton(self.menu, text="Start",
                                    command=self.startStop,
                                    variable=self.plotting, value=True,
                                    indicatoron=0)
        self.stop = tk.Radiobutton(self.menu, text="Stop",
                                   command=self.startStop,
                                   variable=self.plotting, value=False,
                                   indicatoron=0)
        self.online = tk.Radiobutton(self.menu, text="Online",
                                     command=self.changeMode,
                                     variable=self.conecction, value=True,
                                     indicatoron=0)
        self.offline = tk.Radiobutton(self.menu, text="Offline",
                                      command=self.changeMode,
                                      variable=self.conecction, value=False,
                                      indicatoron=0)
        self.E1 = tk.Entry(self.menu, bd=5, width=3)
        self.E2 = tk.Entry(self.menu, bd=5, width=3)
        self.L1 = tk.Label(self.menu, text="X")
        self.L2 = tk.Label(self.menu, text="Y")
        self.mode = tk.Label(self.menu, text="Mode:")
        self.canvas.pack(side=tk.TOP)
        self.L1.pack(side=tk.LEFT)
        self.E1.pack(side=tk.LEFT)
        self.L2.pack(side=tk.LEFT)
        self.E2.pack(side=tk.LEFT)
        self.B1.pack(side=tk.LEFT, padx=(0, 50))
        self.online.pack(side=tk.RIGHT)
        self.offline.pack(side=tk.RIGHT)
        self.mode.pack(side=tk.RIGHT)
        self.stop.pack(side=tk.RIGHT, padx=(0, 50))
        self.start.pack(side=tk.RIGHT)
        self.menu.pack(side=tk.TOP)

    def tkGraph(self):
        self.getD()
        canvas = tk.Canvas(self.frame, width=self.lado, height=self.cima,
                           background='white')
        self.configPlot(canvas)
        return canvas

    def getD(self):
        dx = 2*self.x
        dy = self.y
        propG = dy/dx
        self.lado, self.cima = (self.frame.winfo_screenwidth()), (self.frame.winfo_screenheight())  # noqa: E501
        propF = self.cima/self.lado
        if propG <= propF:
            while propG <= propF:
                self.cima -= 1
                propF = self.cima/self.lado
        self.cima = (0.8 * self.cima)
        self.lado = self.cima / propG
        self.difLine = 0.075 * self.cima
        self.px = self.difLine * .3

    def getLabels(self):
        dx = self.x * 2
        dy = self.y
        xLabels, yLabels, xs = [], [], [-dx/2, -dx/4, 0, dx/4, dx/2]
        for i in range(len(xs)):
            if (xs[i]-int(xs[i])) != 0.0:
                xLabels.append(xs[i])
            else:
                xLabels.append(int(xs[i]))
        xLabels[len(xLabels)-1] = str(xLabels[len(xLabels)-1]) + ' m'
        for i in range(6):
            label = round((dy - ((dy/4) * i)), 2)
            difLabelY = label - int(label)
            if(difLabelY != 0.0):
                yLabels.append(label)
            else:
                yLabels.append(int(label))
        yLabels[0] = str(yLabels[0]) + ' m'
        return [xLabels, yLabels]

    def configPlot(self, canvas):
        labels = self.getLabels()
        xLabels, yLabels = labels[0], labels[1]
        a, b, c, d = [self.difLine, self.difLine], [self.lado - self.difLine, self.difLine], [self.lado - self.difLine, self.cima - self.difLine], [self.difLine, self.cima - self.difLine]  # noqa: E501
        canvas.create_line(a, b, c, d, a, fill='black', width=2)
        stepX = (b[0] - a[0]) / 4
        stepY = (d[1] - a[1]) / 4
        for i in range(5):
            canvas.create_line([self.difLine + (i * stepX), d[1], self.difLine + (i * stepX), d[1] + (self.difLine / 3)], fill='black', width=2)  # noqa: E501
            canvas.create_line([a[0], self.difLine + (i * stepY), a[0] - (self.difLine / 3), self.difLine + (i * stepY)], fill='black', width=2)  # noqa: E501
            canvas.create_text(self.difLine + (i * stepX), d[1] + (0.7 * self.difLine), fill="black", font="Arial 10 bold", text=xLabels[i])  # noqa: E501
            canvas.create_text(a[0] - (0.5 * self.difLine), (self.difLine * .75) + (i * stepY), fill="black", font="Arial 10 bold", text=yLabels[i])  # noqa: E501
        tg = math.tan(45 * math.pi / 180)
        coY = self.cima - (tg * ((self.lado / 2) - self.difLine)) - self.difLine  # noqa: E501
        points = [self.difLine, coY,
                  self.lado/2, self.cima - self.difLine,
                  self.lado - self.difLine, coY,
                  self.lado - self.difLine, self.difLine,
                  self.difLine, self.difLine,
                  self.difLine, coY]
        canvas.create_polygon(points, outline='black',
                              fill='#28d8ff', width=2)
        canvas.create_line(self.lado/2,
                           self.difLine,
                           self.lado/2,
                           self.cima - self.difLine,
                           fill='#5F9EA0', width=2)
        canvas.create_line(self.lado * (.25) + (self.difLine / 2),
                           self.difLine,
                           self.lado * (.25) + (self.difLine / 2),
                           self.cima - self.difLine,
                           fill='#5F9EA0', width=2)
        canvas.create_line(self.lado * (.75) - (self.difLine / 2),
                           self.difLine,
                           self.lado * (.75) - (self.difLine / 2),
                           self.cima - self.difLine,
                           fill='#5F9EA0', width=2)
        canvas.create_line(self.difLine, self.cima/2,
                           self.lado - self.difLine,
                           self.cima/2,
                           fill='#5F9EA0', width=2)
        canvas.create_line(self.difLine,
                           self.cima * (.25) + (self.difLine / 2),
                           self.lado - self.difLine,
                           self.cima * (.25) + (self.difLine / 2),
                           fill='#5F9EA0', width=2)
        canvas.create_line(self.difLine,
                           self.cima * (.75) - (self.difLine / 2),
                           self.lado - self.difLine,
                           self.cima * (.75) - (self.difLine / 2),
                           fill='#5F9EA0', width=2)

    def resizeCanvas(self):
        if self.E1.get() != '' and self.E2.get() != '':
            self.x, self.y = int(self.E1.get()), int(self.E2.get())
            if self.x < .9*self.y:
                self.canvas.delete('all')
                self.getD()
                self.canvas.config(width=self.lado, height=self.cima)
                self.configPlot(self.canvas)
            else:
                messagebox.showinfo("Dimensões incorretas",
                                    "Informe um valor menor para x!")
        else:
            messagebox.showinfo("",
                                "Informe x e y")

    def rotate(self, points, center):
        angle = math.radians(45)
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

    def getPos(self, xp, yp, dx, dy, form):
        propY = (self.cima - (2 * self.difLine)) / dy
        propX = (self.lado - (2 * self.difLine)) / (2 * dx)
        nx = (self.lado / 2) + (xp * propX)
        ny = self.cima - self.difLine - (yp * propY)
        self.px = self.difLine * .3
        h = self.px * (math.sqrt(3) / 2)
        if form == 'circle':
            coords = [nx - (self.difLine/10), ny - (self.difLine/10),
                      nx + (self.difLine/10), ny + (self.difLine/10)]
            return coords
        if form == 'top':
            coords = [nx - (self.px/2), self.difLine + h + self.px*.05,
                      nx + (self.px/2), self.difLine + h + self.px*.05,
                      nx, self.difLine + self.px*.05,  # top
                      nx - (self.px/2), self.difLine + h + self.px*.05]
            return coords
        if form == 'right':
            coords = [(self.lado) - h - self.difLine, ny - (self.px/2),
                      (self.lado) - h - self.difLine, ny + (self.px/2),
                      (self.lado) - self.difLine, ny,
                      (self.lado) - h - self.difLine, ny - (self.px/2)]
            return coords
        if form == 'left':
            coords = [h + self.difLine, ny + (self.px/2),
                      h + self.difLine, ny - (self.px/2),
                      self.difLine, ny,
                      h + self.difLine, ny + (self.px/2)]
            return coords
        if form == 'trCorner':
            coords = [[self.lado - self.difLine - (self.px/2),
                       self.difLine + h + self.px*.05],
                      [self.lado - self.difLine + (self.px/2),
                       self.difLine + h + self.px*.05],
                      [self.lado - self.difLine, self.difLine + self.px*.05]]
            coords = self.rotate(coords,
                                 [self.lado - self.difLine, self.difLine])
            return coords
        if form == 'tlCorner':
            coords = [[h + self.difLine, self.difLine + (self.px/2)],
                      [h + self.difLine, self.difLine - (self.px/2)],
                      [self.difLine, self.difLine]]
            coords = self.rotate(coords, [self.difLine, self.difLine])
            return coords
        if form == 'none':
            return [nx, ny]

    def tkPlot(self, x, y, obj):
        cor = self.cores[obj]
        if (abs(x) <= .95*self.x and y <= .95*self.y and y >= .05*self.y):
            coords = self.getPos(x, y, self.x, self.y, 'circle')
            id = self.canvas.create_oval(coords, fill=cor, width=1)  # noqa: E501
            return id
        else:
            if y > .95*self.y and abs(x) <= .95*self.x:  # top
                coords = self.getPos(x, y, self.x, self.y, 'top')
                id = self.canvas.create_polygon(coords,
                                                outline='black', fill=cor,
                                                width=self.px*.05)
                return id
            if y <= .95*self.y and x > .95*self.x:  # right
                coords = self.getPos(x, y, self.x, self.y, 'right')
                id = self.canvas.create_polygon(coords,
                                                outline='black', fill=cor,
                                                width=self.px*.05)
                return id
            if y <= .95*self.y and x < .95*-self.x:  # left
                coords = self.getPos(x, y, self.x, self.y, 'left')
                id = self.canvas.create_polygon(coords,
                                                outline='black', fill=cor,
                                                width=self.px*.05)
                return id
            if y > .95*self.y and x > .95*self.x:  # top right corner
                coords = self.getPos(x, y, self.x, self.y, 'trCorner')
                id = self.canvas.create_polygon(coords,
                                                outline='black', fill=cor,
                                                width=self.px*.05)
                return id
            if y > .95*self.y and x < .95*-self.x:  # top left corner
                coords = self.getPos(x, y, self.x, self.y, 'tlCorner')
                id = self.canvas.create_polygon(coords,
                                                outline='black', fill=cor,
                                                width=self.px*.05)
                return id

    def clearObjs(self):
        for i in range(len(self.objs)):
            self.canvas.delete(self.objs[i])
            self.master.update()

    def startStop(self):
        if self.plotting.get():
            if not self.conecction.get():
                if not self.aux:
                    self.aux = True
                    self.clearObjs()
                    self.objs = []
                    self.objsCoords = []
                    for i in range(self.qtdObj):
                        self.objsCoords.append([random.uniform(-(1.1*self.x),
                                                1.1*self.x),
                                                random.uniform(self.y/2,
                                                1.1*self.y)])
                        self.objs.append(self.tkPlot(self.objsCoords[i][0],
                                         self.objsCoords[i][1], i))

                    while self.aux:
                        try:
                            for i in range(len(self.objs)):
                                xx, yy = random.uniform(self.objsCoords[i][0]*.95,  # noqa: E501
                                                        self.objsCoords[i][0]*1.05), random.uniform(self.objsCoords[i][1]*.95,  # noqa: E501
                                                                                                    self.objsCoords[i][1]*1.05)  # noqa: E501
                                self.canvas.delete(self.objs[i])
                                self.objs[i] = self.tkPlot(xx, yy, i)
                            self.master.update()
                            sleep(.15)
                        except Exception:
                            self.aux = False
                        pass
                else:
                    pass
            else:
                self.plotOnline()
        else:
            if self.aux:
                self.clearObjs()
                self.aux = False
            else:
                pass

    def plotOnline(self):
        if not self.aux:
            self.aux = True
            for i in range(len(self.objs)):
                self.canvas.delete(self.objs[i])
                self.master.update()
            self.objs = []
            data = crr.read(True)
            xRead = data[1]
            yRead = data[2]
            for i in range(self.qtdObj):
                self.objs.append(self.tkPlot(xRead[i], yRead[i], i))
            while self.aux:
                try:
                    data = crr.read(True)
                    xRead = data[1]
                    yRead = data[2]
                    for i in range(len(self.objs)):
                        self.canvas.delete(self.objs[i])
                        self.objs[i] = self.tkPlot(xRead[i], yRead[i], i)
                    self.master.update()
                except Exception:
                    crr.release()
                    self.aux = False
        else:
            pass

    def changeMode(self):
        if self.conecction.get() == 1:
            connect = crr.connect(self.qtdObj)
            if connect[0]:
                messagebox.showinfo(connect[1],
                                    "Connection ok")
            else:
                messagebox.showinfo("No connection",
                                    connect[1])
                self.online.deselect()
                self.offline.select()
        else:
            release = crr.release()
            messagebox.showinfo(release[1],
                                'Can released')
            self.aux = False
            self.clearObjs()
            if self.plotting.get():
                self.start.deselect()
                self.stop.select()


root = tk.Tk()
app = App(root)
root.mainloop()
