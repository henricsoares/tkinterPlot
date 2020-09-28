import tkinter as tk
'''janela = tk.Tk()
janela.state('zoomed')
# janela.attributes('-fullscreen', True)
frame = tk.Frame(janela, background="#3297a8")
frame.pack(fill=tk.BOTH, expand=True)'''


def canvasG(frame, dY, dX):
    global lado, cima, dx, dy, my_canvas
    dx, dy = dY, dX
    lado, cima = (frame.winfo_screenwidth()), (frame.winfo_screenheight())
    propF = cima/lado
    propG = dy/dx

    if propG <= propF:
        while propG <= propF:
            cima -= 1
            propF = cima/lado

    cima = (0.8 * cima)
    lado = cima / propG
    my_canvas = tk.Canvas(frame, width=lado,
                          height=cima, background='white')
    difLine = 0.05 * cima
    a, b, c, d = [difLine, difLine], [lado - difLine, difLine], [lado - difLine, cima - difLine], [difLine, cima - difLine]  # noqa: E501
    my_canvas.create_line(a, b, c, d, a, fill='black', width=2)
    stepX = (b[0] - a[0]) / 5
    stepY = (d[1] - a[1]) / 5
    for i in range(0, 6, 1):
        my_canvas.create_line(difLine + (i * stepX), d[1], difLine + (i * stepX), d[1] + (difLine / 2), fill='black', width=2)  # noqa: E501
        my_canvas.create_line(a[0], difLine + (i * stepY), a[0] - (difLine / 2), difLine + (i * stepY), fill='black', width=2)  # noqa: E501
        xLabel = round((dx/5) * i, 2)
        my_canvas.create_text(difLine + (i * stepX), d[1] + (0.7 * difLine), fill="black", font="Arial 8 bold", text=xLabel)  # noqa: E501
        yLabel = round((dy - ((dy/5) * i)), 2)
        my_canvas.create_text(a[0] - (0.5 * difLine), (difLine / 2) + (i * stepY), fill="black", font="Arial 8 bold", text=yLabel)  # noqa: E501
    return my_canvas


def canvasP(x, y):
    if (x <= dx and y <= dy):
        propY = cima / dy
        propX = lado / dx
        # print(cima, propY)
        nx = x * propX
        ny = y * propY
        # print(nx, ny)
        id = my_canvas.create_oval(nx, ny, nx + 15, ny + 15, fill='red',
                                   width=0)
        return id
    else:
        print("object out of range")


'''my_canvas = canvasG(5, 5)
canvasP(2.5, 2.5)
my_canvas.pack(side=tk.BOTTOM)
janela.mainloop()'''
