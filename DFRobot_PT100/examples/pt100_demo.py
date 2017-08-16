import time
from machine import Pin

import pt100

led = Pin(2, Pin.OUT)


#36: analog pin
#1:  refer to volatage
obj_pt100 = pt100.PT100(36, 1)

while True:
  
  time.sleep_ms(500)
  pt100_temp = obj_pt100.read()
  print("temp 1 is %d ℃" %pt100_temp)
    
  
