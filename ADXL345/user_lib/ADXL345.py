from machine import Pin,I2C
import math
import time

device = const(0x53)
regAddress = const(0x32)
TO_READ = 6
buff = bytearray(6)

class ADXL345:
    def __init__(self,i2c,addr=device):
        self.addr = addr
        self.i2c = i2c
        b = bytearray(1)
        b[0] = 0
        self.i2c.writeto_mem(self.addr,0x2d,b)
        b[0] = 16
        self.i2c.writeto_mem(self.addr,0x2d,b)
        b[0] = 8
        self.i2c.writeto_mem(self.addr,0x2d,b)

    def get_xValue(self):
        buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ)
        x = (int(buff[1]) << 8) | buff[0]
        if x > 32767:
            x -= 65536
        return x
   
    def get_yValue(self):
        buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ)
        y = (int(buff[3]) << 8) | buff[2]
        if y > 32767:
            y -= 65536
        return y
        
    def get_zValue(self): 
        buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ)
        z = (int(buff[5]) << 8) | buff[4]
        if z > 32767:
            z -= 65536
        return z
        
    def get_xyzValue(self):
        buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ)
        x = (int(buff[1]) << 8) | buff[0]
        if x > 32767:
            x -= 65536
        y = (int(buff[3]) << 8) | buff[2]
        if y > 32767:
            y -= 65536
        z = (int(buff[5]) << 8) | buff[4]
        if z > 32767:
            z -= 65536
        return x,y,z
        
    def RP_calculate(self,x,y,z):
        roll = math.atan2(y , z) * 57.3
        pitch = math.atan2((- x) , math.sqrt(y * y + z * z)) * 57.3
        return roll,pitch
        
    def get_roll(self):
        x,y,z=self.get_xyzValue()
        roll,pitch=self.RP_calculate(x,y,z)
        return roll
        
    def get_pitch(self):
        x,y,z=self.get_xyzValue()
        roll,pitch=self.RP_calculate(x,y,z)
        return pitch 
        
    def get_RoolAndPitch(self):
        x,y,z=self.get_xyzValue()
        roll,pitch=self.RP_calculate(x,y,z)
        return roll,pitch 