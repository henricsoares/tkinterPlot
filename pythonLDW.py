import tkinter as tk
from PIL import ImageTk, Image
import tkinter.font as font
import random  # noqa: F401
from time import sleep
import keyboard  # noqa: F401
import canReadCamera as canrd  # noqa: F401
from threading import Thread


class App(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.winfo_toplevel().title("Python LDW")
        self.rAux = False
        self.lAux = False
        self.rAuxx = False
        self.lAuxx = False
        self.frame = tk.Frame(master, background="#3297a8")
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.lado, self.cima = .8*(self.frame.winfo_screenwidth()), .8*(self.frame.winfo_screenheight())  # noqa: E501
        self.canvas = tk.Canvas(self.frame, width=self.lado, height=self.cima,
                                background='black')
        self.img = Image.open("truck.png")
        self.photo = ImageTk.PhotoImage(self.img)
        self.pw, self.ph = self.photo.width(), self.photo.height()
        self.propT = self.pw/self.ph
        self.pw = .3*self.lado
        self.ph = self.pw/self.propT
        self.img = self.img.resize((int(self.pw), int(self.ph)),
                                   Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.img)
        self.pw, self.ph = self.photo.width(), self.photo.height()
        self.metro = (self.pw/2)*1.0024465
        self.title = tk.Label(self.frame, text='LDW', background="#3297a8",
                              foreground='white')
        self.title['font'] = font.Font(size=30)
        self.canvas.pack(side=tk.BOTTOM)
        self.lab = tk.Label(self.canvas, image=self.photo, background='black')
        self.labpos = (self.lado/2)-(self.pw/2)
        self.lab.place(x=self.labpos, y=(self.cima/2)-(self.ph/2))
        self.title.pack(side=tk.TOP)
        self.llPos = [[self.lado/5, 0.0], [self.lado/5, self.cima]]
        self.lrPos = [[4*self.lado/5, 0.0], [4*self.lado/5, self.cima]]
        self.lw = .02*self.lado
        self.lr = self.canvas.create_line(self.lrPos, fill='white',
                                          width=self.lw)
        self.ll = self.canvas.create_line(self.llPos, fill='white',
                                          width=self.lw)
        self.left = self.lado/5
        self.right = 4*self.lado/5
        self.lLabel = self.canvas.create_text(self.llPos[0][0], 15, text="L",
                                              fill='orange',
                                              font=font.Font(size=int(self.lw),
                                              weight='bold'))
        self.rLabel = self.canvas.create_text(self.lrPos[0][0], 15, text="R",
                                              fill='blue',
                                              font=font.Font(size=int(self.lw),
                                              weight='bold'))
        self.ldValue = self.canvas.create_text((self.llPos[0][0])+(.05*self.lado),  # noqa: E501
                                               15, text='',
                                               fill='yellow',
                                               font=font.Font(size=int(self.lw),  # noqa: E501
                                               weight='bold'))
        self.rdValue = self.canvas.create_text((self.lrPos[0][0])+(.05*self.lado),  # noqa: E501
                                               15, text='',
                                               fill='yellow',
                                               font=font.Font(size=int(self.lw),  # noqa: E501
                                               weight='bold'))
        self.x1, self.y1 = self.lado, self.cima
        self.x2, self.y2 = (self.lado/2)-(self.pw/2), (self.cima/2)-(self.ph/2)
        self.blinkaux = False
        self.count = 0

    def verif(self):
        if (self.right - self.pw*1.05) < self.labpos < (self.pw*.05 + self.right):  # noqa: E501
            self.rAuxx = True
        else:
            app.rAuxx = False
        if (app.left - app.pw*1.05) < app.labpos < (app.pw*.05 + app.left):  # noqa: E501
            app.lAuxx = True
        else:
            app.lAuxx = False

    def _bell(self, act):
        if act == 'verif':
            self.after(500, self.verif)
            return
        elif act == 'bell':
            if self.lAux and self.lAuxx:
                self.canvas.bell()
                self.canvas.itemconfig(app.ll, fill='red')
            else:
                self.canvas.itemconfig(app.ll, fill='yellow')
            if self.rAux and self.rAuxx:
                self.canvas.bell()
                self.canvas.itemconfig(app.lr, fill='red')
            else:
                self.canvas.itemconfig(app.lr, fill='yellow')
            return

    def blinkt(self):
        '''self.lab.place(x=self.x1, y=self.y1)
        self.x1, self.x2 = self.x2, self.x1
        self.y1, self.y2 = self.y2, self.y1
        self.blinkaux = False'''
        sleep(.5)
        if self.blinkaux:
            self.count += 1
            self.blinkaux = False
        else:
            self.count = 0
        print(self.count)


'''conection = (canrd.connect())
while not conection[0]:
    print('Trying to connect...')
    conection = (canrd.connect())
    sleep(1)
print(conection[1])
conection = conection[0]'''
root = tk.Tk()
app = App(root)
auxx = True
while auxx:
    try:
        '''data = canrd.canRead(conection)
        left = float(input("Left: "))
        right = float(input("Right: "))'''
        '''app.left = round(random.uniform(-2, -1), 2)
        app.right = round(random.uniform(1, 2), 2)'''
        if keyboard.is_pressed('a'):
            for i in range(0, 50, 10):
                app.lab.place(x=app.labpos-i,
                              y=(app.cima/2)-(app.ph/2))
                root.update()
                sleep(.00001)
            app.labpos -= 50
        elif keyboard.is_pressed('d'):
            for i in range(0, 50, 10):
                app.lab.place(x=app.labpos+i,
                              y=(app.cima/2)-(app.ph/2))
                root.update()
                sleep(.00001)
            app.labpos += 50
        # print(data)
        if True:  # data[0]:
            app.blinkaux = False
            '''data = data[1]
            app.left = round(data[0], 2)
            app.right = round(data[1], 2)'''
            app.canvas.itemconfigure(app.ldValue, text=app.left)
            app.canvas.itemconfigure(app.rdValue, text=app.right)
            '''if app.left < 0 < app.right:
                ampl = (abs(app.left)+app.right) / 2
                app.labpos = ((ampl - app.right)*app.metro) + (app.lado/2)-(app.pw/2)  # noqa: E501
                app.left, app.right = -ampl*app.metro+(app.lado/2), ampl*app.metro+(app.lado/2)  # noqa: E501
            elif app.left > 0 > app.right:
                ampl = (abs(app.right)+app.left) / 2
                app.labpos = ((ampl - app.left)*app.metro) + (app.lado/2)-(app.pw/2)  # noqa: E501
                app.right, app.left = -ampl*app.metro+(app.lado/2), ampl*app.metro+(app.lado/2)  # noqa: E501
            else:
                app.labpos = (app.lado/2)-(app.pw/2)
                app.left, app.right = -2*app.metro+(app.lado/2), 2*app.metro+(app.lado/2)  # noqa: E501
                app.canvas.itemconfigure(app.ldValue, text='')
                app.canvas.itemconfigure(app.rdValue, text='')
                app.canvas.itemconfig(app.ll, fill='white')
                app.canvas.itemconfig(app.lr, fill='white')'''
            '''elif app.left > 0 < app.right:
                if app.right >= app.left:
                    ampl = (app.right - app.left) / 2
                    app.labpos = ((ampl - app.right)*app.metro) + (app.lado/2)-(app.pw/2)  # noqa: E501
                    app.left, app.right = -ampl*app.metro+(app.lado/2), ampl*app.metro+(app.lado/2)  # noqa: E501
                else:
                    ampl = (app.left - app.right) / 2
                    app.labpos = ((ampl - app.left)*app.metro) + (app.lado/2)-(app.pw/2)  # noqa: E501
                    app.right, app.left = -ampl*app.metro+(app.lado/2), ampl*app.metro+(app.lado/2)  # noqa: E501
            elif app.left < 0 > app.right:
                if app.left <= app.right:
                    ampl = (abs(app.left) - abs(app.right)) / 2
                    app.labpos = ((ampl - app.right)*app.metro) + (app.lado/2)-(app.pw/2)  # noqa: E501
                    app.left, app.right = -ampl*app.metro+(app.lado/2), ampl*app.metro+(app.lado/2)  # noqa: E501
                else:
                    ampl = (abs(app.right) - abs(app.left)) / 2
                    app.labpos = ((ampl - app.left)*app.metro) + (app.lado/2)-(app.pw/2)  # noqa: E501
                    app.right, app.left = -ampl*app.metro+(app.lado/2), ampl*app.metro+(app.lado/2)  # noqa: E501'''
            # app.left, app.right = -ampl*app.metro+(app.lado/2), ampl*app.metro+(app.lado/2)  # noqa: E501
            app.llPos[0][0] = app.left
            app.llPos[1][0] = app.left
            app.lrPos[0][0] = app.right
            app.lrPos[1][0] = app.right
            app.canvas.coords(app.lr, app.lrPos[0][0], app.lrPos[0][1],
                              app.lrPos[1][0], app.lrPos[1][1])
            app.canvas.coords(app.ll, app.llPos[0][0], app.llPos[0][1],
                              app.llPos[1][0], app.llPos[1][1])
            app.canvas.coords(app.lLabel, app.llPos[0][0], 15)
            app.canvas.coords(app.rLabel, app.lrPos[0][0], 15)
            app.canvas.coords(app.ldValue, app.llPos[0][0]+(.05*app.lado),
                              15)
            app.canvas.coords(app.rdValue, app.lrPos[0][0]+(.05*app.lado),
                              15)
            app.lab.place(x=app.labpos, y=(app.cima/2)-(app.ph/2))
            if (app.right - app.pw*1.05) < app.labpos < (app.pw*.05 + app.right):  # noqa: E501
                app.rAux = True
                thread = Thread(target=app._bell('verif'), daemon=True)
                thread.start()
            else:
                app.rAux = False
                app.rAuxx = False
            if (app.left - app.pw*1.05) < app.labpos < (app.pw*.05 + app.left):  # noqa: E501
                app.lAux = True
                thread = Thread(target=app._bell('verif'), daemon=True)
                thread.start()
            else:
                app.lAux = False
                app.lAuxx = False
            app._bell('bell')
        else:
            pass
            '''app.labpos = (app.lado/2)-(app.pw/2)
            app.canvas.itemconfigure(app.ldValue, text='')
            app.canvas.itemconfigure(app.rdValue, text='')
            app.canvas.itemconfig(app.ll, fill='white')
            app.canvas.itemconfig(app.lr, fill='white')
            app.canvas.coords(app.lr, app.lado/5, 0.0,
                              app.lado/5, app.cima)
            app.canvas.coords(app.ll, 4*app.lado/5, 0.0,
                              4*app.lado/5, app.cima)
            app.canvas.coords(app.rLabel, 4*app.lado/5, 15)
            app.canvas.coords(app.lLabel, app.lado/5, 15)'''
            '''app.canvas.coords(app.lr, app.lado*1.1, app.lrPos[0][1],
                              app.lado*1.1, app.lrPos[1][1])
            app.canvas.coords(app.ll, app.lado*1.1, app.llPos[0][1],
                              app.lado*1.1, app.llPos[1][1])
            app.canvas.coords(app.lLabel, app.lado*1.1, 15)
            app.canvas.coords(app.rLabel, app.lado*1.1, 15)
            app.canvas.coords(app.ldValue, app.lado*1.1, 15)
            app.canvas.coords(app.rdValue, app.lado*1.1, 15)
            if not app.blinkaux:
                app.blinkaux = True
                app.after(500, app.blinkt)
            app.blinkaux = True
            app.after(0, app.action())'''
        root.update()
    except Exception:
        # print((canrd.release())[1])
        auxx = False
    sleep(.2)
