import tkinter as tk
import math
window = tk.Tk()
frame = tk.Frame()
frame = tk.Frame(window, background="#3297a8")
frame.pack(fill=tk.BOTH, expand=True)
canvas = tk.Canvas(frame, width=300, height=300, background='white')
canvas.pack()
px = 300 * .3
h = px * (math.sqrt(3) / 2)
nx, ny = 300, 0
coords = [[nx - (px/2), ny + h],  # left down
          [nx + (px/2), ny + h],  # right down # noqa: E501
          [nx, ny]]


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


coords = rotate(coords, 45, [300, 0])
canvas.create_polygon(coords, fill='#000000', width=1)  # noqa: E501
window.mainloop()
