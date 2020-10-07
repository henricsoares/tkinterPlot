import tkinter as tk  # módulo para animação
from time import sleep  # módulo para utilização do delay
from PIL import ImageTk, Image  # módulo para utilização de imagens
import tkinter.font as font  # módulo para configuração de fontes
import canrd  # API para leitura da porta CAN

root = tk.Tk()  # cria a janela principal
root.attributes('-fullscreen', True)  # configura a janela para fullscreen
frame = tk.Frame(root, background="#3297a8")   # adiciona um frame a janela principal # noqa: F405, E501
frame.pack(fill=tk.BOTH, expand=True)   # configura as dimensões do frame # noqa: E501, F405
my_canvas = tk.Canvas(frame, width=1200, height=600, background='black')  # adiciona um quadro ao frame # noqa: F405, E501
img = Image.open("truck.png")  # define imagem utilizada no veículo
photo = ImageTk.PhotoImage(img)  # configura o objeto de imagem
myFont = font.Font(size=30)  # cria uma configuração de fonte # noqa: E501
title = tk.Label(frame, text='Lane Plotting', background="#3297a8", foreground='white', pady=35)  # cria o título de aplicação # noqa: E501
title['font'] = myFont  # atribui a configuração de fonte ao título
my_canvas.grid(row=0, column=0)  # desabilita linhas e colunas para o quadro
my_canvas.pack(side=tk.BOTTOM)  # carrega e posiciona o quadro no frame
lab = tk.Label(my_canvas, image=photo, background='black')  # cria o widget para carregar a imagem # noqa: E501
lab.place(x=430, y=45)  # posiciona a imagem no quadro
title.pack(side=tk.TOP)  # carrega e posiciona o título no frame
llPos = [[350.0, 0.0], [350.0, 150.0], [350.0, 300.0], [350.0, 450.0], [350.0, 605.0]]  # valores iniciais da faixa esquerda # noqa: E501
lrPos = [[850.0, 0.0], [850.0, 150.0], [850.0, 300.0], [850.0, 450.0], [850.0, 605.0]]  # valores iniciais da faixa diireita # noqa: E501
lr = my_canvas.create_line(lrPos, fill='yellow', width=20)  # cria a faixa esquerda # noqa: E501
ll = my_canvas.create_line(llPos, fill='yellow', width=20)  # cria a faixa direita # noqa: E501
# my_canvas.create_line(600, 0, 600, 600, fill='yellow', width=1)  # linha para calibração da posição da imagem no quadro  # noqa: E501
x1, y1 = 1200, 600  # oculta o veículo
x2, y2 = 430, 45  # posiciona o veículo no ponto de origem


def blinkt():  # função para efeito visual na imagem, indica ausência de faixas/ sinal # noqa: E501
    global x1, x2, y1, y2  # utiliza variaveis criadas anteriormente
    sleep(0.5)  # aguarda 200ms para que o efeito seja visível
    lab.place(x=x1, y=y1)  # altera a posição atual do veículo
    x1, x2 = x2, x1  # inverte as variáveis x1 e x2 simultaneamente
    y1, y2 = y2, y1  # inverte as variáveis y1 e y2 simultaneamente


conection = (canrd.connect())  # tenta conexão com porta CAN
print(conection[1])  # exibe o resultado
conection = conection[0]  # extrai somente a resposta booleana
while not True:  # loop principal
    my_canvas.delete(ll)  # apaga a faixa esquerda anterior
    my_canvas.delete(lr)  # apaga a faixa direita anterior
    data = canrd.canRead(conection)  # efetua leitura da porta CAN se a conexão estiver ok # noqa: E501
    if data[0]:  # Inicia tratamento dos dados se houver sinais de faixas # noqa: E501
        data = data[1]  # armazena somente os sinais de faixas
        # print(data)  # exibe sinais de faixas
        left = data[1]  # atribui o sinal da faixa esquerda a variavel
        right = data[0]  # atribui o sinal da direita esquerda a variavel
        # left = random.uniform(-2.5, -2.25)  # simulação da faixa esquerda
        # right = random.uniform(2.5, 2.25)  # simulação da faixa direita
        if left < 0 and right > 0:  # verifica se as faixas estão posicionadas corretamente  # noqa: E501
            ampl = (abs(left)+right) / 2  # determina a amplitude das faixas
            labpos = ((left+right)*167) + 430  # determina a posição da imagem de acordo com as faixas # noqa: E501
        elif left > 0 and right < 0:  # verifica se as faixas estão posicionadas corretamente  # noqa: E501
            ampl = (abs(right)+left) / 2  # determina a amplitude das faixas
            labpos = ((left+right)*167) + 430  # determina a posição da imagem de acordo com as faixas # noqa: E501
        else:  # caso não estejam posicionadas corretamente
            ampl = 0  # determina amplitude nula
        if ampl < 3.0 and ampl > 1.5:  # and labpos > 30 and labpos < 830:  # atualiza a tela caso a amplitude e a posição da imagem sejam adequadas # noqa: E501
            for i in range(4, 0, -1):  # desloca os valores das listas
                lrPos[i][0] = lrPos[i-1][0]  # faixa direita
                llPos[i][0] = llPos[i-1][0]  # faixa esquerda
            lrPos[0][0] = (ampl * 167) + 600  # atribu o valor medido ao primeiro elemento da lista direita # noqa: E501
            llPos[0][0] = (-ampl * 167) + 600  # atribu o valor medido ao primeiro elemento da lista esquerda # noqa: E501
            lab.place(x=labpos, y=45)  # reposiciona a imagem
            lr = my_canvas.create_line(lrPos, fill='yellow', width=20)  # recria a faixa direita # noqa: E501
            ll = my_canvas.create_line(llPos, fill='yellow', width=20)  # recria a faixa esquerda # noqa: E501
            sleep(.05)  # aguarda 50ms antes de sair do loop
        else:  # caso faixas ou amplitude não estejam ok
            lab.place(x=430, y=45)  # coloca o veículo na posição inicial
    else:  # caso não haja sinais de faixas
        blinkt()  # faz a imagem piscar indicando ausência de sinal adequado # noqa: E501
    root.update()  # atualiza a janela principal

print((canrd.release())[1])  # libera a porta CAN ao final do programa # noqa: E501
