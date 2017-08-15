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

motorState={'motor1':0, 'motor2':0, 'motor3':0, 'motor4':0, 'stepperA':0,'stepperB':0,'Begin':0}

class MotorStepper:
  def __init__(self, i2c, addr):
    self.i2c = i2c
    self.addr = addr
  def Write_Motor(self, Reg, buf):
    if currentBoard=="esp8266" or currentBoard=="esp32":
      self.i2c.writeto_mem(self.addr,Reg,buf)
  def Read_Motor(self, Reg, num): 
    _redbuf=bytearray(2) 
    if currentBoard=="esp8266" or currentBoard=="esp32":
      _redbuf = self.i2c.readfrom_mem(self.addr ,Reg, num)
    return _redbuf
  def begin(self):
    writebuf = bytearray("ok")
    redbuf = bytearray(2)
    motorState['Begin'] = 1
    redbuf = self.Read_Motor(0, 2)
    print("Product ID:",hex(redbuf[0]))
    print("Version ID:",hex(redbuf[1]))
    self.Write_Motor(100, writebuf)
    while 1:
      redbuf = self.Read_Motor(0, 2)
      if redbuf[0] == 0x10:
        print("OK!")
        return

class DFRobot_Motor(MotorStepper):
  def __init__(self, id, i2c, addr):
    self.id = id
    super().__init__(i2c, addr)
  def init(self):
    value=bytearray(1)
    value[0]=1;
    if motorState['Begin'] == 0:
      self.begin()
    if self.id == M1:
      self.Write_Motor(0,value)
    elif self.id == M2:
      self.Write_Motor(10,value)
    elif self.id == M3:
      self.Write_Motor(16,value)
    elif self.id == M4:
      self.Write_Motor(22,value)
  def shutdown(self):
    value=bytearray(1)
    value[0]=1;
    if self.id == M1:
      self.Write_Motor(1,value)
    elif self.id == M2:
      self.Write_Motor(11,value)
    elif self.id == M3:
      self.Write_Motor(17,value)
    elif self.id == M4:
      self.Write_Motor(23,value)
  def stop(self):
    value=bytearray(1)
    value[0]=1;
    if self.id == M1:
      self.Write_Motor(2,value)
    elif self.id == M2:
      self.Write_Motor(12,value)
    elif self.id == M3:
      self.Write_Motor(18,value)
    elif self.id == M4:
      self.Write_Motor(24,value)
  def start(self,dir):
    value=bytearray(1)
    value[0]=1;
    if self.id == M1:
      if dir == CW:
        self.Write_Motor(3,value)
      elif dir == CCW:
        self.Write_Motor(4,value)
      motorState['motor1'] = dir
    elif self.id == M2:
      if dir == CW:
        self.Write_Motor(13,value)
      elif dir == CCW:
        self.Write_Motor(14,value)
      motorState['motor2'] = dir
    elif self.id == M3:
      if dir == CW:
        self.Write_Motor(19,value)
      elif dir == CCW:
        self.Write_Motor(20,value)
      motorState['motor3'] = dir
    elif self.id == M4:
      if dir == CW:
        self.Write_Motor(25,value)
      elif dir == CCW:
        self.Write_Motor(26,value)
      motorState['motor4'] = dir
  def speed(self,val):
    value=bytearray(2)
    if val>4096:
      val=4096
    val = 4096-val
    value[0]=val>>8
    value[1]=val
    if self.id == M1:
      self.Write_Motor(5,value)
    elif self.id == M2:
      self.Write_Motor(15,value)
    elif self.id == M3:
      self.Write_Motor(27,value)
    elif self.id == M4:
      self.Write_Motor(21,value)
  def getDir(self):
    if self.id == M1:
      return motorState['motor1']
    elif self.id == M2:
      return motorState['motor2']
    elif self.id == M3:
      return motorState['motor3']
    elif self.id == M4:
      return motorState['motor4']
    
    
class DFRobot_Stepper(MotorStepper):
  def __init__(self, id, i2c, addr):
    self.id = id
    super().__init__(i2c, addr)
  def init(self):
    value=bytearray(1)
    value[0]=1;
    if motorState['Begin'] == 0:
      self.begin()
    if self.id == SA:
      self.Write_Motor(0,value)
    elif self.id == SB:
      self.Write_Motor(16,value)
  def shutdown(self):
    value=bytearray(1)
    value[0]=1;
    if self.id == SA:
      self.Write_Motor(1,value)
    elif self.id == SB:
      self.Write_Motor(17,value)
  def stop(self):
    value=bytearray(1)
    value[0]=1;
    if self.id == SA:
      self.Write_Motor(32,value)
    elif self.id == SB:
      self.Write_Motor(33,value)
  def speed(self,val):
    value=bytearray(2)
    value[0]=val>>8
    value[1]=val
    if self.id == SA:
      self.Write_Motor(34,value)
    elif self.id == SB:
      self.Write_Motor(35,value)
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
          self.Write_Motor(8,value)
        elif dir == CCW:
          self.Write_Motor(9,value)
        motorState['stepperA'] = dir
      elif self.id == SB: 
        if dir == CW:
          self.Write_Motor(30,value)
        elif dir == CCW:
          self.Write_Motor(31,value)
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
          self.Write_Motor(6,value)
        elif dir ==CCW:
          self.Write_Motor(7,value)
        motorState['stepperA'] = dir
      elif self.id == SB: 
        if dir == CW:
          self.Write_Motor(28,value)
        elif dir ==CCW:
          self.Write_Motor(29,value)
        motorState['stepperB'] = dir
  def getDir(self):
    if self.id == SA:
      return motorState['stepperA']
    elif self.id == SB:
      return motorState['stepperB']
      
      
      
      
      
      
      
      






































