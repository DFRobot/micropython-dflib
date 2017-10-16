from machine import Pin
import framebuf
import time
import HZK

#base_address
UNICODETOGB2312_ADDR  = (0x267B06)#Gb2312 coding base address
#ASC0808D2HZ_ADDR      = (0x0066c0)#7*8 ASCII base address
#ASC0812M2ZF_ADDR      = (0x066d40)#6*12 ASCII base address
GBEX0816ZF_ADDR       = (0x27BFA8)#8*16 ASCII base address
JFLS1516HZ_ADDR       = (0x21E72C)#16*16 chinese base address
JFLS1516HZBD_ADDR     = (0x22242C)#16*16 chinese punctuation base address
#scan_direction
EInk_scan_Dir3        = (3<<2)#从右到he_font_size
#CHARACTER_TYPE_8      = (0)#7*8 ASCII
#CHARACTER_TYPE_12     = (1)#6*12 ASCII
CHARACTER_TYPE_16     = (2)#8*16 ASCII
CHINESE_TYPE_1616     = (3)#16*16 Chinese
#color
LUCENCY               = (0)
WHITE                 = (1)
BLACK                 = (2)
RED                   = (3)

eInkdev={'highly':0, 'width':0, 'scandir':0}

class Device:
  def __init__(self, spi, cs_W21=26, cs_GT30=10, dc=5, busy=13):
    self.spi = spi
    self._DFR_W21_CS = Pin(cs_W21,Pin.OUT)
    self._DFR_GT30_CS = Pin(cs_GT30,Pin.OUT)
    self._DFR_W21_DC = Pin(dc,Pin.OUT)
    self.BUSY = Pin(busy,Pin.IN)
    HZK.init(spi,self._DFR_GT30_CS)
    
  def stateScan(self):
    while(not self.BUSY.value()):
	  pass

  def spiWriteByte(self, ddd):
    value=bytearray(1)
    value[0]=ddd
    self.spi.write(value)
   
  def wirteCmd(self, command):
    self._DFR_W21_CS.value(0)
    self._DFR_GT30_CS.value(1)
    self._DFR_W21_DC.value(0)
    self.spiWriteByte(command)
    self._DFR_W21_CS.value(1)
    
  def wirteData(self, data):
    self._DFR_W21_CS.value(0)
    self._DFR_GT30_CS.value(1)
    self._DFR_W21_DC.value(1)
    self.spiWriteByte(data)
    self._DFR_W21_CS.value(1)
  
  def wirteCmdData(self, command, data):
    length = len(data)
    self.wirteCmd(command)
    for i in range(length):
      self.wirteData(data[i])
      
  def spiRead(self, addr, len, ch):
    self._DFR_GT30_CS.value(0)
    self._DFR_W21_CS.value(1)
    self.spiWriteByte(0x0b)
    self.spiWriteByte((addr>>16)&0xff)
    self.spiWriteByte((addr>>8)&0xff)
    self.spiWriteByte(addr&0xff)
    self.spiWriteByte(0x00)
    self.spi.readinto(ch,0x00)
    self._DFR_GT30_CS.value(1)


class IL0376F:
  def __init__(self, spi, cs_W21=26, cs_GT30=10, dc=5, busy=13):
    self._device=Device(spi, cs_W21, cs_GT30, dc, busy)
    eInkdev['highly'] = 104
    eInkdev['width'] = 212
    eInkdev['scandir'] = EInk_scan_Dir3
    self.DF_Display_bw = bytearray(2756)
    self.DF_Display_red = bytearray(2756)
    self.pixel_bw = framebuf.FrameBuffer(self.DF_Display_bw,104,212,framebuf.MONO_HLSB)
    self.pixel_red = framebuf.FrameBuffer(self.DF_Display_red,104,212,framebuf.MONO_HLSB)
    
  def setWindow(self, xm, ym):
    hres = ym//8
    hres <<= 3
    vres_h = xm>>8
    vres_l = xm&0xff
    self._device.wirteCmd(0x61)
    self._device.wirteData(hres)
    self._device.wirteData(vres_h)
    self._device.wirteData(vres_l)
    eInkdev["highly"]= ym
    eInkdev["width"] = xm

  def clear(self,color):
    if(color == WHITE):
      self.pixel_bw.fill(0)
      self.pixel_red.fill(0)
    elif(color == RED):
      self.pixel_bw.fill(0)
      self.pixel_red.fill(1)
    elif(color == BLACK):
      self.pixel_bw.fill(1)
      self.pixel_red.fill(0)
    else:
      print("no color!")

  def flush(self):
    if(eInkdev["scandir"] == EInk_scan_Dir3):
      self.powerOn()
      self._device.wirteCmd(0x10)
      for i in range(2756):
        self._device.wirteData(~self.DF_Display_bw[i])
      self._device.wirteCmd(0x11)
      self._device.wirteCmd(0x13)
      for i in range(2756):
        self._device.wirteData(~self.DF_Display_red[i])
      self._device.wirteCmd(0x11)
      self.powerOff()
    
  def powerOn(self):
    self._device.wirteCmdData(0x06, (0x17,0x17,0x17))
    self._device.wirteCmd(0x04) 
    self._device.stateScan()
    self._device.wirteCmdData(0, (0xc3|eInkdev["scandir"],))    
    self._device.wirteCmdData(0x50, (0x37,))
    self._device.wirteCmdData(0x30, (0x39,))
    self.setWindow(212,104)
    self._device.wirteCmdData(0x82, (0x0a,))
    
  def powerOff(self):
    self._device.stateScan()
    self._device.wirteCmd(0x12)
    time.sleep(12)
    self._device.wirteCmdData(0x82, (0,))
    self._device.wirteCmdData(0x01, (2,0,0,0))
    self._device.wirteCmd(0X02) 

  def drawPoint(self, x, y, color):
    sx = y
    sy = 211-x
    if(color == WHITE):
      self.pixel_bw.pixel(sx, sy, 0)
      self.pixel_red.pixel(sx, sy,0)
    elif(color == RED):
      self.pixel_bw.pixel(sx, sy,0)
      self.pixel_red.pixel(sx, sy,1)
    elif(color == BLACK):
      self.pixel_bw.pixel(sx, sy,1)
      self.pixel_red.pixel(sx, sy,0)
    else:
      return False
    return True

  def drawLine(self, x1, y1, x2, y2, color):
    sx1 = y1
    sy1 = 211-x1
    sx2 = y2
    sy2 = 211-x2
    if(color == WHITE):
      self.pixel_bw.line(sx1, sy1, sx2, sy2, 0)
      self.pixel_red.line(sx1, sy1, sx2, sy2, 0)
    elif(color == RED):
      self.pixel_bw.line(sx1, sy1, sx2, sy2, 0)
      self.pixel_red.line(sx1, sy1, sx2, sy2, 1)
    elif(color == BLACK):
      self.pixel_bw.line(sx1, sy1, sx2, sy2, 1)
      self.pixel_red.line(sx1, sy1, sx2, sy2, 0)
    
  def rectangleFill(self, x1, y1, w, h, color):
    sx1 = y1
    sy1 = 211-x1-w+1
    if(color == WHITE):
      self.pixel_bw.fill_rect(sx1, sy1, h, w, 0)
      self.pixel_red.fill_rect(sx1, sy1, h, w, 0)
    elif(color == RED):
      self.pixel_bw.fill_rect(sx1, sy1, h, w, 0)
      self.pixel_red.fill_rect(sx1, sy1, h, w, 1)
    elif(color == BLACK):
      self.pixel_bw.fill_rect(sx1, sy1, h, w, 1)
      self.pixel_red.fill_rect(sx1, sy1, h, w, 0)
 
  def rectangle(self, x1, y1, w, h, color):
    sx1 = y1
    sy1 = 211-x1-w+1
    if(color == WHITE):
      self.pixel_bw.rect(sx1, sy1, h, w, 0)
      self.pixel_red.rect(sx1, sy1, h, w, 0)
    elif(color == RED):
      self.pixel_bw.rect(sx1, sy1, h, w, 0)
      self.pixel_red.rect(sx1, sy1, h, w, 1)
    elif(color == BLACK):
      self.pixel_bw.rect(sx1, sy1, h, w, 1)
      self.pixel_red.rect(sx1, sy1, h, w, 0)
      
  def drawRectangle(self, x1, y1, w, h, color):
    sx1 = y1
    sy1 = 211-x1-w+1
    if(color == WHITE):
      self.pixel_bw.rect(sx1, sy1, h, w, 0)
      self.pixel_red.rect(sx1, sy1, h, w, 0)
    elif(color == RED):
      self.pixel_bw.rect(sx1, sy1, h, w, 0)
      self.pixel_red.rect(sx1, sy1, h, w, 1)
    elif(color == BLACK):
      self.pixel_bw.rect(sx1, sy1, h, w, 1)
      self.pixel_red.rect(sx1, sy1, h, w, 0)
 
  def drawCirclePoint(self, xc, yc, x, y, color):
    Status = True
    Ixy=[1,1]
    for i in range(8):
      if(i<4):
        Status = self.drawPoint(xc + x*Ixy[0], yc + y*Ixy[1], color)
        if(not Status):
          return Status
      else:
        Status = self.drawPoint(xc + y*Ixy[0], yc + x*Ixy[1], color)
        if(not Status):
          return Status
      Ixy[0] = -1*Ixy[0]
      if((i+1)%2==0):
        Ixy[1] = -1*Ixy[1]
    return Status
  
  def drawCircle(self, xc, yc, r, fill, color):
    Status = True
    x = 0
    y = r
    d = 3-2*r
    if(xc+r<0 or xc-r >= 240 or yc+r < 0 or yc-r >= 320):
      return False
    while(x<=y):
      if(fill):
        for yi in range(x,y+1):
          Status = self.drawCirclePoint(xc, yc, x, yi, color)
      else:
        Status = self.drawCirclePoint(xc, yc, x, y, color)
      if(not Status):
        return Status
      if(d<0):
        d = d+4*x+6
      else:
        d = d+4*(x-y)
        y=y-1
      x=x+1
 
  def showStr(self, x, y, size, ch, color):
    sx=x
    if(size == CHINESE_TYPE_1616):
      MAXfont = 32
      width = 16 
    elif(size == CHARACTER_TYPE_16):
      MAXfont = 16
      width = 8
    for j in range(MAXfont):
      font = ch[j]
      for i in range(8):
        if(font&0x80):
          self.drawPoint(sx, y, color)
        else:
          self.drawPoint(sx, y, LUCENCY)
        font = font<<1
        sx = sx+1
        if((sx-x)==width):
          y = y+1
          sx = x
  
  def disStr(self, x, y, Str, color):
    str_null = bytearray(32)
    unicode_hz = bytearray(2)
    gb2312_hz = bytearray(2)
    length = len(Str)
    i = 0
    while(i<length):
      if(ord(Str[i]) <= 127):
        pass
      else:
        if(((Str[i].encode('utf8')[0]) & 0xf0) == 0xe0):
          temp = (Str[i].encode('utf8')[0] & 0x0f) << 12 | (Str[i].encode('utf8')[1] & 0x3f) << 6 | (Str[i].encode('utf8')[2] & 0x3f)
          unicode_hz[0] = temp >> 8
          unicode_hz[1] = temp
          str_null = HZK.searchUnicode(unicode_hz[0]<<8|unicode_hz[1])
          self.showStr(x, y, CHINESE_TYPE_1616, str_null, color)
          x = x+16
          if(x+16 > 211):
            x = 0
            y = y+18
            if(y+16 > 103):
              y = 0
        elif(((Str[i].encode('gb2312')[0]) & 0x80) == 0x80):
          gb2312_hz[0] = Str[i].encode('gb2312')[0]
          gb2312_hz[1] = Str[i].encode('gb2312')[1]
          str_null = HZK.searchGBK(gb2312_hz[0]<<8|gb2312_hz[1])
          self.showStr(x, y, CHINESE_TYPE_1616, str_null, color)#Refresh the cache
          x = x+16
          if(x+16 > 211):
            x = 0
            y = y+18
            if(y+16 > 103):
              y = 0
      i+=1


