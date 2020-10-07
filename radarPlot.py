import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random  # noqa: F401
import canReadRadar as crr
connection = False


def plot(qtdObj, connection):
    plt.style.use('fast')
    fig = plt.figure()
    ax = plt.subplot()
    '''X = [0.0]*qtdObj
    Y = [0.0]*qtdObj

    for i in range(qtdObj):
        X[i] = (random.uniform(-50.0, 50.0))
        Y[i] = (random.uniform(0, 75.0))'''

    def animate(i):
        '''for j in range(qtdObj):
            X[j] = random.uniform(X[j]-0.5, X[j]+0.5)
            Y[j] = random.uniform(Y[j]-0.5, Y[j]+0.5)'''
        if connection:
            try:
                data = crr.read(connection)
                X, Y = data[1], data[2]

                plt.cla()
                ax.set(xlim=(-55, 55), ylim=(0, 80))
                for j in range(qtdObj):
                    ax.set_title('Simulation')
                    ax.set_xlabel('Lateral Distance from Radar (m)')
                    ax.set_ylabel('Longitudinal Distance from Radar (m)')
                    ax.plot(X[j], Y[j], marker='o', label='Obj')
                    plt.tight_layout()

                    # plt.legend(loc='upper left')
            except Exception:
                print('Erro na leitura')
        else:
            print('There is no connection')
    ani = FuncAnimation(fig, animate,  # noqa: F841
                        interval=5, cache_frame_data=False)
    plt.tight_layout()
    plt.show()


'''print((crr.connect(1))[1])'''
qtdObj = int(input('Num. of objects (max. 32): '))
connect = crr.connect(qtdObj)
if True:  # connect[0]:
    connection = connect[0]
    plot(qtdObj, connection)
else:
    print(connect[1])
'''print(crr.read(True))
print((crr.release())[1])'''
