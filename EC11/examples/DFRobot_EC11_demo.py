import time
import DFRobot_EC11

#this program is for esp8266 or esp32, with inquiry method

#EC11 pin and pos config
ec11 = DFRobot_EC11.EC11(13, 10, 15, 2)  #for esp8266
#ec11 = DFRobot_EC11.EC11(26, 27, 9, 2)  #for esp32

dict_ec11 = {"pos": 0, "time": 0}

while True:
  #read current pos and last action time (us). If the position is unchanged, the read time is 0
  ec11.readPos(dict_ec11)
  if (dict_ec11["pos"] > 10) or (dict_ec11["pos"] < -10):
    ec11.setPos(0)  #set pos
    dict_ec11["pos"]
  print ("pos = %d" %dict_ec11["pos"])
  print ("last action time(us) = %d" %dict_ec11["time"])
  keyStatus = ec11.readKey()
  print ("key status = %d" %keyStatus)
  time.sleep(0.5)
  