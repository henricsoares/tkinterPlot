import tkinter as tk
import math
from time import sleep  # noqa: F401
window = tk.Tk()
frame = tk.Frame(window, background="#3297a8")
frame.pack(fill=tk.BOTH, expand=True)
lado, cima = (frame.winfo_screenwidth())*.2, (frame.winfo_screenheight()*.2)
my_canvas = tk.Canvas(frame, width=lado, height=cima, background='white')
my_canvas.pack(side=tk.BOTTOM)
px = lado * .3
py = px
h = px * (math.sqrt(3) / 2)


def triangle(form):
    if form == 'up':
        coords = [(lado/2) - (px/2), h + px*.05,  # left down
                  (lado/2) + (px/2), h + px*.05,  # right down
                  (lado/2), px*.05,  # top
                  (lado/2) - (px/2), h + px*.05]
    if form == 'right':
        coords = [(lado) - h, (cima/2) - (px/2),
                  (lado) - h, (cima/2) + (px/2),
                  (lado), (cima/2),
                  (lado) - h, (cima/2) - (px/2)]
    if form == 'left':
        coords = [h, (cima/2) + (px/2),
                  h, (cima/2) - (px/2),
                  0, (cima/2),
                  h, (cima/2) + (px/2)]
    id = my_canvas.create_polygon(coords,
                                  outline='black', fill='red', width=px*.05)
    return id


'''tid = triangle('left')
window.update()
for i in range(3):
    print(i)
    sleep(1)
my_canvas.delete(tid)
window.update()
for i in range(3):
    print(i)
    sleep(1)
window.mainloop()'''
print(type('a'))
