from micropython import const
from math import ceil
import sys

currentBoard=""
if(sys.platform == "esp8266"):
  currentBoard = "esp8266"
elif(sys.platform == "esp32"):
  currentBoard = "esp32"
elif(sys.platform=="pyboard"):
  currentBoard="pyboard"
  import pyb 
M1        = const(0)
M2        = const(1)
M3        = const(2)
M4        = const(3)
SA        = const(0)
SB        = const(1)
CW        = const(0)
CCW       = const(1)
A0        = const(0x30>>1)
A1        = const(0x38>>1)
A2        = const(0x3C>>1)
A3        = const(0x3E>>1)

motorState={'motor1':0, 'motor2':0, 'motor3':0, 'motor4':0, 'stepperA':0,\
            'stepperB':0, 'BeginA0':0, 'BeginA1':0, 'BeginA2':0, 'BeginA3':0}

class DFRobot_MotorStepper:
  def __init__(self, i2c, addr):
    self.i2c = i2c
    self.addr = addr
  def Write_Motor(self, addr, Reg, buf):
    if currentBoard=="esp8266" or currentBoard=="esp32":
      self.i2c.writeto_mem(addr,Reg,buf)
  def Read_Motor(self, addr, Reg, num): 
    _redbuf=bytearray(2) 
    if currentBoard=="esp8266" or currentBoard=="esp32":
      _redbuf = self.i2c.readfrom_mem(addr ,Reg, num)
    return _redbuf
  def begin(self, addr):
    writebuf = bytearray("ok")
    redbuf = bytearray(2)
    if(addr == A0):
      if(motorState['BeginA0']):
        return
      else:
        motorState['BeginA0']=1
        print("----A0----")
    elif(addr == A1):
      if(motorState['BeginA1']):
        return
      else:
        motorState['BeginA1']=1
        print("----A1----")
    elif(addr == A2):
      if(motorState['BeginA2']):
        return
      else:
        motorState['BeginA2']=1
        print("----A2----")
    elif(addr == A3):
      if(motorState['BeginA3']):
        return
      else:
        motorState['BeginA3']=1
        print("----A3----")
    else:
      return
    redbuf = self.Read_Motor(addr, 0, 2)
    print("Product ID:",hex(redbuf[0]))
    print("Version ID:",hex(redbuf[1]))
    self.Write_Motor(addr, 100, writebuf)
    while 1:
      redbuf = self.Read_Motor(addr, 0, 2)
      if redbuf[0] == 0x10:
        print("OK!")
        print("")
        return

class DFRobot_Motor(DFRobot_MotorStepper):
  def __init__(self, id, i2c, addr_An):
    self.id = id
    self.addr = addr_An
    super().__init__(i2c, addr_An)
  def init(self):
    value=bytearray(1)
    value[0]=1;
    self.begin(self.addr)
    if self.id == M1:
      self.Write_Motor(self.addr, 0, value)
    elif self.id == M2:
      self.Write_Motor(self.addr, 10,value)
    elif self.id == M3:
      self.Write_Motor(self.addr, 16,value)
    elif self.id == M4:
      self.Write_Motor(self.addr, 22,value)
  def shutdown(self):
    value=bytearray(1)
    value[0]=1;
    if self.id == M1:
      self.Write_Motor(self.addr, 1,value)
    elif self.id == M2:
      self.Write_Motor(self.addr, 11,value)
    elif self.id == M3:
      self.Write_Motor(self.addr, 17,value)
    elif self.id == M4:
      self.Write_Motor(self.addr, 23,value)
  def stop(self):
    value=bytearray(1)
    value[0]=1;
    if self.id == M1:
      self.Write_Motor(self.addr, 2, value)
    elif self.id == M2:
      self.Write_Motor(self.addr, 12,value)
    elif self.id == M3:
      self.Write_Motor(self.addr, 18,value)
    elif self.id == M4:
      self.Write_Motor(self.addr, 24,value)
  def start(self,dir):
    value=bytearray(1)
    value[0]=1;
    if self.id == M1:
      if dir == CW:
        self.Write_Motor(self.addr, 3,value)
      elif dir == CCW:
        self.Write_Motor(self.addr, 4,value)
      motorState['motor1'] = dir
    elif self.id == M2:
      if dir == CW:
        self.Write_Motor(self.addr, 13,value)
      elif dir == CCW:
        self.Write_Motor(self.addr, 14,value)
      motorState['motor2'] = dir
    elif self.id == M3:
      if dir == CW:
        self.Write_Motor(self.addr, 19,value)
      elif dir == CCW:
        self.Write_Motor(self.addr, 20,value)
      motorState['motor3'] = dir
    elif self.id == M4:
      if dir == CW:
        self.Write_Motor(self.addr, 25,value)
      elif dir == CCW:
        self.Write_Motor(self.addr, 26,value)
      motorState['motor4'] = dir
  def speed(self,val):
    value=bytearray(2)
    if val>4096:
      val=4096
    val = 4096-val
    value[0]=val>>8
    value[1]=val
    if self.id == M1:
      self.Write_Motor(self.addr, 5,value)
    elif self.id == M2:
      self.Write_Motor(self.addr, 15,value)
    elif self.id == M3:
      self.Write_Motor(self.addr, 27,value)
    elif self.id == M4:
      self.Write_Motor(self.addr, 21,value)
  def getDir(self):
    if self.id == M1:
      return motorState['motor1']
    elif self.id == M2:
      return motorState['motor2']
    elif self.id == M3:
      return motorState['motor3']
    elif self.id == M4:
      return motorState['motor4']
    
    
class DFRobot_Stepper(DFRobot_MotorStepper):
  def __init__(self, id, i2c, addr):
    self.id = id
    super().__init__(i2c, addr)
  def init(self):
    value=bytearray(1)
    value[0]=1;
    self.begin(self.addr)
    if self.id == SA:
      self.Write_Motor(self.addr, 0,value)
    elif self.id == SB:
      self.Write_Motor(self.addr, 16,value)
  def shutdown(self):
    value=bytearray(1)
    value[0]=1;
    if self.id == SA:
      self.Write_Motor(self.addr, 1,value)
    elif self.id == SB:
      self.Write_Motor(self.addr, 17,value)
  def stop(self):
    value=bytearray(1)
    value[0]=1;
    if self.id == SA:
      self.Write_Motor(self.addr, 32,value)
    elif self.id == SB:
      self.Write_Motor(self.addr, 33,value)
  def speed(self,val):
    value=bytearray(2)
    value[0]=val>>8
    value[1]=val
    if self.id == SA:
      self.Write_Motor(self.addr, 34,value)
    elif self.id == SB:
      self.Write_Motor(self.addr, 35,value)
  def start(self, angle, speed, dir):
    value=bytearray(5)
    _angle=int(ceil(angle*10))
    count = 0
    if speed<8:
      speed=8;
    if _angle%9 <= _angle%18:
      count=_angle//9;
      value[0] = count>>8
      value[1] = count
      value[2] = speed>>8
      value[3] = speed
      value[4] = 0
      if self.id == SA:
        if dir == CW:
          self.Write_Motor(self.addr, 8,value)
        elif dir == CCW:
          self.Write_Motor(self.addr, 9,value)
        motorState['stepperA'] = dir
      elif self.id == SB: 
        if dir == CW:
          self.Write_Motor(self.addr, 30,value)
        elif dir == CCW:
          self.Write_Motor(self.addr, 31,value)
        motorState['stepperB'] = dir
    else:
      count=_angle//18;
      speed=speed*2-1
      value[0] = count>>8
      value[1] = count
      value[2] = speed>>8
      value[3] = speed
      value[4] = 0
      if self.id == SA:
        if dir == CW:
          self.Write_Motor(self.addr, 6,value)
        elif dir ==CCW:
          self.Write_Motor(self.addr, 7,value)
        motorState['stepperA'] = dir
      elif self.id == SB: 
        if dir == CW:
          self.Write_Motor(self.addr, 28,value)
        elif dir ==CCW:
          self.Write_Motor(self.addr, 29,value)
        motorState['stepperB'] = dir
  def getDir(self):
    if self.id == SA:
      return motorState['stepperA']
    elif self.id == SB:
      return motorState['stepperB']
      
      
      
      
      
      
      
      







































