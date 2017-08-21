#IIC function
from micropython import const
import sys
import time

currentBoard=""
if(sys.platform == "esp8266"):
  currentBoard = "esp8266"
elif(sys.platform == "esp32"):
  currentBoard = "esp32"
elif(sys.platform=="pyboard"):
  currentBoard="pyboard"
  import pyb 
  
VL53L0X_REG_IDENTIFICATION_MODEL_ID      	      = const(0x00c0)
VL53L0X_REG_IDENTIFICATION_REVISION_ID        	= const(0x00c2)
VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD   	  = const(0x0050)
VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD 	  = const(0x0070)
VL53L0X_REG_SYSRANGE_START                 		  = const(0x0000)
VL53L0X_REG_RESULT_INTERRUPT_STATUS        		  = const(0x0013)
VL53L0X_REG_RESULT_RANGE_STATUS            	  	= const(0x0014)
VL53L0X_REG_I2C_SLAVE_DEVICE_ADDRESS          	= const(0x008a)
VL53L0X_I2C_ADDR							                  = const(0x0029)
VL53L0X_REG_SYSTEM_RANGE_CONFIG			            = const(0x0009)
VL53L0X_REG_VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV   = const(0x0089)
VL53L0X_REG_SYSRANGE_MODE_SINGLESHOT            = const(0x0000)
VL53L0X_REG_SYSRANGE_MODE_START_STOP            = const(0x0001)
VL53L0X_REG_SYSRANGE_MODE_BACKTOBACK            = const(0x0002)
VL53L0X_REG_SYSRANGE_MODE_TIMED                 = const(0x0004)

VL53L0X_DEVICEMODE_SINGLE_RANGING	              = const(0x0000)
VL53L0X_DEVICEMODE_CONTINUOUS_RANGING	          = const(0x0001)
VL53L0X_DEVICEMODE_CONTINUOUS_TIMED_RANGING     = const(0x0003)
VL53L0X_DEFAULT_MAX_LOOP                        = const(0x00c8)

ESD_2V8 = 1
High = 0
Low = not High
I2C_DevAddr = const(0x29)
DISABLE = 0
ENABLE = not DISABLE
DetailedData={'ambientCount':0, 'signalCount':0, 'distance':0, 'status':0, 'mode':0, 'precision':0}
  
class DFRobotVL53L0X:
  def __init__(self, i2c, addr=0x29):
    self.i2c = i2c
    self.addr = addr
    self.I2C_DevAddr = self.addr
    self.originalData = bytearray(12)
  def writeData(self, Reg, buf):
    if currentBoard=="esp8266" or currentBoard=="esp32":
      self.i2c.writeto_mem(self.I2C_DevAddr,Reg,buf)
  def readData(self, Reg, num):
    if currentBoard=="esp8266" or currentBoard=="esp32":
      self.originalData = self.i2c.readfrom_mem(self.I2C_DevAddr ,Reg, num)
      
  def begin(self, addr):
    if not(self.i2c.scan()[0] == self.addr):
      self.I2C_DevAddr = self.i2c.scan()[0]
    self.DataInit()
    self.setDeviceAddress(addr)
    self.readData(VL53L0X_REG_IDENTIFICATION_REVISION_ID, 1)
    print("Revision ID:",hex(self.originalData[0]))
    self.readData(VL53L0X_REG_IDENTIFICATION_MODEL_ID, 1)
    print("Device ID:",hex(self.originalData[0]))
    
  def setDeviceAddress(self, newAddr):
    newAddr &= 0x7F
    writebuf = bytearray(1)
    writebuf[0] = newAddr
    self.writeData(VL53L0X_REG_I2C_SLAVE_DEVICE_ADDRESS, writebuf)
    self.I2C_DevAddr = newAddr
    
  def readVL53L0X(self):
    self.readData(VL53L0X_REG_RESULT_RANGE_STATUS,12)
    DetailedData['ambientCount'] = ((self.originalData[6] & 0xFF) << 8) | (self.originalData[7] & 0xFF)
    DetailedData['signalCount'] = ((self.originalData[8] & 0xFF) << 8) | (self.originalData[9] & 0xFF)
    DetailedData['distance'] = ((self.originalData[10] & 0xFF) << 8) | (self.originalData[11] & 0xFF)
    DetailedData['status'] = ((self.originalData[0] & 0x78) >> 3)
    
  def setMode(self, mode, precision):
    DetailedData['mode'] = mode
    if precision == High:
      self.setRangeFractionEnable(ENABLE)
      DetailedData['precision'] = precision
    elif precision == Low:
      self.setRangeFractionEnable(DISABLE)
      DetailedData['precision'] = precision
    
  def start(self):
    StartStopByte = VL53L0X_REG_SYSRANGE_MODE_START_STOP
    writebuf = bytearray(1)
    DeviceMode = 0
    LoopNb=0
    Byte = 0
    DeviceMode = DetailedData['mode']
    writebuf[0] = 0x01
    self.writeData(0x80, writebuf)
    self.writeData(0xFF, writebuf)
    writebuf[0] = 0x00
    self.writeData(0x00, writebuf)
    writebuf[0] = 0x3c
    self.writeData(0x91, writebuf)
    writebuf[0] = 0x01
    self.writeData(0x00, writebuf)
    writebuf[0] = 0x00
    self.writeData(0xFF, writebuf)
    self.writeData(0x80, writebuf)
    
    if DeviceMode == VL53L0X_DEVICEMODE_SINGLE_RANGING:
      writebuf[0] = 0x01
      self.writeData(VL53L0X_REG_SYSRANGE_START, writebuf)
      Byte = StartStopByte
      LoopNb = 0
      while True:
        if LoopNb>0:
          self.readData(VL53L0X_REG_SYSRANGE_START, 1)
          Byte = self.originalData[0]
          LoopNb = LoopNb + 1
        if not(((Byte & StartStopByte) == StartStopByte) and (LoopNb < VL53L0X_DEFAULT_MAX_LOOP)):
          break
    elif DeviceMode == VL53L0X_DEVICEMODE_CONTINUOUS_RANGING:
      writebuf[0] = VL53L0X_REG_SYSRANGE_MODE_BACKTOBACK
      self.writeData(VL53L0X_REG_SYSRANGE_START, writebuf)
    else:
      print("---Selected mode not supported---")
 
  def stop(self):
    writebuf = bytearray(1)
    writebuf[0] = VL53L0X_REG_SYSRANGE_MODE_SINGLESHOT
    self.writeData(VL53L0X_REG_SYSRANGE_START, writebuf)
    writebuf[0] = 0x01
    self.writeData(0xFF, writebuf)
    writebuf[0] = 0x00
    self.writeData(0x00, writebuf)
    writebuf[0] = 0x0
    self.writeData(0x91, writebuf)
    writebuf[0] = 0x01
    self.writeData(0x00, writebuf)
    writebuf[0] = 0x00
    self.writeData(0xFF, writebuf)  
   
  def setRangeFractionEnable(self, NewState):
    writebuf = bytearray(1)
    writebuf[0] = NewState
    self.writeData(VL53L0X_REG_SYSTEM_RANGE_CONFIG, writebuf)
    
  def DataInit(self):
    writebuf = bytearray(1)
    if ESD_2V8 == 1:
      self.readData(VL53L0X_REG_VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV, 1)
      writebuf[0] = self.originalData[0]
      writebuf[0] = (writebuf[0] & 0xFE) | 0x01
      self.writeData(VL53L0X_REG_VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV, writebuf)
      writebuf[0] = 0x00
    self.writeData(0x88, writebuf)
    writebuf[0] = 0x01
    self.writeData(0x80, writebuf)
    self.writeData(0xFF, writebuf)
    writebuf[0] = 0x00
    self.writeData(0x00, writebuf)
    writebuf[0] = 0x3c
    self.writeData(0x91, writebuf)
    writebuf[0] = 0x01
    self.writeData(0x00, writebuf)
    writebuf[0] = 0x00
    self.writeData(0xFF, writebuf)
    self.writeData(0x80, writebuf)
    
  @property
  def getDistance(self):
	"Return the measured distance."
    self.readVL53L0X()
    if DetailedData['precision'] == High:
      value = DetailedData['distance']/4.0
    else:
      value = DetailedData['distance']
    if DetailedData['status'] == 11:
      return value
    else:
      return 0#"{:s}".format("Inaccurate!")
  
  @property
  def getAmbientCount(self):
	"Return ambient count."
    value = DetailedData['ambientCount']
    return value
    
  @property
  def getSignalCount(self):
	"Return signal count."
    value = DetailedData['signalCount']
    return value 
    
  @property
  def getStatus(self):
	"Return status."
    value = DetailedData['status']
    return value

































