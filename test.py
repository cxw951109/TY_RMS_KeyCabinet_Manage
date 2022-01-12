# f={}
# f['dddd']=666666

# f.update(gg=5555)
# print(f)
from Lib.crc16 import *
from Lib.Utils import *
from Lib.RelayControl import *

# def openDoor(doorIndex):
#     caleValue=int(doorIndex-1)
#     hexVal = hex(caleValue)[2:].zfill(2)
#     sendVal = '0x' + (hexVal) 
#     #print(sendVal)
#     sendComm = '0x01 0x05 0x00 ' + sendVal  +' 0x00 0x00'
#     sendComm = '01 05 00 ' + hexVal +' 00 00 '+ crc16.calculateCRC(sendComm)
#     print(sendComm.lower())

# openDoor(5)
relayControl=RelayControl()
relayControl.openDoor(30)
relayControl.getOpenList()