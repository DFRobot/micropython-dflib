import time
import DFRobot_EC11

#this program is for esp8266 or esp32

#EC11 pin and pos config
ec11 = DFRobot_EC11.EC11(13, 10, 15, 2)  #for esp8266
#ec11 = DFRobot_EC11.EC11(26, 27, 9, 2)  #for esp32

#define coder intrrupt call back function
def ec11_cbCoder(dict_ec11):
  print ("pos = %d" %dict_ec11["pos"])
  print ("last action time(us) = %d" %dict_ec11["time"])

#defien key intrrupt call back function
def ec11_cbKey():
  time.sleep(0.01)
  print ("key down")

#set call back function
ec11.setCbCoder(ec11_cbCoder)
ec11.setCbKey(ec11_cbKey)

while True:
  pass
  
  
