import tkinter as tk  # módulo para animação
import random  # módulo para números randômicos # noqa: F401
from time import sleep  # módulo para utilização do delay  # noqa: F401
import keyboard  # noqa: F401
import tkinter.font as font  # módulo para configuração de fontes  # noqa: F401
import canrd  # API para leitura da porta CAN  # noqa: F401
import tkinterPlot as tkp
# --------------------------------------------------------------------------------------------------------
janela = tk.Tk()  # cria a janela principal
janela.state('zoomed')
# root.attributes('-fullscreen', True)  # configura a janela para fullscreen
frame = tk.Frame(janela, background="#3297a8")   # adiciona um frame a janela principal # noqa: F405, E501
frame.pack(fill=tk.BOTH, expand=True)   # configura as dimensões do frame # noqa: E501, F405
my_canvas = tkp.canvasG(frame, 5, 5)
ponto = tkp.canvasP(2.5, 2.5)
my_canvas.pack(side=tk.BOTTOM)
while not keyboard.is_pressed('q'):
    xx = random.uniform(287, 289)
    yy = random.uniform(287, 289)
    my_canvas.coords(ponto, xx, yy, xx+15, yy+15)
    janela.update()
