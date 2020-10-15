import tkinter as tk

window = tk.Tk()
frame = tk.Frame(window, background="#3297a8")
frame.pack(fill=tk.BOTH, expand=True)
lado, cima = (frame.winfo_screenwidth()), (frame.winfo_screenheight())
my_canvas = tk.Canvas(frame, width=lado, height=cima, background='white')
px, py = lado * .1, cima * .1
my_canvas.create_line((lado/2) - (px/2), (cima/2) + (py/2),
                      (lado/2) + (px/2), (cima/2) + (py/2),
                      (lado/2), (cima/2) - (py/2),
                      (lado/2) - (px/2), (cima/2) + (py/2),
                      fill='black', width=2)
my_canvas.pack(side=tk.BOTTOM)
window.mainloop()
