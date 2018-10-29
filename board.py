#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import socket
import pickle
import time
import datetime

from utils import *
from config import *

# Функция, отправляющая пакет данных на пульт
# Принимает на вход название пакета и его самого 
def sendPultCommand(cmd, param):
    sendCommand(server, cmd, param, (IP_PULT, PORT_PULT))

# Функция - callback Watchdog-а, вызывает отсылающую функцию
def callPultWD():
#    print("callPultWD")
    sendPultCommand("wd", 0)

# Класс, распаковывающий сообщение от борта
class Receiver(threading.Thread):
    def __init__(self, sock):
        super(Receiver, self).__init__()
        self.daemon = True
        self.sock = sock
        self.interval = 0.1
        self.stopped = threading.Event()

    def run(self):
        print('Receiver started')

        while not self.stopped.wait(self.interval): # Цикл, тикающий 1 раз в 0.1 сек
#            print('%s Receiver: wait data...' % getDateTime())

            try:
                dataRAW = self.sock.recvfrom(1024) # попытка получения сообщения
                cmd, param = pickle.loads(dataRAW[0]) # распаковка полученного сообщения
                addr = dataRAW[1]

#                print("%s: cmd=%s, param=%s" % (getDateTime(),cmd, param))
                
                if (cmd=="wd"): # обработка "обнуляещего" сообщения от борта
                    boardReceiverWD.setCount()

            except Exception as err:
                print("%s Receiver: Error: %s" % (getDateTime(), err))

    def stop(self):
        self.stopped.set()

# Класс - Watchdog
class BoardReceiverWD(threading.Thread):
    def __init__(self):
        super(BoardReceiverWD, self).__init__()
        self.daemon = True
        self.interval = 1
        self.stopped = threading.Event()
        self.count = 0

    def run(self):
        print('BoardReceiverWD started')

        while not self.stopped.wait(self.interval): # Цикл, тикающий раз в сек
#            print('%s ReceiverWD: wait data...' % getDateTime())

            try:
                callPultWD() # вызов функции, отправляющей борту "обнуляющего" сообщения

                self.count = self.count + 1
                if self.count > 3: # если юольше 3 секунд нет сигнала от борта
                    print('%s BoardReceiverWD: Error: No connection, Count: %d' % (getDateTime(), self.count))
#                    Motors(0, 0)
                else:
#                    print('%s BoardReceiverWD: Count: %d' % (getDateTime(), self.count))
                    pass

            except Exception as err:
                print("%s BoardReceiverWD: Error: %s" % (getDateTime(), err))

    # Функция, обнуляющая счетчик, если появился сигнал от борта
    def setCount(self, param = 0):
#        print('SetCount...')

        if (param == 0 and self.count > 3):
            print("BoardReceiverWD: Connection restored")

        self.count = param # обнуление счетчика

    def stop(self):
        self.stopped.set()

# создание сервера 
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((IP_BOARD, PORT_BOARD))

print("Board started: %s on port %d..." % (IP_BOARD, PORT_BOARD))
server.settimeout(TIMEOUT)

# создание экземпляров классов 
receiver = Receiver(server)
receiver.start()

boardReceiverWD = BoardReceiverWD()
boardReceiverWD.start()

running = True

while running: # главный цикл
    pass

# остановка всех потоков и сервера
server.close()
receiver.stop()
boardReceiverWD.stop()
