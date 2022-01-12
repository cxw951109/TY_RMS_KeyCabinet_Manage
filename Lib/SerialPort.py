import serial  
from time import sleep  
import threading
class SerialPort(object):
    
    def __init__(self,Name,BaudRate):
        # 串口通信同步锁
        self.lockSend=threading.Lock() 
        self.ser = serial.Serial(Name, BaudRate, timeout=0.1)   
       
    def Read(self,readCount=0):
        try:
            self.lockSend.acquire()
            data=None
            while True:    
                #count = self.ser.inWaiting() #获取接收缓存区的字节数
                if(readCount==0):
                    data = self.ser.readall()    
                    if data == None:    
                        continue  
                    else:  
                        break  
                else:
                    data = self.ser.read(readCount)    
                    if data == None:    
                        continue  
                    else:  
                        break  
                sleep(0.002)
                self.ser.flushInput()
            # self.lockSend.release()
            return data
        except Exception as e:
            raise e
        #     self.lockSend.release()
        except OSError as e:
            raise e
        #     self.lockSend.release()  
        finally:
            self.lockSend.release()
         


    def Write(self,data):
        try:
            self.lockSend.acquire()
            #self.ser.flushInput()
            self.ser.write(data)
        #     self.lockSend.release()
        except Exception as e:
            raise e
            #self.lockSend.release()
        except OSError as e:
            raise e
            #self.lockSend.release()
        finally:
            self.lockSend.release()

    def Close(self):
        try:
            self.ser.close()
        except Exception as e:
            print('serialClose:',e)
            


if __name__ == "__main__":
    import SerialPort
    sp = SerialPort.SerialPort('/dev/serial_2',9600)
    while True:
        d = sp.Read()
        print(bytes.decode(d))



