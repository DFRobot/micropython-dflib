import time
from machine import Pin

import ec11

led = Pin(2, Pin.OUT)


'''
dir: 1 :C.W, else anti-Clock
pos: ec11 position
ec11_time: one step time(us)
button: button status
if this function is called
if pos changed and call this function, is_pressed will be 2
if button changed and call this function, is_pressed will be 0
'''
def ec11_callBack(dir, pos, ec11_time, is_pressed):
  if is_pressed == 2:
    print("direction is: %d, position at %d, spend %d us" %(dir, pos, ec11_time))
  else:
    print("button change to %d" %is_pressed)


#26, 27, 9: ec11's pin A, pin B and pin C
#ec11_callBack: call back function
#2: init position(it can be default with 0)
obj_coder = ec11.EC11(26, 27, 9, ec11_callBack, 2)

while True:
  pass  
    
  
