import tkinter as tk  # módulo para animação
import random  # módulo para números randômicos # noqa: F401
from time import sleep  # módulo para utilização do delay  # noqa: F401
import keyboard  # noqa: F401
import tkinter.font as font  # módulo para configuração de fontes  # noqa: F401
import canrd  # API para leitura da porta CAN  # noqa: F401
import tkinterPlot as tkp
# --------------------------------------------------------------------------------------------------------
janela = tk.Tk()  # cria a janela principal
graph = tkp.tkGraph(janela, 7, 13.5)
ponto = tkp.tkPlot(-5, 5)
while True:
    janela.update()
