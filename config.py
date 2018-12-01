#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Сокеты =================
IP_BOARD        = '192.168.1.140'
PORT_BOARD      = 6000
PORT_BOARD_WD   = 6001

IP_PULT         = '192.168.1.113'
PORT_PULT       = 6010
PORT_PULT_WD    = 6011

# Channels

CH_LEFT     = 12    # левый ведущий
CH_RIGHT    = 13    # правый ведущий
CH_SERVO1   = 9     # первый рычаг
CH_SERVO2   = 10    # второй рычаг
CH_SERVO3   = 11    # клешня
CH_SERVO4   = 12    # вращение

# Timeout
TIMEOUT = 60

# Скорость
# SPEED = 100

# WhatchDog
WD_INTERVAL = 1
WD_COUNT = 2

# Speed
BASE_SPEED = 100
SPEED_0 = 30
SPEED_1 = 50
SPEED_2 = 100

# Servo
STEP_1 = 10
STEP_2 = 10
STEP_3 = 5


SERVO_INTERVAL = 0.1

# Raspberry
'''
SERVO_1_START = 1500
SERVO_1_MAX = 2100
SERVO_1_MIN = 900
SERVO_2_START = 1500
SERVO_2_MAX = 2500
SERVO_2_MIN = 900
SERVO_3_START = 1500
SERVO_3_MAX = 2250
SERVO_3_MIN = 900
'''

# EV3DEV
SERVO_1_START = 0
SERVO_1_MAX = 1000
SERVO_1_MIN = 0
SERVO_2_START = 0
SERVO_2_MAX = 1000
SERVO_2_MIN = 0
SERVO_3_START = 0
SERVO_3_MAX = 1000
SERVO_3_MIN = 0
