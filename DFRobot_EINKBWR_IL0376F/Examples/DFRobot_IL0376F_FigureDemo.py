from machine import Pin,SPI
import DFRobot_EINKBWR_IL0376F
import time
#Pin definition
EINK_CS = 26
Font_CS = 10
EINK_DC = 5
BUSY    = 13
#color
LUCENCY = DFRobot_EINKBWR_IL0376F.LUCENCY
WHITE   = DFRobot_EINKBWR_IL0376F.WHITE
BLACK   = DFRobot_EINKBWR_IL0376F.BLACK
RED     = DFRobot_EINKBWR_IL0376F.RED
x=12

spi = SPI(baudrate=100000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
eink_IL0376F = DFRobot_EINKBWR_IL0376F.IL0376F(spi,EINK_CS,Font_CS,EINK_DC,BUSY)

while True:
  #Clear the screen and display white
  eink_IL0376F.clear(WHITE)
  #Let me draw a red dot
  for y in range(12,92):
    if(y%2 == 0):
      eink_IL0376F.drawPoint(x,y,RED)
  #Draw two lines
  eink_IL0376F.drawLine(24,12,36,92,RED)
  eink_IL0376F.drawLine(36,12,24,92,RED)
  #Draw a red rectangle
  eink_IL0376F.drawRectangle(48,12,51,81,RED)
  #Fill a rectangle with black
  eink_IL0376F.rectangleFill(55,19,37,67,BLACK)
  #Draw a hollow circle
  eink_IL0376F.drawCircle(160,51,40,0,RED)
  #Draw a solid circle
  eink_IL0376F.drawCircle(160,51,30,1,BLACK)
  #Refresh screen display
  eink_IL0376F.flush()
  time.sleep(5)


