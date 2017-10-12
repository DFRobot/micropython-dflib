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

spi = SPI(baudrate=100000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
eink_IL0376F = DFRobot_EINKBWR_IL0376F.IL0376F(spi,EINK_CS,Font_CS,EINK_DC,BUSY)

while True:
  #Clear the screen and display white
  eink_IL0376F.clear(WHITE)
  #Displays a string, red font
  eink_IL0376F.disStr(12,12,"三色电子墨水屏中文显示测试程序",RED);
  #Refresh screen display
  eink_IL0376F.disRefresh()
  time.sleep(5)

