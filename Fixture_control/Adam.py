import serial
import time
from typing import Tuple, List, Dict
import threading
class Adam():
    def __init__(self, port: str, baudrate: int, bytesize:int , stopbits: float, parity: str):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.parity = parity
        self.READBUFLEN = 9
        self.buf = None
        self.lock = threading.Lock()

    def WriteAndReadSerial(self, writebuf: str, buflen: int = 9):
        with self.lock:
            try:
                self.READBUFLEN = buflen
                self.buf = None
                if isinstance(writebuf, str):
                    writebuf = writebuf.encode()
                with serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity,
                                   stopbits=self.stopbits, timeout=1) as ser:
                    ser.write(writebuf)
                    self.buf = ser.read(self.READBUFLEN)
            except Exception as e:
                self.buf = repr(e) + str(e.__traceback__.tb_frame.f_globals['__file__']) + str(e.__traceback__.tb_lineno)


    def GetAdamkValue(self, addr: str) -> float:  # addr --> '#033'
        with self.lock:
            cmd = addr.encode()
            cmd = cmd + b'\x0d\x00'
            value = 99999999
            try:
                with serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity,
                                   stopbits=self.stopbits, timeout=2) as ser:
                    for i in range(5):
                        ser.write(cmd)
                        buf = ser.read(self.READBUFLEN)  # b'>+03.323\r'
                        # print(buf)
                        try:
                            buf = buf.decode()
                            if '>' in buf and '\r' in buf:
                                value = float(buf[1:-1])
                                break
                            else:
                                self.buf = buf
                                print('Get adam value error, buff:', buf)
                        except Exception as e:
                            continue
            except Exception as e:
                self.buf = repr(e) + str(e.__traceback__.tb_frame.f_globals['__file__']) + str(e.__traceback__.tb_lineno)
        return value

if __name__ == '__main__':
    adam = Adam(port='COM6', baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_TWO)
    # value = adam.GetAdamkValue('#030')
    # print(value)

    cmd = ':001r_rgbi01-01\n'

    adam.WriteAndReadSerial(cmd, 20)
    time.sleep(0.5)
    print(adam.buf)


