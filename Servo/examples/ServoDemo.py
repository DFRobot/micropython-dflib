import Servo
import time
sv1 = Servo.Servo(pin=15)
sv2 = Servo.Servo(pin=13)
time.sleep(1)


try:
  while True:
    sv1.angle(0)
    sv2.angle(0)
    time.sleep(2)
    sv1.angle(180)
    sv2.angle(180)
    time.sleep(2)
except:
  sv1.deinit()
  sv2.deinit()

