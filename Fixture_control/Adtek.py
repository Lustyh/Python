import serial


class Adtek():
    def __init__(self, port, baudrate, bytesize, stopbits, parity):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.parity = parity
        self._METER_READ_COMMAND = b'\x03'
        self._METER_WRITE_COMMAND = b'\x06'
        self.CMD_ADDR_RELAY_STATUS = b'\x00\x05'
        self.CMD_ADDR_RELAY_DSTATUS = b'\x00\x22'
        self.READBUFLEN = 13
        self.buf = None

    def WriteAndReadSerial(self, writebuf, readlen):
        self.buf = None
        with serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity,
                           stopbits=self.stopbits, timeout=0.5) as ser:
            ser.write(writebuf)
            self.buf = ser.read(self.READBUFLEN)

    def CRC16(self, bBuf, dataLen):
        CRC = 0xffff
        SLSB = 0
        for i in range(dataLen):
            CRC = CRC ^ bBuf[i]
            for j in range(8):
                SLSB = CRC & 0x0001
                CRC = CRC >> 1
                if (SLSB != 0):
                    CRC = CRC ^ 0xa001
        return CRC



    def GetAdtekValue(self, addr): #addr --> '0x02'
        # Voltage = b'\x02\x03\x00\x00\x00\x04'
        cmd1 = bytes.fromhex(addr[2:4])  # Adtek Meter Address 0x0x--> b'\x02'
        cmd2 = self._METER_READ_COMMAND  # Read command
        cmd3 = b'\x00'  # Starting Address High
        cmd4 = b'\x00'  # Starting Address Low
        cmd5 = b'\x00'  # Number of Word High
        cmd6 = b'\x04'  # Number of Word Low
        cmd = cmd1 + cmd2 + cmd3 + cmd4 + cmd5 + cmd6
        CRC = self.CRC16(cmd, 6)
        cmd7 = CRC.to_bytes(2, byteorder='little', signed=False)
        cmd = cmd + cmd7
        with serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity,
                           stopbits=self.stopbits, timeout=2) as ser:
            ser.write(cmd)
            buf = ser.read(self.READBUFLEN)
            # print(buf)
        dis1Val = 99999
        dis2Val = 99999
        if (buf[0] == 0x02 and buf[1] == 0x03 and buf[2] == 0x08):
            dis1Val = (buf[5] << 8) | buf[6] & 0xff
            dis2Val = (buf[9] << 8) | buf[10] & 0xff
            # print(dis1Val)
            # print(dis2Val)
            if not dis1Val < 0x8000:
                # dis1Val = ~dis1Val + 1
                dis1Val = dis1Val - 65536
            dis1Val = dis1Val / 1000

            if not dis2Val < 0x8000:
                # dis2Val = ~dis2Val + 1
                dis2Val = dis2Val - 65536
            dis2Val = dis2Val / 10000
            # print(dis1Val)
            # print(dis2Val)
        else:
            print('Get adtek value error, buff:', buf)
        return (dis1Val, dis2Val)

    def GetAdtekRelayStatus(self, addr, meterType):
        cmdAddr = bytes.fromhex(addr[2:4])
        cmdFunc = self._METER_READ_COMMAND  # Read command
        if meterType == 'S':
            cmdStartAddr = self.CMD_ADDR_RELAY_STATUS
        else: # meterType == 'D'
            cmdStartAddr = self.CMD_ADDR_RELAY_DSTATUS
        cmdNOOFWord = b'\x00\x01'
        tmp = cmdAddr + cmdFunc + cmdStartAddr + cmdNOOFWord
        crc = self.CRC16(tmp, 6)
        cmdCRC = crc.to_bytes(2, byteorder='little', signed=False)
        cmd = tmp + cmdCRC
        self.WriteAndReadSerial(cmd, 7)
        bStatus = None
        if len(self.buf) >= 7:
            if self.buf[0:1]==cmdAddr and self.buf[1:2]==cmdFunc:
                bStatus = self.buf[4]
        return bStatus



    def SetAdtekRelay(self, meterType, addr, relay, status):
        # meterType='D'/'S' addr = '0x02' relay = '1/2/3/4'-->b'\x01'/b'\x02'/b'x04'/b'x08' status='ON/OFF'
        ucRelNo = {'1':b'\x01', '2':b'\x02', '3':b'\x04', '4':b'\x08'}
        for i in range(10):
            rlstatus = self.GetAdtekRelayStatus(addr, meterType)
            if rlstatus != None:
                break
        if rlstatus == None:
            return False
        if status == 'ON':
            x  =ord(ucRelNo[relay])
            rlstatus = (rlstatus) | ord(ucRelNo[relay])
        elif status == 'OFF':
            rlstatus = (rlstatus) & (~ord(ucRelNo[relay]))
        # cmd
        cmdAddr = bytes.fromhex(addr[2:4])
        cmdFunc = self._METER_WRITE_COMMAND
        if meterType == 'S':
            cmdStartAddr = self.CMD_ADDR_RELAY_STATUS
        else:  # meterType == 'D'
            cmdStartAddr = self.CMD_ADDR_RELAY_DSTATUS
        cmdData = rlstatus.to_bytes(2, byteorder='big', signed=False)
        tmp = cmdAddr + cmdFunc + cmdStartAddr + cmdData
        crc = self.CRC16(tmp, 6)
        cmdCRC = crc.to_bytes(2, byteorder='little', signed=False)
        cmd = tmp + cmdCRC

        for i in range(10):
            self.WriteAndReadSerial(cmd, 7)
            # CRC = self.CRC16(self.buf, 6)
            newStatus = self.GetAdtekRelayStatus(addr, meterType)
            res = newStatus == cmdData[1]
            if res:
                break
        return res

if __name__ == '__main__':
    adtek = Adtek(port='COM5', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_TWO)
    # adtek.SetAdtekRelay('D', '0x02', '1', 'ON')
    # adtek.SetAdtekRelay('D', '0x02', '2', 'ON')
    # values = adtek.GetAdtekValue('0x02')
    # print(values)
    RES = adtek.SetAdtekRelay('D', '0x02', '1', 'OFF')
    print(RES)
    # adtek.SetAdtekRelay('D', '0x02', '2', 'OFF')