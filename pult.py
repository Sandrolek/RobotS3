#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import socket
import pickle
import time
import datetime
import joystick
#import pygame

from utils import *
from config import *
import joy

# Функция, отправляющая пакет данных на борт.
# Принимает на вход имя пакета данных и сам пакет
def sendBoardCommand(cmd, param):
    sendCommand(socket_server, cmd, param, (IP_BOARD, PORT_BOARD))

def sendBoardCommandWD(cmd, param):
    sendCommand(socket_server_wd, cmd, param, (IP_BOARD, PORT_BOARD_WD))

# Функция - callback отправки скорости
def setBoardSpeed(leftSpeed, rightSpeed):
    sendBoardCommand("speed", (leftSpeed, rightSpeed))

# Функция WD, отправляющая сообщение об обнулении счетчика WD
def callBoardWD():
    sendBoardCommandWD("wd", 0)

# Класс, принимающий и распаковывающий сообщения от борта
class PultReceiver(threading.Thread):
    def __init__(self, sock):
        super(PultReceiver, self).__init__()
        self.daemon = True
        self.socket_server = sock
        self.interval = 0.1
        self.stopped = threading.Event()

    def run(self):
        print('PultReceiver started')

        while not self.stopped.wait(self.interval): # Цикл, тикающий раз в 0.1 сек
#            print('%s Receiver: wait data...' % getDateTime())

            try:
                dataRAW = self.socket_server.recvfrom(1024) # ожидание получения сообщения
                cmd, param = pickle.loads(dataRAW[0]) #распаковка полученного сообщения

                if (cmd != ""):
                    print("%s: PultReceiver: cmd=%s, param=%s" % (getDateTime(),cmd, param))

            except Exception as err:
                print("%s PultReceiver: Error: %s" % (getDateTime(), err))

    def stop(self):
        self.stopped.set()

# Класс, принимающий и распаковывающий сообщения от борта
class PultReceiverWD(threading.Thread):
    def __init__(self, sock):
        super(PultReceiverWD, self).__init__()
        self.daemon = True
        self.socket_server = sock
        self.interval = 0.1
        self.stopped = threading.Event()

    def run(self):
        print('PultReceiverWD started')

        while not self.stopped.wait(self.interval): # Цикл, тикающий раз в 0.1 сек
#            print('%s Receiver: wait data...' % getDateTime())

            try:
                dataRAW = self.socket_server.recvfrom(1024) # ожидание получения сообщения
                cmd, param = pickle.loads(dataRAW[0]) #распаковка полученного сообщения
#                print("%s: cmd=%s, param=%s" % (getDateTime(),cmd, param))

                if (cmd=="wd"): # Получение сообщения, обнуляющего счетчик WD на пульте
                                # тут надо добавлять в проверку КАЖДУЮ валидную команду и обнулять WD
                    pultCountWD.setCount()
                else:
                    print("%s: PultReceiverWD: Wrong command: cmd=%s, param=%s" % (getDateTime(),cmd, param))

            except Exception as err:
                print("%s PultReceiverWD: Error: %s" % (getDateTime(), err))

    def stop(self):
        self.stopped.set()

class PultSenderWD(threading.Thread):
    def __init__(self):
        super(PultSenderWD, self).__init__()
        self.daemon = True
        self.interval = 0.1
        self.stopped = threading.Event()

    def run(self):
        print('PultSenderWD started')

        while not self.stopped.wait(self.interval): # Цикл, тикающий раз в 0.1 сек
#            print('%s Receiver: wait data...' % getDateTime())
            try:
                callBoardWD() # вызов функции, обнуляющей счетчик WD на борте (раньше вызывали из симметричного PultReceiverWD)
                pass

            except Exception as err:
                print("%s PultSenderWD: Error: %s" % (getDateTime(), err))

    def stop(self):
        self.stopped.set()

# Класс - WatchDog пульта
class PultCountWD(threading.Thread):
    def __init__(self):
        super(PultCountWD, self).__init__()
        self.daemon = True
        
        self.interval = WD_INTERVAL
        self.stopped = threading.Event()
        self.count = 0

    def run(self):
        print('PultCountWD started')

        while not self.stopped.wait(self.interval): # Цикл, тикающий 1 раз в сек
#            print('%s PultReceiverWD: wait data...' % getDateTime())

            try:
                self.count = self.count + 1
                if self.count > WD_COUNT: # если счетчик больше заданного порога
                    print('%s PultCountWD: Error: No connection, Count: %d' % (getDateTime(), self.count))
                else:
#                    print('%s PultReceiverWD: Count: %d' % (getDateTime(), self.count))
                    pass

            except Exception as err:
                print("%s PultCountWD: Error: %s" % (getDateTime(), err))

    def setCount(self, param=0): # Функция, обнуляющая счетчик
#        print('SetCount...')
        if (param == 0 and self.count > WD_COUNT):  # если счетчик хотят обнулить и счетчик больше заданного порога, то сообщаем о восстановлении соединения с пультом
            print("%s PultCountWD: Connection restored" % (getDateTime()))

        self.count = param

    def stop(self):
        self.stopped.set()

# создание socket-сервера
socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_server.bind((IP_PULT, PORT_PULT))
socket_server.settimeout(TIMEOUT)
print("Pult started: %s on port %d..." % (IP_PULT, PORT_PULT))

socket_server_wd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_server_wd.bind((IP_PULT, PORT_PULT_WD))
socket_server_wd.settimeout(TIMEOUT)
print("Pult WD started: %s on port %d..." % (IP_PULT, PORT_PULT_WD))

# создание экземпляров классов и запуск соответствующих потоков
pultReceiver = PultReceiver(socket_server)
pultReceiver.start()

pultReceiverWD = PultReceiverWD(socket_server_wd)
pultReceiverWD.start()

pultSenderWD = PultSenderWD()
pultSenderWD.start()

pultCountWD = PultCountWD()
pultCountWD.start()

j = joystick.Joystick()
j.open("/dev/input/js0")
time.sleep(2)
j.info()
j.start()

joy1 = joy.Joyst(j, socket_server)
joy1.start()

running = True

while running: # главный цикл программы
    time.sleep(0.1)

# остановка всех потоков
client.close()
pultReceiverWD.stop()
pultReceiver.stop()
