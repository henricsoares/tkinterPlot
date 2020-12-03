import cantools
import PCANBasic as pcb
# import keyboard
objPCAN = pcb.PCANBasic()
MPC_C03 = 285147519
MPC_C04 = 285147775
db = cantools.database.load_file('truck.dbc')
db.messages
cL, cR = 0, 0


def connect():
    result = objPCAN.Initialize(pcb.PCAN_USBBUS1, pcb.PCAN_BAUD_666K)

    if result != pcb.PCAN_ERROR_OK:
        result = objPCAN.GetErrorText(result)
        return([False, result[1].decode()])
    else:
        result = objPCAN.GetErrorText(result)
        objPCAN.FilterMessages(pcb.PCAN_USBBUS1,
                               MPC_C03, MPC_C04,
                               pcb.PCAN_MODE_EXTENDED)
        return([True, result[1].decode()])


def release():
    # Release the Channel
    result = objPCAN.Uninitialize(pcb.PCAN_USBBUS1)
    if result != pcb.PCAN_ERROR_OK:
        # An error occurred, get a text describing the error and show it
        result = objPCAN.GetErrorText(result)
        return(False, result[1].decode())
    else:
        return([True, "PCAN-USB (Ch-1) was released"])


def canRead(conection):
    global cL, cR
    count = 0
    if conection:
        aux = True
        while aux:
            returned = objPCAN.Read(pcb.PCAN_USBBUS1)
            if returned[0] == 0:
                msg = returned[1]

                # Verify if desire ID come from PCAN is inside dbc dictionary msg  # noqa: E501
                if msg.ID == MPC_C04:
                    msg = db.decode_message(msg.ID, msg.DATA)
                    cR, cL = msg[
                                 'ConfLaneRt_Cval_MPC'
                                 ], msg['ConfLaneLt_Cval_MPC']
                    if cR == 'SNA' or cL == 'SNA':
                        cR, cL = 0, 0
                elif msg.ID == MPC_C03:

                    # if it is true decode this Data
                    can_port = db.decode_message(msg.ID, msg.DATA)

                    # Second if is used to select desire ID data

                    if(can_port['DistLaneLineLt_Cval_MPC']
                       != 'SNA' and can_port['DistLaneLineRt_Cval_MPC'
                                             ] != 'SNA'
                       and 80 <= cL <= 90 and 80 <= cR <= 90):
                        lanes = [0.0, 0.0]
                        lanes[0] = -can_port['DistLaneLineLt_Cval_MPC']
                        lanes[1] = -can_port['DistLaneLineRt_Cval_MPC']
                        aux = False
                        return([True, lanes])
                    else:
                        return([False, 'SNA'])
            elif returned[0] == 67108864:
                return([False, 'No connection'])
                aux = False
            elif returned[0] == 32:
                count += 1
                if count > 2999:
                    return([False, 'Empty message'])
                    count = 0
                    aux = False
    else:
        return([False, 'No connection'])


'''status = connect()
print(status[1])
auxx = True
while not keyboard.is_pressed('q') and auxx:
    print(canRead(status[0]))

print(release())'''
