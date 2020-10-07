import cantools
import PCANBasic as pcb
import keyboard  # noqa: F401

# config can
objPCAN = pcb.PCANBasic()
db = cantools.database.load_file('car.dbc')

# qtdObj = int(input("Quantidade de objetos (máx. 32): "))
# qtdObj = 1
idsA = [1285, ]

X = [0.0]
Y = [0.0]


def connect(qtdObj):
    global X, Y
    for i in range(qtdObj - 1):
        idsA.append(idsA[i]+10)
    X = X * qtdObj
    Y = Y * qtdObj

    result = objPCAN.Initialize(pcb.PCAN_USBBUS1, pcb.PCAN_BAUD_500K)

    if result != pcb.PCAN_ERROR_OK:
        result = objPCAN.GetErrorText(result)
        return([False, result[1].decode()])
    else:
        result = objPCAN.GetErrorText(result)
        return([True, result[1].decode()])


def release():
    # Release the Channel
    result = objPCAN.Uninitialize(pcb.PCAN_USBBUS1)
    if result != pcb.PCAN_ERROR_OK:
        # An error occurred, get a text describing the error and show it
        result = objPCAN.GetErrorText(result)
        return(False, result[1].decode())
    else:
        result = objPCAN.GetErrorText(result)
        return([True, result[1].decode()])


def read(conection):
    count = 0
    if conection:
        aux = True
        while aux:
            returned = objPCAN.Read(pcb.PCAN_USBBUS1)

            if returned[0] == pcb.PCAN_ERROR_OK:
                msg = returned[1]

                if msg.ID in idsA:
                    can_read_A = db.decode_message(msg.ID, b''+msg.DATA)
                    xread = can_read_A[f'Radar1_Obj{int(idsA.index(msg.ID)):02d}_dx']  # noqa: E501
                    yread = -can_read_A[f'Radar1_Obj{int(idsA.index(msg.ID)):02d}_dy']  # noqa: E501
                    if abs(yread) != 0.0:
                        X[idsA.index(msg.ID)] = yread
                        Y[idsA.index(msg.ID)] = xread
                        # print(X, Y)
                        return([True, X, Y])
                        aux = False
            elif returned[0] == 32:
                count += 1
                if count > 99999:
                    return([False, 'Empty message'])
                    aux = False
    else:
        return([False, 'No connection'])


'''status = connect(5)
print(status[1])
print(read(status[0]))'''
'''while not keyboard.is_pressed('q'):
    print(read(status[0]))
    # print(objPCAN.Read(pcb.PCAN_USBBUS1))'''

'''print(release())'''
