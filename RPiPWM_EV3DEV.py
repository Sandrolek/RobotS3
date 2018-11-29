import time
from enum import IntEnum   # для создания нумерованных списков
import math
import threading

import evdev
import ev3dev.auto as ev3

class _PwmMode(IntEnum):    # список режимов работы
    servo90 = 90            # серва 90 градусов
    servo120 = 120          # серва 120 градусов
    servo180 = 180          # серва 180 градусов
    servo270 = 270          # серва 270 градусов
    forwardMotor = 100      # мотор без реверса
    reverseMotor = 4        # мотор с реверсом
    onOff = 5               # вкл/выкл пина

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
        return 1

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
        pass

class Servo270(PwmBase):
    """Класс для управления сервой 270 град"""
    def __init__(self, channel, freq=PwmFreq.H50, extended=False):
        pass

class ReverseMotor(PwmBase):
    """Класс для управления мотором с реверсом"""
    def __init__(self, channel, freq=PwmFreq.H50, extended=False):
        print("Channel=%d" % channel)

        if channel == 12:
            self.motor = ev3.LargeMotor(ev3.OUTPUT_B)
        elif channel == 13:
            self.motor = ev3.LargeMotor(ev3.OUTPUT_A)
        else:
            pass

    def setValue(self, value: int):  # устанавливаем значение
        speed = value * -1
        self.motor.run_direct(duty_cycle_sp=speed)
