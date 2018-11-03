#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rpicam
import threading
import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst
from gi.repository import GObject


class SKVideo_RPicam_Transmiter(threading.Thread):
    def __init__(self, Format, resolution, framerate, host, port):
        super(SKVideo_RPicam_Transmiter, self).__init__()
        self.daemon = True
        self.Format = Format
        self.resolution = resolution
        self.framerate = framerate
        self.host = host
        self.port = port
        self.robotCamStreamer = rpicam.RPiCamStreamer(self.Format, self.resolution, self.framerate,
                                                      (self.host, self.port), self.onFrameCallback)

    def onFrameCallback(frame):
        pass

    def run(self):
        print('SKVideo_RPi_Transmit started')
        self.robotCamStreamer.start()

    def stop_kill(self):
        print('SKVideo_RPi_Transmit stoped')
        self.robotCamStreamer.stop()
        self.robotCamStreamer.close()


class SKVideo_USB_Transmiter(threading.Thread):
    def __init__(self, device, width, height, framerate, host, port):
        super(SKVideo_USB_Transmiter, self).__init__()
        self.daemon = True

        self.device = device
        self.width = width
        self.height = height
        self.framerate = framerate
        self.host = host
        self.port = port

        # инициализация Gstreamer
        Gst.init(None)

        # Создание GStreamer pipeline
        self.pipeline = Gst.Pipeline()

        # Создание элементов
        self.src = Gst.ElementFactory.make('v4l2src')
        self.src.set_property('device', self.device)

        self.srcFilter = Gst.ElementFactory.make('capsfilter')
        self.srcCaps = Gst.caps_from_string(
            'image/jpeg, width=%d, height=%d, framerate=%d/1' % (self.width, self.height, self.framerate))
        self.srcFilter.set_property('caps', self.srcCaps)

        self.pay = Gst.ElementFactory.make('rtpjpegpay')

        self.sink = Gst.ElementFactory.make('udpsink')
        self.sink.set_property('host', self.host)
        self.sink.set_property('port', self.port)

        # Добавляем элементы в цепочку
        self.pipeline.add(self.src)
        self.pipeline.add(self.srcFilter)
        self.pipeline.add(self.pay)
        self.pipeline.add(self.sink)

        # Сединяем элементы
        self.src.link(self.srcFilter)
        self.srcFilter.link(self.pay)
        self.pay.link(self.sink)

    def onFrameCallback(frame):
        pass

    def run(self):
        print('SKVideo_USB_Transmit started')
        self.pipeline.set_state(Gst.State.PLAYING)
        print('GST pipeline PLAYING')

    def stop_kill(self):
        print('SKVideo_USB_Transmit stoped')
        self.pipeline.set_state(Gst.State.NULL)
