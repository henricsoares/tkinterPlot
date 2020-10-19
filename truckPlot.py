import tkinter as tk
import random  # noqa: F401
from time import sleep
import keyboard  # noqa: F401
from PIL import ImageTk, Image
import tkinter.font as font
import canrd  # noqa: F401

root = tk.Tk()
root.attributes('-fullscreen', True)
frame = tk.Frame(root, background="#3297a8")   # noqa: F405, E501
frame.pack(fill=tk.BOTH, expand=True)   # noqa: E501, F405
lado, cima = .8*(frame.winfo_screenwidth()), .8*(frame.winfo_screenheight())
my_canvas = tk.Canvas(frame, width=lado, height=cima, background='black')  # noqa: F405, E501
img = Image.open("truck.png")
photo = ImageTk.PhotoImage(img)
pw, ph = photo.width(), photo.height()
propT = pw/ph
pw = .3*lado
ph = pw/propT
img = img.resize((int(pw), int(ph)), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(img)
pw, ph = photo.width(), photo.height()
metro = pw/2
myFont = font.Font(size=30)  # noqa: E501
title = tk.Label(frame, text='Lane Plotting', background="#3297a8", foreground='white')  # noqa: E501
title['font'] = myFont
my_canvas.pack(side=tk.BOTTOM)
lab = tk.Label(my_canvas, image=photo, background='black')  # noqa: E501
lab.place(x=(lado/2)-(pw/2), y=(cima/2)-(ph/2))
title.pack(side=tk.TOP)
llPos = [[lado/5, 0.0], [lado/5, cima/4], [lado/5, 2*cima/4], [lado/5, 3*cima/4], [lado/5, cima]]  # noqa: E501
lrPos = [[4*lado/5, 0.0], [4*lado/5, cima/4], [4*lado/5, 2*cima/4], [4*lado/5, 3*cima/4], [4*lado/5, cima]]  # noqa: E501
lw = .02*lado
lr = my_canvas.create_line(lrPos, fill='yellow', width=lw)  # noqa: E501
ll = my_canvas.create_line(llPos, fill='yellow', width=lw)  # noqa: E501
# my_canvas.create_line(lado/2, 0, lado/2, cima, fill='yellow', width=1)  # noqa: E501
x1, y1 = lado, cima
x2, y2 = (lado/2)-(pw/2), (cima/2)-(ph/2)


def blinkt():  # noqa: E501
    global x1, x2, y1, y2
    sleep(0.5)
    lab.place(x=x1, y=y1)
    x1, x2 = x2, x1
    y1, y2 = y2, y1


'''conection = (canrd.connect())
print(conection[1])
conection = conection[0]'''
aux = True
while not keyboard.is_pressed('q') and aux:
    try:
        my_canvas.delete(ll)
        my_canvas.delete(lr)
        '''data = canrd.canRead(conection)  # noqa: E501'''
        if True:  # data[0]:  # noqa: E501
            '''data = data[1]
            # print(data)
            left = data[1]
            right = data[0]'''
            left = random.uniform(-2, -1.9)  # simulação da faixa esquerda
            right = random.uniform(2, 1.9)  # simulação da faixa direita'''
            if left < 0 and right > 0:
                ampl = (abs(left)+right) / 2
                labpos = ((left+right)*metro) + (lado/2)-(pw/2)  # noqa: E501
            elif left > 0 and right < 0:  # noqa: E501
                ampl = (abs(right)+left) / 2
                labpos = ((left+right)*metro) + (lado/2)-(pw/2)  # noqa: E501
            else:
                ampl = 0
            if ampl < 4.0 and ampl > 1:  # noqa: E501
                for i in range(4, 0, -1):
                    lrPos[i][0] = lrPos[i-1][0]
                    llPos[i][0] = llPos[i-1][0]
                lrPos[0][0] = (ampl * metro) + (lado/2)  # noqa: E501
                llPos[0][0] = (-ampl * metro) + (lado/2)  # noqa: E501
                lab.place(x=labpos, y=(cima/2)-(ph/2))
                lr = my_canvas.create_line(lrPos, fill='yellow', width=lw)  # noqa: E501
                ll = my_canvas.create_line(llPos, fill='yellow', width=lw)  # noqa: E501
                sleep(.1)
            else:
                lab.place(x=(lado/2)-(pw/2), y=(cima/2)-(ph/2))
        else:
            blinkt()  # noqa: E501
        root.update()
    except Exception:
        pass
        aux = False
'''print((canrd.release())[1])  # noqa: E501'''
