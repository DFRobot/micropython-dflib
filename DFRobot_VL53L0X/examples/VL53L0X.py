
from machine import Pin,I2C
import DFRobot_VL53L0X
import time
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
sensor = DFRobot_VL53L0X.DFRobotVL53L0X(i2c)

High       = 0 #High precision(0.25mm)
Low        = 1 #Low precision(1mm)
Single     = 0 #Single mode
Continuous = 1 #Back-to-back mode

sensor.begin(0x50)
sensor.setMode(Continuous,High)
sensor.start()

def calcSpeed():
	inspeed1 = sensor.distance
	time.sleep(0.05)
	inspeed2 = sensor.distance
	return (inspeed2-inspeed1)/50.0

while 1:
  print("----- START TEST ----")
  print("ambient Count:",sensor.getAmbientCount)
  print("Signal Count:",sensor.getSignalCount)
  print("Distance(mm):",sensor.distance)
  print("Status:",sensor.getStatus)
  print("Speed(m/s):",calcSpeed())
  print("----- END TEST ----")
  time.sleep(1)
 






