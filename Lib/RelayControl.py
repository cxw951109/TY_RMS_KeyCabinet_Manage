from Lib.SerialPort import *
from Lib.crc16 import *
from Lib.Utils import *
import datetime
import time
import os
import threading
import binascii
import re 
import math
class RelayControl(object):
    """8路继电器模块"""

    Case=None

    def __init__(self):
        self.seria = None
        try:
            self.seria = SerialPort('COM3',19200)
            print('8路继电器模块初始化成功')
        except Exception as ex:
            print('8路继电器模块初始化失败：'+ str(ex))
        self.READ_CMD=['01 03 80 40 00 02 EC 1F','02 03 80 40 00 02 EC 2C']

    def doorControl(self,doorIndex,swich):
        addr=str(math.ceil(doorIndex/16))
        if(doorIndex>16):
            doorIndex=doorIndex-16

        caleValue=int(doorIndex-1)
        hexVal = hex(caleValue)[2:].zfill(2)
        sendVal = '0x' + (hexVal) 

        sendComm= ''
        if(swich):
            sendComm = '0x0'+addr+' 0x05 0x00 ' + sendVal  +' 0xff 0x00'
            sendComm = '0'+addr+' 05 00 ' + hexVal +' ff 00 '+ crc16.calculateCRC(sendComm)
        else:
            sendComm = '0x0'+addr+' 0x05 0x00 ' + sendVal  +' 0x00 0x00'
            sendComm = '0'+addr+' 05 00 ' + hexVal +' 00 00 '+ crc16.calculateCRC(sendComm)   
        print(sendComm)
        try:
            self.seria.Write(bytes.fromhex(sendComm.lower()))
        except Exception as e:
            print('error1:',e)
        except OSError as e:
            print('error2:',e)

    def openDoor(self,doorIndex):
        self.doorControl(doorIndex,True)
        time.sleep(0.1)
        self.doorControl(doorIndex,False)
        time.sleep(0.1)
        readValue=self.seria.Read()
        
    def getAllStatus(self):
        status=''
        status+=self.getStatus(1)
        time.sleep(0.1)
        status+=self.getStatus(2)
        status=status[:-2]
        print(status)
        return status

    def getOpenList(self):
        openList=[]
        for index,item in enumerate(self.getAllStatus()):
            if(item=='1'):
                openList.append(index+1)
        
        print(openList)
        return openList

    
    def getStatus(self,index):
        try:
            self.seria.Write(bytes.fromhex(self.READ_CMD[index-1]))
            time.sleep(0.1)
            readValue=self.seria.Read()
            val = str(binascii.b2a_hex(readValue).decode())
            print('111111111_',val)
            yzValue=crc16.calculateCRC(' '.join(['0x'+item  for item in re.findall(r'(.{2})',val[:-4])])).replace(' ','').lower()
            yzValue=yzValue[:2]+yzValue[-2:]
            print(yzValue)
            print(val[-4:])
            if(yzValue==val[-4:]):
                return self.parseResult(val)
            else:
                print('ffffffffdfdfdf')
                return '0000000000000000'
        except Exception as e:
            print('serialRead:',e)
            return '0000000000000000'

    def parseResult(self, data):
        """
        01 02 01 00 88 A1
        6,7 位为八路继电器所有开关状态，转为二进制后制成列表返回
        :param data:
        :return:
        """
        binary_data = bin(int(data[10:14], 16))[2:]
        binary_data=binary_data.zfill(16)
        binary_data=''.join(reversed(binary_data))
        switch_list=[]
        return binary_data
        # for i in binary_data:
        #     switch_list.append(int(i))
        # #print(switch_list)

                    








