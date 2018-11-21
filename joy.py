#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import time

import joystick

from utils import *
from config import *


class Joyst(threading.Thread):
    def __init__(self, j, client):
        super(Joyst, self).__init__()
        self.daemon = True
        self.stopped = threading.Event()
        
        self.j = j
        self.client = client
        
        self.leftSpeed = 0
        self.rightSpeed = 0
        self.lastRightSp = 0
        self.lastLeftSp = 0
        self.SPEED = 100
        self.speedChange = False

        #инициализируем переменные значения кнопок и их названия (и то же самое для стиков) 
        self.hatX = 0.0
        self.hatY = 0.0
        self.turning = 'hat0x'
        self.direct = 'hat0y'
        self.startTrans = 'start'
        self.btnA = 'a'
        self.btnY = 'y'
        self.btnX = 'x'
        self.btnB = 'b'
        self.btnTr = 'tr'
        self.btnTl = 'tl'
        self.btnThumbl = 'thumbl'

        #8 axes found:
        # x, y: левый стик по Х и Y, z:левый курок, база на -1 (-1...1),
        # rx, ry:правый стик по X и Y, rz:правый курок, база на -1 (-1...1),
        # hat0x, hat0y
        #11 buttons found: a, b, x, y,
        # tl, tr:торцевай кнопка,
        # select, start, mode,
        # thumbl, thumbr: клик на стик


        self.hatXOld = 0.0
        self.hatYOld = 0.0
        self.BASE_SPEED = 100
        self.SPEED_0 = 30
        self.SPEED_1 = 50
        self.SPEED_2 = 100
        self.speedChange = False

        self.bA=0
        self.bAOld=0
        self.servoAChange=False
        self.bY=0
        self.bYOld=0
        self.servoYChange=False

        self.bX=0
        self.bXOld=0
        self.servoXChange=False
        self.bB=0
        self.bBOld=0
        self.servoBChange=False

        self.bTr = 0

        self.bTl = 0
        self.bTlOld = 0
        self.count_bTl = 0

        self.bThumbl = 0
        self.bThumblOld = 0
        self.lightsChange = False
        self.lightsValue = False

        self.speedCur = self.SPEED_1

    def onBtnThumbl(self, value):
        print("btnThumbl=%s" % value)

        if self.bThumbl == 0 and self.bThumblOld == 1:
            self.bThumblOld = 0
            self.lightsChange = False
        elif self.bThumbl == 1 and self.bThumblOld == 1:
                self.lightsChange = False
        elif self.bThumbl == 1 and self.bThumblOld == 0:
            self.bThumblOld = 1
            self.lightsValue = not self.lightsValue
            self.lightsChange = True

    def onBtnTl(self, value):
        print("btnTl=%s" % value)

        if self.bTl == 0 and self.bTlOld == 1:
            self.bTlOld = 0

            self.count_bTl = self.count_bTl + 1
            if self.count_bTl > 2:
                self.count_bTl = 0

            if self.count_bTl == 0:
                self.speedCur = self.SPEED_0
            elif self.count_bTl == 1:
                self.speedCur = self.SPEED_1
            elif self.count_bTl == 2:
                self.speedCur = self.SPEED_2
            print('speedCur = %d' % self.speedCur)
        elif self.bTl == 1 and self.bTlOld == 0:
            self.bTlOld = 1

    def onBtnTr(self, value):
        print("btnTr=%s" % value)

    def onBtnY(self, value):
        print("btnY=%s" % value)

        self.bY = value  # Серва 1 или 2: вверх
        if self.bY != self.bYOld or self.bY == 1:
            if self.bY == 1:
                self.servoYChange = True
            #            print('btnY = %d' % (bY))
            self.bYOld = self.bY

    def onBtnA(self, value):
        print("btnA=%s" % value)
        self.bA = value # Серва 1 или 2: вниз
        if self.bA != self.bAOld or self.bA == 1:
            if self.bA == 1:
                self.servoAChange = True
#            print('btnA = %d' % (bA))
            self.bAOld = self.bA

    def onBtnX(self, value):
        print("btnX=%s" % value)

        self.bX = value  # Серва 3:
        if self.bX != self.bXOld or self.bX == 1:
            if self.bX == 1:
                self.servoXChange = True
            #            print('btnX = %d' % (bX))
            self.bXOld = self.bX

    def onBtnB(self, value):
        print("btnB=%s" % value)

        self.bB = value  # Серва 3:
        if self.bB != self.bBOld or self.bB == 1:
            if self.bB == 1:
                self.servoBChange = True
            #            print('btnB = %d' % (bB))
            self.bBOld = self.bB

    def sendBoardCommand(self, cmd, param):
        sendCommand(self.client, cmd, param, (IP_BOARD, PORT_BOARD))
    
    def run(self):
        print('Joystick started')

        self.j.onButtonClick("thumbl", self.onBtnThumbl)
        self.j.onButtonClick("tl", self.onBtnTl)
        self.j.onButtonClick("tr", self.onBtnTr)
        self.j.onButtonClick("y", self.onBtnY)
        self.j.onButtonClick("a", self.onBtnA)
        self.j.onButtonClick("x", self.onBtnX)
        self.j.onButtonClick("b", self.onBtnB)

        while True:
            try:
                self.hatX = self.j.axis.get(self.turning)
                self.hatY = self.j.axis.get(self.direct)

                if self.hatX != self.hatXOld:
        #            print((hatX, hatXOld))
                    if self.hatX != 0:
                        self.leftSpeed = round(self.hatX * self.speedCur)
                        self.rightSpeed = round(-self.hatX * self.speedCur)
                    else:
                        self.leftSpeed = 0
                        self.rightSpeed = 0
                    self.speedChange = True
                    self.hatXOld = self.hatX

                elif self.hatY != self.hatYOld:
                    if self.hatY != 0:
                        self.leftSpeed = round(self.hatY * self.speedCur)
                        self.rightSpeed = round(self.hatY * self.speedCur)
                    else:
                        self.leftSpeed = 0
                        self.rightSpeed = 0
                    self.speedChange = True
                    self.hatYOld = self.hatY

                if self.lightsChange:
                    self.lightsChange = False
#                        print(self.lightsValue)
#                        s.LightsOnOff(lightsValue)

                if self.speedChange:
                    self.speedChange = False
                    print('leftM=%d, rightM=%d' % (self.leftSpeed, self.rightSpeed))
                    self.sendBoardCommand('speed', (self.leftSpeed, self.rightSpeed))

                if self.servoYChange:
                    self.servoYChange = False
                    if self.bTr == 1:
                        self.sendBoardCommand('s2_up', 0) # Поднимаем 2-у серву, т.к. прижат курок
                    else:
                        self.sendBoardCommand('s1_up', 0) # Поднимаем 1-ю серву

                if self.servoAChange:
                    self.servoAChange = False
                    if self.bTr == 1:
                        print('S2 DOWN')
                        self.sendBoardCommand('s2_down', 0) # Поднимаем 2-у серву, т.к. прижат курок
                    else:
                        self.sendBoardCommand('s1_down', 0) # Поднимаем 2-ю серву

                if self.servoXChange:
                    self.servoXChange = False
                    self.sendBoardCommand('s3_up', 0) # Серва 3

                if self.servoBChange:
                    self.servoBChange = False
                    self.sendBoardCommand('s3_down', 0) # Серва 3

            except (Exception) as err:
                print("%s Error: %s" % (getDateTime(), err))

            except(KeyboardInterrupt, SystemExit):
                print('Ctrl+C pressed')
                self.j.exit()
            
            time.sleep(0.1)

    def stop(self):
        self.stopped.set()