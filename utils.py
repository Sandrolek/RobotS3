#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#импортируем нужный модули
import datetime
import pickle 
import socket

# функция для получения точной даты и времени. Возвращает соответственно дату и время
def getDateTime():
    now = datetime.datetime.now()
    return now.strftime("%d-%m-%Y %H:%M:%S")

# функция для отсылки некоего пакета данных. Получает на вход клиента, с помощбю которого отправляем сообщение,
# имя отправляемого пакета, сам пакет и IP и порт на который отправляем
def sendCommand(client, cmd, param, addr):
    msg = pickle.dumps([cmd, param])
    client.sendto(msg, addr)
