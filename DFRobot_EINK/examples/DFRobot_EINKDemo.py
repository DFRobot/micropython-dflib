from machine import Pin,SPI
import DFRobot_EINK
import time

spi = SPI(baudrate=100000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))

eink = DFRobot_EINK.DFRobot_Eink(spi,Pin(2),Pin(4),Pin(5))

#color
LUCENCY  = 0
WHITE    = 1
BLACK    = 2
RED      = 3
x=12

#Clear the screen and display white
eink.clear(WHITE)


while True:
  #Let me draw a red dot
  for y in range(12,92):
    if(y%2 == 0):
      eink.drawPoint(x,y,RED)
  #Draw two lines
  eink.drawLine(24,12,36,92,RED)
  eink.drawLine(36,12,24,92,RED)
  #Draw a red rectangle
  eink.drawRectangle(48,12,98,92,RED)
  #Fill a rectangle with black
  eink.rectangleFill(55,19,91,85,BLACK)
  #Draw a hollow circle
  eink.drawCircle(160,51,40,0,RED)
  #Draw a solid circle
  eink.drawCircle(160,51,30,1,BLACK)
  #Refresh screen display
  eink.disRefresh()
  time.sleep(3000)
  #Clear the screen and display white
  eink.clear(WHITE)

