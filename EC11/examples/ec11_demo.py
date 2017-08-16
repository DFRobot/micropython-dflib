import time
from machine import Pin

import ec11

led = Pin(2, Pin.OUT)


'''
dir: 1 :C.W, else anti-Clock
pos: ec11 position
ec11_time: one step time(us)
is_pressed: button status
if this function is called
if dir == 0, button pressed called this function, else position changed called this function
'''
def ec11_callBack(dir, pos, ec11_time, is_pressed):
  if dir != 0:
    print("direction is: %d, position at %d, spend %d us" %(dir, pos, ec11_time))
  else:
    print("button change to %d" %is_pressed)


#26, 27, 9: ec11's pin A, pin B and pin C
#ec11_callBack: call back function
#2: init position(it can be default with 0)
obj_coder = ec11.EC11(26, 27, 9, ec11_callBack, 2)

while True:
  pass  
    
  
