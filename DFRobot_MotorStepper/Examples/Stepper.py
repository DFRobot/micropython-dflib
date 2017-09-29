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
CW=DFRobot_MotorStepper.CW

stepperA=DFRobot_MotorStepper.DFRobot_Stepper(DFRobot_MotorStepper.SA, i2c, DFRobot_MotorStepper.A0)
stepperB=DFRobot_MotorStepper.DFRobot_Stepper(DFRobot_MotorStepper.SB, i2c, DFRobot_MotorStepper.A0)
stepperA.init()
stepperB.init()

def reverse_SA():
  stepperA.start(0, 20, not stepperA.getDir())

i=0
while True:
  stepperB.start(6.3, 15, CW) #Group B stepper motor every 1 s rotational 6.3 °
  if (++i%2) == 0: 
    reverse_SA() #Stepping motor (Group A) rotate in reverse in every 2 seconds
    i=0
  time.sleep(1)