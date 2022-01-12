
#! /usr/bin/python 
# _*_ coding: utf-8 _*_ 
 
""" 
简单的CRC16计算示例： 
    CRC16校验码计算方法如下： 
    1、初始化CRC值为0xFFFF 
    2、被检验数的第1字节跟CRC的低8位异或，将结果放入CRC的低8位（CRC的高8位不变） 
    3、CRC右移1位，若移出的为0继续右移;为1CRC寄存器跟生成多项式（倒序后的值）异或（X16+X15+X2+1 <--> 0x8005 >>> 0xA0001) 
    4、重复步骤3,8次第1字字数据处理完成 
    5、取被检验数据的下1字节，进行2、3、4步;至到整个数据检验完成 
    6、将最后的CRC值,高低字节交换 
"""
import re
import time
class crc16(object):
    # CRC16生成多项式：X16+X15+X2+1 
    GENERATOR_POLYNOMIAL = 0x8005 
    # CRC初始值为：0xFFFF 
    CRC = 0xFFFF 
    def calculateCRC(dataarray): 
        """ 
        检查输入数据是否合法 
        :param dataarray: 需要生成CRC校验的数据 
        :return: 合法的数据元组 
        """ 

        datalist = None   #以空格分割字符串得到对应字符串列表 
        #print(u'输入的字符串序列：{0}'.format(datalist)) 
        if(dataarray is bytes):
            datalist=dataarray
        else:
            datalist = dataarray.split() 
 
        index = 0 
        try: 
            # 将输入的字符串按不同进制数转化为数据序列 
            for index, item in enumerate(datalist): 
                # print index,item 
                if '0x'in item.lower().strip(): 
                    datalist[index] = int(item, 16) 
                elif '0o' in item.lower().strip(): 
                    datalist[index] = int(item,8) 
                elif '0b' in item.lower().strip(): 
                    datalist[index] = int(item,2) 
                else: 
                    datalist[index] = int(item) 
            #print (u'成功转换后的对应的序列：{0}'.format(datalist)) 
            # 处理第1个字节数据 
            temp = crc16.calculateonebyte(datalist.pop(0), 0xFFFF) 
            # 循环处理其它字节数据 
            for data in datalist: 
                temp = crc16.calculateonebyte(data,temp) 
            newValue=str(hex(temp))
            newValue='0x'+newValue[2:].zfill(4)
            newValue=newValue[4:].zfill(2)+' '+newValue[2:4].zfill(2)
            return newValue.upper()
  
        except ValueError as err: 
            print(u'第{0}个数据{1}输入有误'.format(index,datalist[index]).encode('utf-8')) 
            print(err) 
        # finally: 
        #     print('当前datalist:{0} '.format(datalist)) 
    def calculateonebyte(databyte, tempcrc): 
        """ 
        计算1字节数据的CRC值 
        :param databyte: 需计算的字节数据 
        :param tempcrc: 当前的CRC值 
        :return: 当道新的CRC值 
        """ 
        # databyte必须为字节数据 
        # assert 0x00 <= databyte <= 0xFF 
        # 同上字节数据检查 
        if not 0x00 <= databyte <= 0xFF: 
            raise Exception((u'数据：0x{0:<02X}不是字节数据[0x00-0xFF]'.format(databyte)).encode('utf-8')) 
 
        # 把字节数据根CRC当前值的低8位相异或   
        low_byte = (databyte ^ tempcrc) & 0x00FF 
        # 当前CRC的高8位值不变 
        resultCRC = (tempcrc & 0xFF00) | low_byte 
 
        # 循环计算8位数据 
        for index in range(8): 
            # 若最低为1：CRC当前值跟生成多项式异或;为0继续 
            if resultCRC & 0x0001 == 1: 
                #print("[%d]: 0x%4X ^^^^ 0x%4X" % (index,resultCRC>>1,resultCRC^GENERATOR_POLYNOMIAL)) 
                resultCRC >>= 1 
                resultCRC ^= 0xA001 # 0xA001是0x8005循环右移16位的值 
            else: 
                # print ("[{0}]: 0x{1:X} >>>> 0x{2:X}".format(index,resultCRC,resultCRC>>1)) 
                resultCRC >>= 1 
 
    
        return resultCRC 
    def setTem(temValue):
        hexVal = hex(temValue)
        sendVal = ('0x' + hexVal[2:4] + ' 0x' + hexVal[4:])
        sendComm = '0x01 0x06 0x00 0x00 ' + sendVal
        sendComm = '01 06 00 00 ' + (hexVal[2:4]).upper() + ' ' + (hexVal[4:]).upper() +' '+ crc16.calculateCRC(sendComm)
        return sendComm
 
 
if __name__ == '__main__': 
    data_string = ' '.join(['0x'+item  for item in re.findall(r'(.{2})',"0103080c110c1c60000002")])  #以16进制,10进制,8进制输入的数据流 
    hexVal =hex(7600)
    hexVal=('0x'+hexVal[2:4]+' 0x'+hexVal[4:])
    sendComm = '0x01 0x06 0x00 0x00 ' + hexVal
    sendComm = crc16.calculateCRC(sendComm)
    print(crc16.setTem(7600))
    print(crc16.calculateCRC(data_string).replace(' ','')) 
    ddd='0106 0000 1D4C 816F'
    print(int('8903',16))
    print(ddd[12:14]+ddd[10:12])
    
    gg='0103080c110c1c60000002da4c'
    
    print(crc16.calculateCRC(' '.join(['0x'+item  for item in re.findall(r'(.{2})',gg[:-4])])).replace(' ','').lower()==gg[-4:])

    print(gg[-4:]);

    d=None
    print(d!=None and d>=75)

    ff=73

    gg=75.10

    print(gg!=None and gg>=ff)

    t = time.time()
    sjc = (int(t)) * 1000

    print(sjc)
    print(hex(-8000))
    print(hex(65536-8000))
