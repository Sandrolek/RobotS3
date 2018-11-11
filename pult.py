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
    sendCommand(client, cmd, param, (IP_BOARD, PORT_BOARD))

# Функция - callback отправки скорости
def setBoardSpeed(leftSpeed, rightSpeed):
    sendBoardCommand("speed", (leftSpeed, rightSpeed))

# Функция WD, отправляющая сообщение об обнулении счетчика WD
def callBoardWD():
    sendBoardCommand("wd", 0)

# Класс, принимающий и распаковывающий сообщения от борта
class PultReceiver(threading.Thread):
    def __init__(self, sock):
        super(PultReceiver, self).__init__()
        self.daemon = True
        self.sock = sock
        self.interval = 0.1
        self.stopped = threading.Event()

    def run(self):
        print('PultReceiver started')

        while not self.stopped.wait(self.interval): # Цикл, тикающий раз в 0.1 сек
#            print('%s Receiver: wait data...' % getDateTime())

            callBoardWD() # вызов функции, обнуляющей счетчик WD на борте (раньше вызывали из симметричного PultReceiverWD)

            try:
                dataRAW = self.sock.recvfrom(1024) # ожидание получения сообщения
                cmd, param = pickle.loads(dataRAW[0]) #распаковка полученного сообщения
                addr = dataRAW[1]

#                print("%s: cmd=%s, param=%s" % (getDateTime(),cmd, param))

                if (cmd=="wd"): # Получение сообщения, обнуляющего счетчик WD на пульте
                                # тут надо добавлять в проверку КАЖДУЮ валидную команду и обнулять WD
                    pultReceiverWD.setCount()

            except Exception as err:
                print("%s PultReceiverWD: Error: %s" % (getDateTime(), err))

    def stop(self):
        self.stopped.set()

# Класс - WatchDog пульта
class PultReceiverWD(threading.Thread):
    def __init__(self):
        super(PultReceiverWD, self).__init__()
        self.daemon = True
        
        self.interval = WD_INTERVAL
        self.stopped = threading.Event()
        self.count = 0

    def run(self):
        print('PultReceiverWD started')

        while not self.stopped.wait(self.interval): # Цикл, тикающий 1 раз в сек
#            print('%s PultReceiverWD: wait data...' % getDateTime())

            try:
                self.count = self.count + 1
                if self.count > WD_COUNT: # если счетчик больше заданного порога
                    print('%s PultReceiverWD: Error: No connection, Count: %d' % (getDateTime(), self.count))
#                    Motors(0, 0)
                else:
#                    print('%s PultReceiverWD: Count: %d' % (getDateTime(), self.count))
                    pass

            except Exception as err:
                print("%s PultReceiverWD: Error: %s" % (getDateTime(), err))

    def setCount(self, param=0): # Функция, обнуляющая счетчик
#        print('SetCount...')
        self.count = param

    def stop(self):
        self.stopped.set()

# создание socket-сервера
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((IP_PULT, PORT_PULT))
print("Pult started: %s on port %d..." % (IP_PULT, PORT_PULT))
client.settimeout(TIMEOUT)

#senderWD = SenderWD(client)
#senderWD.start()

# создание экземпляров классов и запуск соответствующих потоков
pultReceiver = PultReceiver(client)
pultReceiver.start()

pultReceiverWD = PultReceiverWD()
pultReceiverWD.start()

j = joystick.Joystick()
j.open("/dev/input/js0")
time.sleep(2)
j.info()
j.start()

joy1 = joy.Joyst(j, client)
joy1.start()

running = True

while running: # главный цикл программы
    time.sleep(0.1)

# остановка всех потоков
client.close()
pultReceiverWD.stop()
pultReceiver.stop()
