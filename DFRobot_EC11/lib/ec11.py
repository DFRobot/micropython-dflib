import time
from machine import Pin


class EC11:
  def __init__(self, pinA, pinB, pinC, cbFun, pos = 0):
    self.pos = pos
    self.lastSum = 0
    self.sum = 0
    self.lastTime = 0
    self.time = 0
    self.cbFun = cbFun
    self.dir = 0
    self.pinA = Pin(pinA, Pin.IN)
    self.pinB = Pin(pinB, Pin.IN)
    self.pinC = Pin(pinC, Pin.IN)
    self.pinA.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = self.IRQHandler_pinAB)
    self.pinB.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = self.IRQHandler_pinAB)
    self.pinC.irq(trigger = Pin.IRQ_FALLING, handler = self.IRQHandler_pinC)
    
  def IRQHandler_pinAB(self, arg):
    status_pinA = self.pinA.value()
    status_pinB = self.pinB.value()
    self.sum = (status_pinA << 1) | status_pinB
    if self.sum != self.lastSum:
      res = (self.lastSum << 2) | self.sum
      self.lastSum = self.sum
      if res == 0b1101 or res == 0b0100 or res == 0b0010 or res == 0b1011:
        self.pos += 1
        self.dir = 1
      if res == 0b1110 or res == 0b0111 or res == 0b0001 or res == 0b1000:
        self.pos -= 1
        self.dir = -1
      self.time = time.ticks_us() - self.lastTime
      self.lastTime = time.ticks_us()
      self.cbFun(self.dir, self.pos, self.time, self.pinC.value())
  
  def IRQHandler_pinC(self, arg):
    self.cbFun(0, 0, 0, 0)
  
  def readPos(self):
    return self.pos
    
  def readTime_ms(self):
    return self.time / 1000
    
  def readTime_us(self):
    return self.time
  
  def readButton(self):
    return self.pinC.value()

