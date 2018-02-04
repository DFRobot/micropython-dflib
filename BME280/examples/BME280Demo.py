from machine import Pin, I2C
import time
import BME280
i2c = I2C(scl=Pin(22),sda=Pin(21), freq=10000)
bme = BME280.BME280(i2c=i2c)
while True:
  print(bme.temperature, bme.pressure, bme.humidity)
  time.sleep(1)
