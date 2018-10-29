#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import pickle
import socket


def getDateTime():
    now = datetime.datetime.now()
    return now.strftime("%d-%m-%Y %H:%M:%S")

def sendCommand(client, cmd, param, addr):
    msg = pickle.dumps([cmd, param])
    client.sendto(msg, addr)
