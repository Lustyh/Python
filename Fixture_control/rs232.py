import serial
import time
import json
import re
from datetime import datetime
from threading import Lock

class serial_port():
  def __init__(self, baudrate, fixture_port):
    self.serial_lock = Lock()
    self.baudrate = baudrate
    self.port = fixture_port
    self.connect()

  def connect(self):
    try:
      self.port = serial.Serial(
      port=self.port,
      baudrate=self.baudrate,
      timeout=1
      )
      self.cmds = []
    except Exception as e:
      print(e)
      raise e

  def disconnect(self):
    while True:
      try:
        self.port.close()
        break
      except:
        continue

  def Fixture_Movement(self,command):
    if 'TEST_START' in command:
      return self.exec_cmd(command,'TEST_START_OK')
    if 'TEST_END' in command:
      return self.exec_cmd(command,'TEST_END_OK')

  def OS_Test(self,command):
    return self.Measure_exec(command,",",20)  

  def exec_cmd(self, command, expect: str = '', timeout=4):
    self.serial_lock.acquire()
    self.clean()
    cmd = command.encode("ascii")
    self.port.write(cmd)
    tmp = ""
    start_time = time.time()
    while time.time() - start_time < timeout:
      time.sleep(.001)
      try:
        # print(self.port.read())
        tmp+=self.port.read().decode('utf-8',errors='replace')
        if expect in tmp:
          break
      except Exception as e:
        tmp+=str(e)
    self.serial_lock.release()
    # encodings = ['utf-8', 'ascii', 'latin-1']
    return tmp

  def mea_curr_vol(self, command, expect: str = '', timeout=4):
    # expect to do the match,
    self.serial_lock.acquire()
    self.clean()
    if command != 'test':
      cmd = command.encode("ascii")
      self.port.write(cmd)
      tmp = ""
      start_time = time.time()
      while time.time() - start_time < timeout:
        time.sleep(.001)
        try:
          # print(self.port.read())
          tmp+=self.port.read().decode('utf-8',errors='replace')
          matches = re.search(expect,tmp)
          if matches:
            break
        except Exception as e:
          tmp+=str(e)
    else:
      tmp = "V_SCAP:2.33V"
      matches = re.search(expect,tmp)
      if matches:
        print(matches.group(0))
    self.serial_lock.release()
    # encodings = ['utf-8', 'ascii', 'latin-1']
    return tmp

  def Measure_exec(self, command, expect: str = '', timeout=4):
    self.serial_lock.acquire()
    self.clean()
    cmd = command.encode("ascii")
    self.port.write(cmd)
    tmp = ""
    start_time = time.time()
    while time.time() - start_time < timeout:
      time.sleep(.001)
      try:
        # print(self.port.read())
        tmp+=self.port.read().decode('utf-8',errors='replace')
        if tmp.count(expect) == 14:
          break
      except Exception as e:
        tmp+=str(e)
    self.serial_lock.release()
    # encodings = ['utf-8', 'ascii', 'latin-1']
    return tmp

  def clean(self):
    if self.port == None:
      return
    self.port.cancel_read()
    self.port.reset_input_buffer()
    self.port.cancel_write()
    self.port.reset_output_buffer()
    time.sleep(0.001)


if __name__ == "__main__":
  fixture_fwt = serial_port('25600','COM3')
  print(fixture_fwt)
  # checkstring = 'V'
  # output = fixture_fwt.mea_curr_vol('test',':(\d+(\.\d+)?)'+checkstring)
  # print(output)
  # if 'OK' in output.upper():
  #   print('OPEN OK')
  output = fixture_fwt.exec_cmd('CLOSE\r\n')
  print(output)
  output = fixture_fwt.exec_cmd('OPEN\r\n')
  print(output)
  # if 'READY' in output.upper():
  #   print('CLOSE OK')
