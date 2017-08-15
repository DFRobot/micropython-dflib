from machine import Pin,I2C
import DFRobot_MotorStepper
import time

SA  = 0 #StepperA
M3  = 2 #Motor3
M4  = 3 #Motor4
CW  = 0 #positive direction
CCW = 1 #rotate in reverse
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
IICADDR = (0x30>>1) #IIC device address

stepperA=DFRobot_MotorStepper.DFRobot_Stepper(SA, i2c, IICADDR)
motor1=DFRobot_MotorStepper.DFRobot_Motor(M3, i2c, IICADDR)
motor2=DFRobot_MotorStepper.DFRobot_Motor(M4, i2c, IICADDR)
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
  
