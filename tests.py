import tkinter as tk
from PIL import ImageTk, Image
import tkinter.font as font

root = tk.Tk()
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
metro = (pw/2)*1.0024465
myFont = font.Font(size=30)  # noqa: E501
title = tk.Label(frame, text='Lane Plotting', background="#3297a8", foreground='white')  # noqa: E501
title['font'] = myFont
my_canvas.pack(side=tk.BOTTOM)
lab = tk.Label(my_canvas, image=photo, background='black')  # noqa: E501
lab.place(x=(lado/2)-(pw/2), y=(cima/2)-(ph/2))
title.pack(side=tk.TOP)
llPos = [[lado/5, 0.0], [lado/5, cima]]  # noqa: E501
lrPos = [[4*lado/5, 0.0], [4*lado/5, cima]]  # noqa: E501
lw = .02*lado
lr = my_canvas.create_line(lrPos, fill='yellow', width=lw)  # noqa: E501
ll = my_canvas.create_line(llPos, fill='yellow', width=lw)  # noqa: E501
# my_canvas.create_line((lado/2)-metro, 0, (lado/2)-metro, cima, fill='yellow', width=1)  # noqa: E501
aux = True
while aux:
    try:
        left = int(input("Left: "))
        right = int(input("Right: "))
        if left < 0 and right > 0:
            ampl = (abs(left)+right) / 2
            labpos = ((ampl - right)*metro) + (lado/2)-(pw/2)  # noqa: E501
        elif left > 0 and right < 0:
            ampl = (abs(right)+left) / 2
            labpos = ((ampl - left)*metro) + (lado/2)-(pw/2)  # noqa: E501
        elif left > 0 and right > 0:
            if right >= left:
                ampl = (right - left) / 2
                labpos = ((ampl - right)*metro) + (lado/2)-(pw/2)
            else:
                ampl = (left - right) / 2
                labpos = ((-ampl - right)*metro) + (lado/2)-(pw/2)
        elif left < 0 and right < 0:
            if left <= right:
                ampl = (abs(left) - abs(right)) / 2
                labpos = ((ampl - right)*metro) + (lado/2)-(pw/2)
            else:
                ampl = (abs(right) - abs(left)) / 2
                labpos = ((-ampl - right)*metro) + (lado/2)-(pw/2)
        llPos[0][0] = (-ampl * metro) + (lado/2)  # noqa: E501
        llPos[1][0] = (-ampl * metro) + (lado/2)  # noqa: E501
        lrPos[0][0] = (ampl * metro) + (lado/2)  # noqa: E501
        lrPos[1][0] = (ampl * metro) + (lado/2)  # noqa: E501
        my_canvas.coords(lr, lrPos[0][0], lrPos[0][1], lrPos[1][0], lrPos[1][1])  # noqa: E501
        my_canvas.coords(ll, llPos[0][0], llPos[0][1], llPos[1][0], llPos[1][1])  # noqa: E501
        lab.place(x=labpos, y=(cima/2)-(ph/2))
        root.update()
    except Exception:
        aux = False
# root.mainloop()
