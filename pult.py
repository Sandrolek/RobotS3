#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import socket
import pickle
import time
import datetime
import pygame

from utils import *
from config import *


def sendBoardCommand(cmd, param):
    sendCommand(client, cmd, param, (IP_BOARD, PORT_BOARD))

def setBoardSpeed(leftSpeed, rightSpeed):
    sendBoardCommand("speed", (leftSpeed, rightSpeed))

def callBoardWD():
    sendBoardCommand("wd", 0)


class PultReceiver(threading.Thread):
    def __init__(self, sock):
        super(PultReceiver, self).__init__()
        self.daemon = True
        self.sock = sock
        self.interval = 0.1
        self.stopped = threading.Event()

    def run(self):
        print('PultReceiver started')

        while not self.stopped.wait(self.interval):
#            print('%s Receiver: wait data...' % getDateTime())

            try:
                dataRAW = self.sock.recvfrom(1024)
                cmd, param = pickle.loads(dataRAW[0])
                addr = dataRAW[1]

#                print("%s: cmd=%s, param=%s" % (getDateTime(),cmd, param))

                if (cmd=="wd"):
                    pultReceiverWD.setCount()

            except Exception as err:
                print("%s PultReceiverWD: Error: %s" % (getDateTime(), err))

    def stop(self):
        self.stopped.set()

class PultReceiverWD(threading.Thread):
    def __init__(self):
        super(PultReceiverWD, self).__init__()
        self.daemon = True
        self.interval = 1
        self.stopped = threading.Event()
        self.count = 0

    def run(self):
        print('PultReceiverWD started')

        while not self.stopped.wait(self.interval):
#            print('%s PultReceiverWD: wait data...' % getDateTime())

            try:
                callBoardWD()

                self.count = self.count + 1
                if self.count > 3:
                    print('%s PultReceiverWD: Error: No connection, Count: %d' % (getDateTime(), self.count))
#                    Motors(0, 0)
                else:
#                    print('%s PultReceiverWD: Count: %d' % (getDateTime(), self.count))
                    pass

            except Exception as err:
                print("%s PultReceiverWD: Error: %s" % (getDateTime(), err))

    def setCount(self, param=0):
#        print('SetCount...')
        self.count = param

    def stop(self):
        self.stopped.set()

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((IP_PULT, PORT_PULT))
print("Pult started: %s on port %d..." % (IP_PULT, PORT_PULT))
client.settimeout(TIMEOUT)

#senderWD = SenderWD(client)
#senderWD.start()

pultReceiver = PultReceiver(client)
pultReceiver.start()

pultReceiverWD = PultReceiverWD()
pultReceiverWD.start()

screen = pygame.display.set_mode([640, 480])  # создаем окно программы
clock = pygame.time.Clock()
#pygame.joystick.init()

running = True

while running:
    for event in pygame.event.get():
#        print(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            print(event)

            if event.key == pygame.K_LEFT:
                setBoardSpeed(SPEED, -SPEED)
            elif event.key == pygame.K_RIGHT:
                setBoardSpeed(-SPEED, SPEED)
            elif event.key == pygame.K_UP:
                setBoardSpeed(SPEED, SPEED)
            elif event.key == pygame.K_DOWN:
                setBoardSpeed(-SPEED, -SPEED)
            elif event.key == pygame.K_SPACE:
                beep()
        elif event.type == pygame.KEYUP:
            setBoardSpeed(0,0)
        elif event.type == pygame.K_HOME:
            setBoardSpeed(0, 0)
            exit()
            running = False
            break

client.close()
sender.stop()
