#M1--->motor_Group_1--->[M1A(+),M1B(-)]
#M2--->motor_Group_2--->[M2A(+),M1B(-)]
#M3--->motor_Group_3--->[M3A(+),M3B(-)]
#M4--->motor_Group_4--->[M4A(+),M4B(-)]
#CW: rotate in positive direction
#CCW: rotate in reverse
#A0: Chip Selection Address 1
#A1: Chip Selection Address 2
#A2: Chip Selection Address 3
#A3: Chip Selection Address 4
from machine import Pin,I2C
import DFRobot_MotorStepper
import time
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
CW=DFRobot_MotorStepper.CW
CCW=DFRobot_MotorStepper.CCW

motor1=DFRobot_MotorStepper.DFRobot_Motor(DFRobot_MotorStepper.M1, i2c, DFRobot_MotorStepper.A0)
motor2=DFRobot_MotorStepper.DFRobot_Motor(DFRobot_MotorStepper.M2, i2c, DFRobot_MotorStepper.A0)
motor3=DFRobot_MotorStepper.DFRobot_Motor(DFRobot_MotorStepper.M3, i2c, DFRobot_MotorStepper.A0)
motor4=DFRobot_MotorStepper.DFRobot_Motor(DFRobot_MotorStepper.M4, i2c, DFRobot_MotorStepper.A0)
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
