import PCANBasic as pcb
import cantools
db = cantools.database.load_file('truck.dbc')
objPCAN = pcb.PCANBasic()
objPCAN.Initialize(pcb.PCAN_USBBUS1, pcb.PCAN_BAUD_666K)
objPCAN.FilterMessages(pcb.PCAN_USBBUS1,
                       218000407, 285147775,
                       pcb.PCAN_MODE_EXTENDED)
while True:
    returned = objPCAN.Read(pcb.PCAN_USBBUS1)
    msg = returned[1]
    if False:  # msg.ID == 285147519:
        msg = db.decode_message(msg.ID, msg.DATA)
        if (msg['DistLaneLineRt_Cval_MPC']
           != 'SNA' and msg['DistLaneLineLt_Cval_MPC'] != 'SNA'):
            right, left = round(float(msg['DistLaneLineRt_Cval_MPC']),
                                4), round(float(msg['DistLaneLineLt_Cval_MPC']
                                                ), 4)
            print(left, right)
    elif False:  # msg.ID == 285147775:
        msg = db.decode_message(msg.ID, msg.DATA)
        cR, cL = msg['ConfLaneRt_Cval_MPC'], msg['ConfLaneLt_Cval_MPC']
        if cR != 'SNA' and cL != 'SNA':
            if 60 <= cL <= 90 and 60 <= cR <= 90:
                print(cL, cR)
    elif msg.ID == 218000407:
        msg = db.decode_message(msg.ID, msg.DATA)
        msg = int(msg['VehSpd_Cval_ICUC'])
        print(msg)
