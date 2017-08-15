from machine import Pin,I2C
import DFRobot_MotorStepper
import time

SA  = 0 #StepperA
SB  = 1 #StepperB
CW  = 0 #positive direction
CCW = 1 #rotate in reverse
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
IICADDR = (0x30>>1) #IIC device address

stepperA=DFRobot_MotorStepper.DFRobot_Stepper(SA, i2c, IICADDR)
stepperB=DFRobot_MotorStepper.DFRobot_Stepper(SB, i2c, IICADDR)
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