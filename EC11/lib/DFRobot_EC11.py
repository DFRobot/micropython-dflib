import time
from machine import Pin

class EC11:
  def __init__(self, pinA, pinB, pinC, pos = 0):
    self.originalPos = pos * 4
    self.pos = self.originalPos
    self.lastPos = self.pos
    self.lastSum = 0
    self.sum = 0
    self.lastTime = 0
    self.passTime = 0
    self.cbCoder = self.IRQHandler_pinAB
    self.cbButton = self.IRQHandler_pinC
    self.cbCoderStatus = 0
    self.cbButtonStatus = 0
    self.pinA = Pin(pinA, Pin.IN)
    self.pinB = Pin(pinB, Pin.IN)
    self.pinC = Pin(pinC, Pin.IN)
    self.pinA.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = self.IRQHandler_pinAB)
    self.pinB.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = self.IRQHandler_pinAB)
    self.pinC.irq(trigger = Pin.IRQ_FALLING, handler = self.IRQHandler_pinC)
    self.lastSum = (self.pinA.value() << 1) | self.pinB.value()
    
  def IRQHandler_pinAB(self, arg):
    self.sum = (self.pinA.value() << 1) | self.pinB.value()
    if self.sum != self.lastSum:
      res = (self.lastSum << 2) | self.sum
      self.lastSum = self.sum
      if res == 0b1101 or res == 0b0100 or res == 0b0010 or res == 0b1011:
        self.pos += 1
      if res == 0b1110 or res == 0b0111 or res == 0b0001 or res == 0b1000:
        self.pos -= 1
      var = round(self.pos / 4)
      if (((self.pos - self.originalPos) % 4) == 0) and (var != round(self.lastPos / 4)):
        currentTime = time.ticks_us()
        self.passTime = currentTime - self.lastTime
        self.lastTime = currentTime
        self.lastPos = self.pos
        if self.cbCoderStatus == 1:
          dict = {"pos" : 0, "time" : 0}
          dict["pos"] = var
          dict["time"] = self.passTime
          self.cbCoder(dict)
  
  def IRQHandler_pinC(self, arg):
    if self.cbButtonStatus == 1:
      self.cbButton()
  
  def readPos(self, dict):
    varTime = self.passTime
    self.passTime = 0
    dict["pos"] = round(self.pos / 4)
    dict["time"] = varTime
  
  def readKey(self):
    return self.pinC.value()
    
  def setPos(self, pos):
    self.originalPos = pos * 4
    self.pos = self.originalPos
    self.lastPos = self.pos
  
  def setCbCoder(self, fun):
    self.cbCoder = fun
    self.cbCoderStatus = 1
    
  def setCbKey(self, fun):
    self.cbButton = fun
    self.cbButtonStatus = 1

    
