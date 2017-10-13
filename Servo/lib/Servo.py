from machine import Pin
from machine import PWM


class Servo:
  def __init__(self,pin):
    self.pwm = PWM(Pin(pin),freq=50)
    self.max=self._map(2.4,0,20,0,1024)
    self.min=self._map(0.65,0,20,0,1024)
    
    self.angle(0)
    self.id = pin
    print("init %s"% (self.id))
    self.lastStat=0

  
  def angle(self,ang):
    if ang >= 180:
      ang=180
    if ang < 0:
      ang=0
    
    self.turn = self._map(ang,0,180,self.min,self.max)
    self.pwm.duty((int)(self.turn))
    self.lastStat=ang

   
  def read(self):
    return self.lastStat
    
 
  def _map(self,x,inMin,inMax,outMin,outMax):
    return (x-inMin)*(outMax-outMin)/(inMax-inMin)+outMin

  
  def deinit(self):
    print("deinit %s"% (self.id))
    self.pwm.deinit()
