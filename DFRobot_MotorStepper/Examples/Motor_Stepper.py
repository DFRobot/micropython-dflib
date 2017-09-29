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
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

stepperA=DFRobot_MotorStepper.DFRobot_Stepper(DFRobot_MotorStepper.SA, i2c, DFRobot_MotorStepper.A0)
motor1=DFRobot_MotorStepper.DFRobot_Motor(DFRobot_MotorStepper.M3, i2c, DFRobot_MotorStepper.A0)
motor2=DFRobot_MotorStepper.DFRobot_Motor(DFRobot_MotorStepper.M4, i2c, DFRobot_MotorStepper.A0)
#Initialize motor drive chip of stepping motor (Group A) and ¾ group of D.C motor
motor3.init()
motor4.init()
stepperA.init()

def reverse_SA():
  stepperA.start(0, 20, not stepperA.getDir())
def reverse3_4():
  motor3.start(not motor3.getDir());
  motor4.start(not motor4.getDir());

i=0
while True:
  reverse3_4() #Motor3 and motor4 reverse in every 1.5 seconds
  if (++i%2) == 0:
    reverse_SA() #Stepping motor (Group A) reverse in every 3 seconds
    i=0
  time.sleep(1.5)
  
