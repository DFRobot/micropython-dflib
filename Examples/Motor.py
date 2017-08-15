from machine import Pin,I2C
import DFRobot_MotorStepper
import time

M1  = 0 #Motor1
M2  = 1 #Motor2
M3  = 2 #Motor3
M4  = 3 #Motor4
CW  = 0 #positive direction
CCW = 1 #rotate in reverse
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
IICADDR = (0x30>>1)#IIC device address

motor1=DFRobot_MotorStepper.DFRobot_Motor(M1, i2c, IICADDR)
motor2=DFRobot_MotorStepper.DFRobot_Motor(M2, i2c, IICADDR)
motor3=DFRobot_MotorStepper.DFRobot_Motor(M3, i2c, IICADDR)
motor4=DFRobot_MotorStepper.DFRobot_Motor(M4, i2c, IICADDR)
motor1.init()
motor2.init()
motor3.init()
motor4.init()

while True:
  #Setting initial velocity
  motor1.speed(4096);
  motor2.speed(4096);
  motor3.speed(4096);
  motor4.speed(4096);
  #Motor1 and motor3 rotate in positive direction; motor2 and motor4 rotate in reverse
  motor1.start(CW);
  motor2.start(CCW);
  motor3.start(CW);
  motor4.start(CCW);
  time.sleep(2);

  #Change velocity in 2 seconds
  motor1.speed(1000);
  motor2.speed(1000);
  motor3.speed(1000);
  motor4.speed(1000);
  #All motors rotate in reverse
  motor1.start(CCW);
  motor2.start(CW);
  motor3.start(CCW);
  motor4.start(CW);
  time.sleep(2);
  
  #All motors brake and stop rotating
  motor1.stop();
  motor2.stop();
  motor3.stop();
  motor4.stop();
  time.sleep(2);