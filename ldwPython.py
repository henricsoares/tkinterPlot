import tkinter as tk
from PIL import ImageTk, Image
import tkinter.font as font
import random  # noqa: F401
from time import sleep
import keyboard  # noqa: F401
import canReadCamera as canrd


class App(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.winfo_toplevel().title("Python LDW")
        self.rAux = False
        self.lAux = False
        self.frame = tk.Frame(root, background="#3297a8")   # noqa: F405, E501
        self.frame.pack(fill=tk.BOTH, expand=True)   # noqa: E501, F405
        self.lado, self.cima = .8*(self.frame.winfo_screenwidth()), .8*(self.frame.winfo_screenheight())  # noqa: E501
        self.canvas = tk.Canvas(self.frame, width=self.lado, height=self.cima, background='black')  # noqa: F405, E501
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
        self.title = tk.Label(self.frame, text='LDW', background="#3297a8", foreground='white')  # noqa: E501
        self.title['font'] = font.Font(size=30)
        self.canvas.pack(side=tk.BOTTOM)
        self.lab = tk.Label(self.canvas, image=self.photo, background='black')  # noqa: E501
        self.labpos = (self.lado/2)-(self.pw/2)
        self.lab.place(x=self.labpos, y=(self.cima/2)-(self.ph/2))
        self.title.pack(side=tk.TOP)
        self.llPos = [[self.lado/5, 0.0], [self.lado/5, self.cima]]  # noqa: E501
        self.lrPos = [[4*self.lado/5, 0.0], [4*self.lado/5, self.cima]]  # noqa: E501
        self.lw = .02*self.lado
        self.lr = self.canvas.create_line(self.lrPos, fill='yellow', width=self.lw)  # noqa: E501
        self.ll = self.canvas.create_line(self.llPos, fill='yellow', width=self.lw)  # noqa: E501
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
                                               15, text=self.left,
                                               fill='yellow',
                                               font=font.Font(size=int(self.lw),  # noqa: E501
                                               weight='bold'))
        self.rdValue = self.canvas.create_text((self.lrPos[0][0])+(.05*self.lado),  # noqa: E501
                                               15, text=self.right,
                                               fill='yellow',
                                               font=font.Font(size=int(self.lw),  # noqa: E501
                                               weight='bold'))
        self.x1, self.y1 = self.lado, self.cima
        self.x2, self.y2 = (self.lado/2)-(self.pw/2), (self.cima/2)-(self.ph/2)
        # canvas.create_line((lado/2)-metro, 0, (lado/2)-metro, cima, fill='yellow', width=1)  # noqa: E501

    def _bell(self):
        # print('_bell')
        if self.lAux or self.rAux:
            self.canvas.bell()

    def blinkt(self):
        sleep(0.5)
        self.lab.place(x=self.x1, y=self.y1)
        self.x1, self.x2 = self.x2, self.x1
        self.y1, self.y2 = self.y2, self.y1


root = tk.Tk()
app = App(root)
auxx = True
conection = (canrd.connect())
print(conection[1])
conection = conection[0]
while auxx:
    try:
        data = canrd.canRead(conection)
        '''left = float(input("Left: "))
        right = float(input("Right: "))'
        app.left = round(random.uniform(-2, -1.5), 2)
        app.right = round(random.uniform(1.5, 2), 2)'''
        if data[0]:
            app.canvas.itemconfigure(app.ldValue, text=app.left)
            app.canvas.itemconfigure(app.rdValue, text=app.right)
            if app.left < 0 < app.right:
                ampl = (abs(app.left)+app.right) / 2
                app.labpos = ((ampl - app.right)*app.metro) + (app.lado/2)-(app.pw/2)  # noqa: E501
                app.left, app.right = -ampl*app.metro+(app.lado/2), ampl*app.metro+(app.lado/2)  # noqa: E501
            elif app.left > 0 > app.right:
                ampl = (abs(app.right)+app.left) / 2
                app.labpos = ((ampl - app.left)*app.metro) + (app.lado/2)-(app.pw/2)  # noqa: E501
                app.right, app.left = -ampl*app.metro+(app.lado/2), ampl*app.metro+(app.lado/2)  # noqa: E501
            elif app.left > 0 < app.right:
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
                    app.right, app.left = -ampl*app.metro+(app.lado/2), ampl*app.metro+(app.lado/2)  # noqa: E501

            app.left, app.right = -ampl*app.metro+(app.lado/2), ampl*app.metro+(app.lado/2)  # noqa: E501
            app.llPos[0][0] = app.left  # noqa: E501
            app.llPos[1][0] = app.left  # noqa: E501
            app.lrPos[0][0] = app.right  # noqa: E501
            app.lrPos[1][0] = app.right  # noqa: E501
            app.canvas.coords(app.lr, app.lrPos[0][0], app.lrPos[0][1], app.lrPos[1][0], app.lrPos[1][1])  # noqa: E501
            app.canvas.coords(app.ll, app.llPos[0][0], app.llPos[0][1], app.llPos[1][0], app.llPos[1][1])  # noqa: E501
            '''if keyboard.is_pressed('a'):
                for i in range(50):
                    app.lab.place(x=app.labpos-i,
                                    y=(app.cima/2)-(app.ph/2))
                    root.update()
                    sleep(.0001)
                app.labpos -= 50
            elif keyboard.is_pressed('d'):
                for i in range(50):
                    app.lab.place(x=app.labpos+i,
                                    y=(app.cima/2)-(app.ph/2))
                    root.update()
                    sleep(.0001)
                app.labpos += 50'''
            if (app.right - app.pw*1.05) < app.labpos < (app.pw*.05 + app.right):  # noqa: E501
                app.canvas.itemconfig(app.lr, fill='red')
                app.rAux = True
                root.after(500, app._bell)
            else:
                app.rAux = False
                app.canvas.itemconfig(app.lr, fill='yellow')
            if (app.left - app.pw*1.05) < app.labpos < (app.pw*.05 + app.left):  # noqa: E501
                app.canvas.itemconfig(app.ll, fill='red')
                app.lAux = True
                root.after(500, app._bell)
            else:
                app.lAux = False
                app.canvas.itemconfig(app.ll, fill='yellow')
            app.canvas.coords(app.lLabel, app.llPos[0][0], 15)
            app.canvas.coords(app.rLabel, app.lrPos[0][0], 15)
            app.canvas.coords(app.ldValue, app.llPos[0][0]+(.05*app.lado),
                              15)
            app.canvas.coords(app.rdValue, app.lrPos[0][0]+(.05*app.lado),
                              15)
            app.lab.place(x=app.labpos, y=(app.cima/2)-(app.ph/2))
        else:
            app.blinkt()
        root.update()
    except Exception:
        print((canrd.release())[1])
        auxx = False
    # sleep(.2)
