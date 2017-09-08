from micropython import const
import time

DFR_W21_SPI_SPEED     = const(0x02)
#scan_direction
EInk_scan_Dir1        = const(2<<2)#从左到右，从上到下
EInk_scan_Dir2        = const(0<<2)#从左到右，从下到上
EInk_scan_Dir3        = const(3<<2)#从右到左，从上到下
EInk_scan_Dir4        = const(1<<2)#从右到左，从下到上
#color
LUCENCY               = const(0)
WHITE                 = const(1)
BLACK                 = const(2)
RED                   = const(3)
#base_address
UNICODETOGB2312_ADDR  = const(0x267B06)#Gb2312 coding base address
ASC0808D2HZ_ADDR      = const(0x0066c0)#7*8 ASCII base address
ASC0812M2ZF_ADDR      = const(0x066d40)#6*12 ASCII base address
GBEX0816ZF_ADDR       = const(0x27BFAA)#8*16 ASCII base address
JFLS1516HZ_ADDR       = const(0x21E72C)#16*16 chinese base address
JFLS1516HZBD_ADDR     = const(0x22242C)#16*16 chinese punctuation base address
#The_font_size
CHARACTER_TYPE_8      = const(0)#7*8 ASCII
CHARACTER_TYPE_12     = const(1)#6*12 ASCII
CHARACTER_TYPE_16     = const(2)#8*16 ASCII
CHINESE_TYPE_1616     = const(3)#16*16 Chinese

eInkdev={'highly':0, 'width':0, 'scandir':0}

ucs_gb2312_table = [
'''
[0x00A4,0xA1E8], [0x00A7,0xA1EC], [0x00A8,0xA1A7], [0x00B0,0xA1E3], '''A1'''
[0x00B1,0xA1C0], [0x00B7,0xA1A4], [0x00D7,0xA1C1], [0x00F7,0xA1C2],
[0x02C7,0xA1A6], [0x02C9,0xA1A5], [0x2014,0xA1AA], [0x2016,0xA1AC],  
[0x2018,0xA1AE], [0x2019,0xA1AF], [0x201C,0xA1B0], [0x201D,0xA1B1],  
[0x2026,0xA1AD], [0x2030,0xA1EB], [0x2032,0xA1E4], [0x2033,0xA1E5],  
[0x203B,0xA1F9], [0x2103,0xA1E6], [0x2116,0xA1ED], [0x2190,0xA1FB],  
[0x2191,0xA1FC], [0x2192,0xA1FA], [0x2193,0xA1FD], [0x2208,0xA1CA],  
[0x220F,0xA1C7], [0x2211,0xA1C6], [0x221A,0xA1CC], [0x221D,0xA1D8],  
[0x221E,0xA1DE], [0x2220,0xA1CF], [0x2225,0xA1CE], [0x2227,0xA1C4],  
[0x2228,0xA1C5], [0x2229,0xA1C9], [0x222A,0xA1C8], [0x222B,0xA1D2],  
[0x222E,0xA1D3], [0x2234,0xA1E0], [0x2235,0xA1DF], [0x2236,0xA1C3],  
[0x2237,0xA1CB], [0x223D,0xA1D7], [0x2248,0xA1D6], [0x224C,0xA1D5],  
[0x2260,0xA1D9], [0x2261,0xA1D4], [0x2264,0xA1DC], [0x2265,0xA1DD],  
[0x226E,0xA1DA], [0x226F,0xA1DB], [0x2299,0xA1D1], [0x22A5,0xA1CD],  
[0x2312,0xA1D0], [0x25A0,0xA1F6], [0x25A1,0xA1F5], [0x25B2,0xA1F8], 
[0x25C7,0xA1F3], [0x25CB,0xA1F0], [0x25CE,0xA1F2], [0x25CF,0xA1F1],  
[0x2605,0xA1EF], [0x2606,0xA1EE], [0x2640,0xA1E2], [0x2642,0xA1E1],  
[0x3000,0xA1A1], [0x3001,0xA1A2], [0x3002,0xA1A3], [0x3003,0xA1A8],  
[0x3005,0xA1A9], [0x3008,0xA1B4], [0x3009,0xA1B5], [0x300A,0xA1B6],  
[0x300B,0xA1B7], [0x300C,0xA1B8], [0x300D,0xA1B9], [0x300E,0xA1BA],  
[0x300F,0xA1BB], [0x3010,0xA1BE], [0x3011,0xA1BF], [0x3013,0xA1FE],  
[0x3014,0xA1B2], [0x3015,0xA1B3], [0x3016,0xA1BC], [0x3017,0xA1BD],
[0x25B3,0xA1F7], [0x25C6,0xA1F4], [0xFF04,0xA1E7], [0xFF5E,0xA1AB], 
[0xFFE0,0xA1E9], [0xFFE1,0xA1EA],
[0x2161,0xA2F2], [0x2162,0xA2F3], [0x2163,0xA2F4], [0x2164,0xA2F5], '''A2'''
[0x2165,0xA2F6], [0x2166,0xA2F7], [0x2167,0xA2F8], [0x2168,0xA2F9],  
[0x2169,0xA2FA], [0x216A,0xA2FB], [0x216B,0xA2FC], [0x2460,0xA2D9], 
[0x2463,0xA2DC], [0x2464,0xA2DD], [0x2465,0xA2DE], [0x2466,0xA2DF],  
[0x2467,0xA2E0], [0x2468,0xA2E1], [0x2469,0xA2E2], [0x2474,0xA2C5],  
[0x2475,0xA2C6], [0x2476,0xA2C7], [0x2477,0xA2C8], [0x2478,0xA2C9],  
[0x2479,0xA2CA], [0x247A,0xA2CB], [0x247B,0xA2CC], [0x247C,0xA2CD],  
[0x247D,0xA2CE], [0x247E,0xA2CF], [0x247F,0xA2D0], [0x2480,0xA2D1],  
[0x2481,0xA2D2], [0x2482,0xA2D3], [0x2483,0xA2D4], [0x2484,0xA2D5],  
[0x2485,0xA2D6], [0x2486,0xA2D7], [0x2487,0xA2D8], [0x2488,0xA2B1],  
[0x2489,0xA2B2], [0x248A,0xA2B3], [0x248B,0xA2B4], [0x248C,0xA2B5],  
[0x248D,0xA2B6], [0x248E,0xA2B7], [0x248F,0xA2B8], [0x2490,0xA2B9],  
[0x2491,0xA2BA], [0x2492,0xA2BB], [0x2493,0xA2BC], [0x2494,0xA2BD],  
[0x2495,0xA2BE], [0x2496,0xA2BF], [0x2497,0xA2C0], [0x2498,0xA2C1],  
[0x2499,0xA2C2], [0x249A,0xA2C3], [0x249B,0xA2C4], [0x2461,0xA2DA], 
[0x2462,0xA2DB], [0x3220,0xA2E5], [0x3221,0xA2E6], [0x3229,0xA2EE],
[0x3222,0xA2E7], [0x3223,0xA2E8], [0x3224,0xA2E9], [0x3225,0xA2EA],  
[0x3226,0xA2EB], [0x3227,0xA2EC], [0x3228,0xA2ED], [0x2160,0xA2F1],
[0xFF01,0xA3A1], [0xFF02,0xA3A2], [0xFF03,0xA3A3], [0xFF05,0xA3A5],  '''A3'''
[0xFF06,0xA3A6], [0xFF07,0xA3A7], [0xFF08,0xA3A8], [0xFF09,0xA3A9],  
[0xFF0A,0xA3AA], [0xFF0B,0xA3AB], [0xFF0C,0xA3AC], [0xFF0D,0xA3AD],  
[0xFF0E,0xA3AE], [0xFF0F,0xA3AF], [0xFF10,0xA3B0], [0xFF11,0xA3B1],  
[0xFF12,0xA3B2], [0xFF13,0xA3B3], [0xFF14,0xA3B4], [0xFF15,0xA3B5],  
[0xFF16,0xA3B6], [0xFF17,0xA3B7], [0xFF18,0xA3B8], [0xFF19,0xA3B9],  
[0xFF1A,0xA3BA], [0xFF1B,0xA3BB], [0xFF1C,0xA3BC], [0xFF1D,0xA3BD],  
[0xFF1E,0xA3BE], [0xFF1F,0xA3BF], [0xFF20,0xA3C0], [0xFF21,0xA3C1],  
[0xFF22,0xA3C2], [0xFF23,0xA3C3], [0xFF24,0xA3C4], [0xFF25,0xA3C5],  
[0xFF26,0xA3C6], [0xFF27,0xA3C7], [0xFF28,0xA3C8], [0xFF29,0xA3C9],  
[0xFF2A,0xA3CA], [0xFF2B,0xA3CB], [0xFF2C,0xA3CC], [0xFF2D,0xA3CD],  
[0xFF2E,0xA3CE], [0xFF2F,0xA3CF], [0xFF30,0xA3D0], [0xFF31,0xA3D1],  
[0xFF32,0xA3D2], [0xFF33,0xA3D3], [0xFF34,0xA3D4], [0xFF35,0xA3D5],  
[0xFF36,0xA3D6], [0xFF37,0xA3D7], [0xFF38,0xA3D8], [0xFF39,0xA3D9],  
[0xFF3A,0xA3DA], [0xFF3B,0xA3DB], [0xFF3C,0xA3DC], [0xFF3D,0xA3DD],  
[0xFF3E,0xA3DE], [0xFF3F,0xA3DF], [0xFF40,0xA3E0], [0xFF41,0xA3E1],  
[0xFF42,0xA3E2], [0xFF43,0xA3E3], [0xFF44,0xA3E4], [0xFF45,0xA3E5],  
[0xFF46,0xA3E6], [0xFF47,0xA3E7], [0xFF48,0xA3E8], [0xFF49,0xA3E9],  
[0xFF4A,0xA3EA], [0xFF4B,0xA3EB], [0xFF4C,0xA3EC], [0xFF4D,0xA3ED],  
[0xFF4E,0xA3EE], [0xFF4F,0xA3EF], [0xFF50,0xA3F0], [0xFF51,0xA3F1],  
[0xFF52,0xA3F2], [0xFF53,0xA3F3], [0xFF54,0xA3F4], [0xFF55,0xA3F5],  
[0xFF56,0xA3F6], [0xFF57,0xA3F7], [0xFF58,0xA3F8], [0xFF59,0xA3F9],  
[0xFF5A,0xA3FA], [0xFF5B,0xA3FB], [0xFF5C,0xA3FC], [0xFF5D,0xA3FD],
[0xFFE3,0xA3FE], [0xFFE5,0xA3A4]
'''
]

class DFRobot_Device:
  def __init__(self, spi, cs_W21=2, cs_GT30=4, dc=5):
    self.spi = spi
    self._DFR_W21_CS = cs_W21
    self._DFR_GT30_CS = cs_GT30
    self._DFR_W21_DC = dc
    self.DF_Display_bw = bytearray(2756)
    self.DF_Display_red = bytearray(2756)
    self._DFR_W21_CS.init(self._DFR_W21_CS.OUT, value=1)
    self._DFR_W21_CS.init(self._DFR_GT30_CS.OUT, value=1)
    self._DFR_W21_DC.init(self._DFR_W21_DC.OUT, value=1)

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
    len = len(data)
    self.wirteCmd(command)
    for i in range(len):
      self.wirteData(data[len])

  def spiRead(self, addr, len, ch):
    self._DFR_GT30_CS.value(0)
    self._DFR_W21_CS.value(1)
    for x in [(0x0b),(addr >> 16),(addr >> 8),(addr),(0x00)]:
      self.spiWriteByte(x)
    self.readinto(ch)

  def spiDelay(self, xsp):
    while xsp:
      for i in range(DFR_W21_SPI_SPEED):
        pass
      xsp=xsp-1

class DFRobot_Font:
  def __init(self):
    self._Device = DFRobot_Device()
    self._Eink = DFRobot_EInk()
  def unicodeToGB2312(self, unicode, GB2312):
    code = unicode[0]
    code = (code<<8) + unicode[1]
    if(code<0x4e00 or code>0x9FBF):
      for i in range(1000):
        if(ucs_gb2312_table[i][0] == code):
          GB2312[0] = ucs_gb2312_table[i][1]>>8
          GB2312[1] = ucs_gb2312_table[i][1]
          return True
    elif(code<0xa0):
      result=1
    elif(code<=0xf7):
      h=code-160;
    elif(code<0x2c7):
      result=1
    elif(code<=0x2c9):
      h=code-160-463;
    elif(code<0x2010):
      result=1;
    elif(code<=0x2312):
      h=code-160-463-7494;
    elif(code<0x2460):
      result=1;
    elif(code<=0x2642):
      h=code-160-463-7494-333;
    elif(code<0x3000):
      result=1;
    elif(code<=0x3017):
      h=code-160-463-7494-333-2493;
    elif(code<0x3220):
      result=1;
    elif(code<=0x3229):
      h=code-160-463-7494-333-2493-520;
    elif(code<0x4e00):
      result=1;
    elif(code<=0x9b54):
      h=code-160-463-7494-333-2493-520-7126;
    elif(code<0x9c7c):
      result=1;
    elif(code<=0x9ce2):
      h=code-160-463-7494-333-2493-520-7126-295;
    elif(code<0x9e1f):
      result=1;
    elif(code<=0x9fa0):
      h=code-160-463-7494-333-2493-520-7126-295-316;
    elif(code<0xe76c):
      result=1;
    elif(code<=0xe774):
      h=code-160-463-7494-333-2493-520-7126-295-316-18379;
    elif(code<0xff00):
      result=1;
    elif(code<=0xff5f):
      h=code-160-463-7494-333-2493-520-7126-295-316-18379-6027;
    elif(code<0xffe0):
      result=1;
    elif(code<=0xffe5):
      h=code-160-463-7494-333-2493-520-7126-295-316-18379-6027-128;
    else:
      result=1
    if(result==0):
      addr = UNICODETOGB2312_ADDR + (h<<1)
      self._Device.spiRead(addr, 2, GB2312)
    else:
      GB2312[0] = 0xa1
      GB2312[1] = 0xa1
    return True
    
  def GB2312_addr(self, ch, type):
    if(ch[0] < 0x80):
      if(ch[0] >= ord(" ")):
        temp = ch[0] - ord(" ")
      if(type == CHARACTER_TYPE_8):
        temp = temp*8  + ASC0808D2HZ_ADDR
      elif(type == CHARACTER_TYPE_12):
        temp = temp*12 + ASC0812M2ZF_ADDR 
      elif(type == CHARACTER_TYPE_16):
        temp = temp*16 + GBEX0816ZF_ADDR
    else:
      if(ch[0] >=0xA4 and ch[0] <= 0Xa8 and ch[1] >=0xA1):
        temp = JFLS1516HZ_ADDR
      elif(ch[0] >=0xA1 and ch[0] <= 0Xa9 and ch[1] >=0xA1):
        temp =( (ch[0] - 0xA1) * 94 + (ch[1] - 0xA1))*32+ JFLS1516HZBD_ADDR
      elif(ch[0] >=0xB0 and ch[0] <= 0xF7 and ch[1] >=0xA1):
        temp = ((ch[0] - 0xB0) * 94 + (ch[1] - 0xA1)+ 846)*32+ JFLS1516HZ_ADDR
      return temp
	
  def getLattice(self, gb2312, size, ch2):
    if(size == CHINESE_TYPE_1616):
      addr = self.GB2312_addr(gb2312, CHINESE_TYPE_1616)
      self._Device.spiRead(addr, 32, ch2)
    elif(size == CHARACTER_TYPE_16):
      addr = self.GB2312_addr(gb2312, CHARACTER_TYPE_16)
      self._Device.spiRead(addr, 16, ch2)
    
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
          self._Eink.drawPoint(sx, y, color)
        else:
          self._Eink.drawPoint(sx, y, LUCENCY)
        font = font<<1
        sx = sx+1
        if((sx-x)==width):
          y = y+1


class DFRobot_EInk:
  def __init__(self, spi, cs_W21=2, cs_GT30=4, dc=5):
    self._device = DFRobot_Device(spi, cs_W21, cs_GT30, dc)
    self._font = DFRobot_Font()
    eInkdev['highly'] = 104
    eInkdev['width'] = 212
    eInkdev['scandir'] = EInk_scan_Dir3
  
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
  
  def powerOn(self):
    self._device.wirteCmdData(0x06, (0x17,0x17,0x17))
    self._device.wirteCmd(0x04)      
    time.sleep(3)
    self._device.wirteCmdData(0, 0xc3|eInkdev["scandir"])    
    self._device.wirteCmdData(0x50, 0x37)
    self._device.wirteCmdData(0x30, 0x39)
    self.setWindow(212,104)
    self._device.wirteCmdData(0x82, 0x0a)
    
  def powerOff(self):
    self._device.wirteCmd(0x12)
    time.sleep(15)
    self._device.wirteCmdData(0x82, 0)
    self._device.wirteCmdData(0x01, (2,0,0,0))
    self._device.wirteCmd(0X02)
  
  def picDisplay(self, pic_bw, pic_red):
    for i in range(2756):
      self._device.DF_Display_bw[i] = pic_bw[i]
    for i in range(2756):
      self._device.DF_Display_red[i] = pic_red[i]
   
  def disRefresh(self):
    if(eInkdev["scandir"] == EInk_scan_Dir3):
      self.powerOn()
      self._device.wirteCmd(0x10)
      for i in range(2756):
        self._device.wirteData(~self._device.DF_Display_bw[i])
      self._device.wirteCmd(0x11)
      self._device.wirteCmd(0x13)
      for i in range(2756):
        self._device.wirteData(~self._device.DF_Display_red[i])
      self._device.wirteCmd(0x11)
      self.powerOff()
       
  def clear(self,color):
    if(color == WHITE):
      bw = 0x00
      red = 0x00
    elif(color == RED):
      bw = 0x00
      red = 0xff
    elif(color == BLACK):
      bw = 0xff
      red = 0x00
    else:
      print("no color!")
    for i in range(2756):
      self._device.DF_Display_bw[i]=bw
      self._device.DF_Display_red[i]=red
    self.displayRefresh()
    
  def drawPoint(self, x, y, color):
    if(x>211 or y>103 or x<0 or y<0):
      print("Out of display!")
      return False
    sx = 211-x
    sby = sx*13
    sy = (y+1)//8
    sby = sby+sy
    sy = (y+1)%8
    if(color == RED):
      if(sy):
        self._device.DF_Display_bw[sby] &= 2**(8-sy)
        self._device.DF_Display_red[sby] |= 2**(8-sy)
      else:
        self._device.DF_Display_bw[sby-1] &= 0xFE
        self._device.DF_Display_red[sby-1] |= 0x01
      return True
    elif(color == BLACK):
      if(sy):
        self._device.DF_Display_red[sby] &= 2**(8-sy)
        self._device.DF_Display_bw[sby] |= 2**(8-sy)
      else:
        self._device.DF_Display_red[sby-1] &= 0xFE
        self._device.DF_Display_bw[sby-1] |= 0x01
      return True
    elif(color == WHITE):
      if(sy):
        self._device.DF_Display_red[sby] &= 2**(8-sy)
        self._device.DF_Display_bw[sby] &= 2**(8-sy)
      else:
        self._device.DF_Display_red[sby-1] &= 0xFE
        self._device.DF_Display_bw[sby-1] &= 0xFE
      return True
    elif(color == LUCENCY):
      return True
    else:
      return False

  def drawLine(self, x1, y1, x2, y2, color):
    Status = True
    xerr=0
    yerr=0
    delta_x=x2-x1
    delta_y=y2-y1
    uRow=x1
    uCol=y1
    if(delta_x>0):
      incx=1
    elif(delta_x==0):
      incx=0
    else:
      incx=-1
      delta_x=-delta_x
    if(delta_y>0):
      incy=1
    elif(delta_y==0):
      incy=0
    else:
      incy=-1
      delta_y=-delta_y
    if(delta_x>delta_y):
      distance=delta_x
    else:
      distance=delta_y
    for i in range(distance+2):
      Status = self.drawPoint(uRow, uCol, color)
      if(not Status):
        return Status
      xerr = xerr+delta_x
      yerr = yerr+delta_y
      if(xerr>distance):
        xerr = xerr-distance
        uRow = uRow+incx
      if(yerr>distance):
        yerr = yerr-distance
        uCol = uCol+incy
    return Status
   
  def drawRectangle(self, x1, y1, x2, y2, color):
    Status = True
    Status = self.drawLine(x1,y1,x2,y1,color)
    if(not Status):
      return Status
    Status = self.drawLine(x1,y1,x1,y2,color)
    if(not Status):
      return Status
    Status = self.drawLine(x1,y2,x2,y2,color)
    if(not Status):
      return Status
    Status = self.drawLine(x2,y1,x2,y2,color)
    if(not Status):
      return Status
    return Status
  
  def rectangleFill(self, x1, y1, x2, y2, color):
    Status = True
    for sy in range(y1,y2+1):
      for sx in range(x1,x2+1):
        Status = self.drawPoint(sx, sy, color)
        if(not Status):
          return Status
    return Status
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

  def disStr(self, x, y, Str, color):
    str_null = bytearray[32]
    unicode_hz = bytearray[2]
    gb2312_hz = bytearray[2]
    len = len(Str)
    for i in range(len):
      if(ord(Str[i]) <= 127):
        self._font.getLattice(ord(Str[i]), CHARACTER_TYPE_16, str_null)
        self._font.showStr(x, y, CHINESE_TYPE_1616, str_null, color)
        x = x+8
        if(x+8 > 211):
          x = 0
          y = y+18
          if(y+16 > 103):
            y = 0
      else:
        if(((Str[i].encode('utf8')[0]) & 0xf0) == 0xe0):
          temp = (Str[i].encode('utf8')[0] & 0x0f) << 12 | (Str[i].encode('utf8')[1] & 0x3f) << 6 | (Str[i].encode('utf8')[2] & 0x3f);
          unicode_hz[0] = temp >> 8;
          unicode_hz[1] = temp
          self._font.unicodeToGB2312(unicode_hz, gb2312_hz)
          self._font.getLattice(gb2312_hz, CHINESE_TYPE_1616, str_null)
          self._font.showStr(x, y, CHINESE_TYPE_1616, str_null, color)
          x = x+16
          if(x+16 > 211):
            x = 0
            y = y+18
            if(y+16 > 103):
              y = 0
        elif(((Str[i].encode('gb2312')[0]) & 0x80) == 0x80):
          gb2312_hz[0] = Str[i].encode('gb2312')[0]
          gb2312_hz[1] = Str[i].encode('gb2312')[1]
          self._font.getLattice(gb2312_hz, CHINESE_TYPE_1616, str_null);#Getting font
          self._font.showStr(x, y, CHINESE_TYPE_1616, str_null, color);#Refresh the cache
          x = x+16
          if(x+16 > 211):
            x = 0
            y = y+18
            if(y+16 > 103):
              y = 0
        else:
          unicode_hz[0] = Str[i].encode('unicode')[0]
          unicode_hz[1] = Str[i].encode('unicode')[1]
          self._font.unicodeToGB2312(unicode_hz, gb2312_hz)
          self._font.getLattice(gb2312_hz, CHINESE_TYPE_1616, str_null);#Getting font
          self._font.showStr(x, y, CHINESE_TYPE_1616, str_null, color);#Refresh the cache
          x = x+16
          if(x+16 > 211):
            x = 0
            y = y+18
            if(y+16 > 103):
              y = 0

