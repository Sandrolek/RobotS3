#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import socket
import pickle
import time
import datetime
import RPiPWM

from utils import *
from config import *

# Функция, отправляющая пакет данных на пульт
# Принимает на вход название пакета и его самого 
def sendPultCommand(cmd, param):
    sendCommand(socket_server_wd, cmd, param, (IP_PULT, PORT_PULT_WD))

# Функция - callback Watchdog-а, вызывает отсылающую функцию
def callPultWD():
    sendPultCommand("wd", 0)

# Класс, принимающий и распаковывающий сообщение от пульта
class BoardReceiver(threading.Thread):
    def __init__(self, sock):
        super(BoardReceiver, self).__init__()
        self.daemon = True
        self.socket_server = sock
        self.interval = 0.1
        self.stopped = threading.Event()

    def run(self):
        print('BoardReceiver started')

        while not self.stopped.wait(self.interval): # Цикл, тикающий 1 раз в 0.1 сек
#            print('%s Receiver: wait data...' % getDateTime())

            try:
                dataRAW = self.socket_server.recvfrom(1024) # ожидание получения сообщения
                cmd, param = pickle.loads(dataRAW[0]) # распаковка полученного сообщения

#                print("%s Receiver: cmd=%s, param=%s" % (getDateTime(),cmd, param))
                
                if (cmd=="wd"): # Получение сообщения, обнуляещего счетчик WD на борте
                    boardReceiverWD.setCount()
                elif (cmd=="speed"):
                    lS = param[0]
                    rS = param[1]
                    print("%s BoardReceiver: leftSpeed = %s rightSpeed = %s" % (getDateTime(), lS, rS))
                    Motors(lS, rS)
                elif (cmd=="s1_up"):
                    print("s1_up")
                    MotorServo1(1)
                elif (cmd=="s1_down"):
                    print("s1_down")
                    MotorServo1(-1)
                elif (cmd=="s2_up"):
                    print("s2_up")
                    MotorServo2(1)
                elif (cmd=="s2_down"):
                    print("s2_down")
                    MotorServo2(-1)
                elif (cmd=="s3_up"):
                    print("s3_up")
                    MotorServo3(1)
                elif (cmd=="s3_down"):
                    print("s3_down")
                    MotorServo3(-1)

            except Exception as err:
                print("%s BoardReceiver: Error: %s" % (getDateTime(), err))

    def stop(self):
        self.stopped.set()


class BoardReceiverWD(threading.Thread):
    def __init__(self, sock):
        super(BoardReceiverWD, self).__init__()
        self.daemon = True
        self.socket_server = sock
        self.interval = 0.1
        self.stopped = threading.Event()

    def run(self):
        print('BoardReceiverWD started')

        while not self.stopped.wait(self.interval):  # Цикл, тикающий 1 раз в 0.1 сек
            #            callPultWD() # вызов функции, обнуляющей счетчик WD на пульте

            try:
                dataRAW = self.socket_server.recvfrom(1024)  # ожидание получения сообщения
                cmd, param = pickle.loads(dataRAW[0])  # распаковка полученного сообщения
                #                print("%s Receiver: cmd=%s, param=%s" % (getDateTime(),cmd, param))

                if (cmd == "wd"):  # Получение сообщения, обнуляещего счетчик WD на борте
                    boardCountWD.setCount()

            except Exception as err:
                print("%s BoardReceiverWD: Error: %s" % (getDateTime(), err))

    def stop(self):
        self.stopped.set()


class BoardSenderWD(threading.Thread):
    def __init__(self):
        super(BoardSenderWD, self).__init__()
        self.daemon = True
        self.interval = 0.1
        self.stopped = threading.Event()

    def run(self):
        print('BoardSenderWD started')

        while not self.stopped.wait(self.interval):
            try:
                callPultWD()  # вызов функции, обнуляющей счетчик WD на пульте
                pass

            except Exception as err:
                print("%s BoardSenderWD: Error: %s" % (getDateTime(), err))

    def stop(self):
        self.stopped.set()

# Класс - Watchdog борта
class BoardCountWD(threading.Thread):
    def __init__(self):
        super(BoardCountWD, self).__init__()
        self.daemon = True
        self.interval = WD_INTERVAL
        self.stopped = threading.Event()
        self.count = 0

    def run(self):
        print('BoardCountWD started')

        while not self.stopped.wait(self.interval): # Цикл, тикающий 1 раз в сек
#            print('%s ReceiverWD: wait data...' % getDateTime())

            try:
                self.count = self.count + 1
                if self.count > WD_COUNT: # если счетчик больше заданного порога
                    print('%s BoardCountWD: Error: No connection, Count: %d' % (getDateTime(), self.count))
                    Motors(0, 0)
                else:
#                    print('%s BoardReceiverWD: Count: %d' % (getDateTime(), self.count))
                    pass

            except Exception as err:
                print("%s BoardCountWD: Error: %s" % (getDateTime(), err))

    # Функция, обнуляющая счетчик, если появился сигнал от пульта
    def setCount(self, param = 0):
#        print('SetCount...')

        if (param == 0 and self.count > WD_COUNT): # если счетчик хотят обнулить и счетчик больше заданного порога, то сообщаем о восстановлении соединения с пультом
            print("%s BoardCountWD: Connection restored" % (getDateTime()))

        self.count = param 

    def stop(self):
        self.stopped.set()

# Порты моторов
chanRevMotorL = 12
chanRevMotorR = 13

# создаем объекты моторов
motorL = RPiPWM.ReverseMotor(chanRevMotorL)
motorR = RPiPWM.ReverseMotor(chanRevMotorR)

def Motors(leftSpeed, rightSpeed):
    motorL.setValue(leftSpeed)
    motorR.setValue(rightSpeed)

curServo1 = 0
curServo2 = 0
curServo3 = 0
curLights = 0

chanServo1_180 = 9
chanServo2_180 = 10
chanServo3_180 = 11

servo1_180 = RPiPWM.Servo180(chanServo1_180, extended=True)
servo2_180 = RPiPWM.Servo180(chanServo2_180, extended=True)
servo3_180 = RPiPWM.Servo180(chanServo3_180, extended=True)

print("Servo channels: Servo180_1 - %d, Servo180_2 - %d, Servo180_3 - %d" % (chanServo1_180, chanServo2_180, chanServo3_180))

def MotorServo3(directServo):
    s3 = servo3_180.getValue()

    global curServo3
    curServo3 = s3

    if directServo == 1:
        s3 = s3 + 50
        if s3 > 2250:
            s3 = 2250
    else:
        if directServo == -1:
            s3 = s3 - 50
            if s3 < 900:
                s3 = 900
#    print('valueServo3: %s' % (s3))
    servo3_180.SetMcs(s3)

    return 0

def MotorServo2(directServo):
    s2 = servo2_180.getValue()

    global curServo2
    curServo2 = s2

    if directServo == 1:
        s2 = s2 + 50
        if s2 > 2500:
            s2 = 2500
    else:
        if directServo == -1:
            s2 = s2 - 50
            if s2 < 900:
                s2 = 900
#    print('valueServo2: %s' % (s2))
    servo2_180.SetMcs(s2)

    return 0

def MotorServo1(directServo):
    s1 = servo1_180.getValue()

    global curServo1
    curServo1 = s1

    if directServo == 1:
        s1 = s1 + 50
        if s1 > 2100:
            s1 = 2100
    else:
        if directServo == -1:
            s1 = s1 - 50
            if s1 < 900:
                s1 = 900

#    print('valueServo1: %d' % (s1))
    servo1_180.SetMcs(s1)

    return 0

def LightsOnOff(turnOnOff):
    global curLights
    curLights = turnOnOff

    print("Lights: %d" % turnOnOff)
    lights.setValue(turnOnOff)

    return 0

# создание socket-сервера 
socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_server.bind((IP_BOARD, PORT_BOARD))
socket_server.settimeout(TIMEOUT)
print("Board started: %s on port %d..." % (IP_BOARD, PORT_BOARD))

# создание socket-сервера
socket_server_wd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_server_wd.bind((IP_BOARD, PORT_BOARD_WD))
socket_server_wd.settimeout(TIMEOUT)
print("Board WD started: %s on port %d..." % (IP_BOARD, PORT_BOARD_WD))

# создание экземпляров классов и запуск соответствующих потоков
boardReceiver = BoardReceiver(socket_server)
boardReceiver.start()

boardReceiverWD = BoardReceiverWD(socket_server_wd)
boardReceiverWD.start()

boardSenderWD = BoardSenderWD()
boardSenderWD.start()

boardCountWD = BoardCountWD()
boardCountWD.start()

running = True

while running: # главный цикл
    time.sleep(0.1)

# остановка всех потоков и сервера
socket_server.close()
receiver.stop()
boardReceiverWD.stop()
Motors(0,0)
