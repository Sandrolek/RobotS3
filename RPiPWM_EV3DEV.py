import time
from enum import IntEnum   # для создания нумерованных списков
import math
import threading

import evdev
import ev3dev.auto as ev3

from config import *

class PwmFreq(IntEnum):     # список возможных частот работы
    H50 = 50                # 50 Гц
    H125 = 125              # 125 Гц
    H250 = 250              # 250 Гц

class PwmBase:
    """Базовый класс для управления драйвером ШИМ (PCA9685)"""
    def __init__(self, channel: int, mode, freq=PwmFreq.H50, extended=False):
        self._channel = channel
        self._mode = mode
        self._extended = extended
        self._value = 0     # значение, которе установлено на канале

    def setMcs(self, value: int):
        pass

    def getMcs(self):
        return 1

    def getValue(self):
        return self._value

    def setValue(self, value: int):  # устанавливаем значение
        pass

class Servo90(PwmBase):
    """Класс для управления сервой 90 град"""
    def __init__(self, channel, freq=PwmFreq.H50, extended=False):
        pass

class Servo120(PwmBase):
    """Класс для управления сервой 120 град"""
    def __init__(self, channel, freq=PwmFreq.H50, extended=False):
        pass

class Servo180(PwmBase):
    def __init__(self, channel, freq=PwmFreq.H50, extended=False):
        PwmBase.__init__(self, channel, freq, extended)
        if self._channel == 9:
            self.servo1_180 = ev3.LargeMotor(ev3.OUTPUT_C)

    def setMcs(self, value: int):
        if self._value < value:
            pos = STEP_1
        elif self._value > value:
            pos = -STEP_1
        else:
            pos = 0

        self._value = value

        if self._channel == 9:
            self.servo1_180.run_to_rel_pos(position_sp=pos, speed_sp=200, stop_action='hold')

class Servo270(PwmBase):
    """Класс для управления сервой 270 град"""
    def __init__(self, channel, freq=PwmFreq.H50, extended=False):
        pass

class ReverseMotor(PwmBase):
    """Класс для управления мотором с реверсом"""
    def __init__(self, channel, freq=PwmFreq.H50, extended=False):
        PwmBase.__init__(self, channel, freq, extended)
#        print("Channel=%d" % self._channel)
        if self._channel == 12:
            self.motor = ev3.LargeMotor(ev3.OUTPUT_B)
        elif self._channel == 13:
            self.motor = ev3.LargeMotor(ev3.OUTPUT_A)
        else:
            pass

    def setValue(self, value: int):  # устанавливаем значение
        speed = value * -1
#        print("Channel=%d, SPEED=%d" % (self._channel, speed))
        self.motor.run_direct(duty_cycle_sp=speed)
