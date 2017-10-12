#  Servo Library for Micropython

---------------------------------------------------------

Provide an Arduino library to control the e-ink screen display, via SPI communication.

## Table of Contents

* [Summary](#summary)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)

## Summary

提供一个基本的舵机库，对外提供转动角度、转动速度接口，可以在ESP32，ESP8266板子上运行。
这个库基于硬件PWM运行，每个舵机都要占用一个支持硬件PWM的数字IO

## Methods

```Py
    Servo(pin)
    angle(ang)
    read()
    _map(x,inMin,inMax,outMin,outMax)
    deinit()
    pwm
```

## Compatibility

MCU                | Work Well | Work Wrong | Untested  | Remarks
------------------ | :----------: | :----------: | :---------: | -----
FireBeetle-ESP32  |      √       |             |            | 
FireBeetle-ESP8266  |      √       |             |            | 
pyboard |             |             |     √       | 

## History

- Sep 29, 2017 - Version 0.1 released.

## Credits

Written by lixin(1035868977@qq.com), 2017. (Welcome to our [website](https://www.dfrobot.com/))
