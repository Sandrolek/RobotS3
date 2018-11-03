#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import receiver
import threading
import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst
from gi.repository import GObject

class SKVideo_RPicam_Receiver(threading.Thread):
    def __init__(self, ip_robot, port):
        super(SKVideo_RPicam_Receiver, self).__init__()
        self.daemon = True
        self.ip_robot = ip_robot
        self.port = port
        self.recv = receiver.StreamReceiver(receiver.FORMAT_H264, (self.ip_robot, self.port))

    def onFrameCallback(frame):
        pass

    def run(self):
        print('SKVideo_RPicam_Receiver started')
        self.recv.play_pipeline()
        print('Waiting for GStream video pipline from IP:%s on PORT:%d' % (self.ip_robot, self.port))

    def stop_kill(self):
        print('SKVideo_RPicam_Receiver stoped')
        self.recv.stop_pipeline()
        self.recv.null_pipeline()


class SKVideo_USB_Receiver(threading.Thread):
    def __init__(self, port):
        super(SKVideo_USB_Receiver, self).__init__()
        self.daemon = True
        self.port = port
        # инициализация Gstreamer
        Gst.init(None)

        # Создание GStreamer pipeline
        self.pipeline = Gst.Pipeline()

        # Создание элементов
        self.src = Gst.ElementFactory.make('udpsrc')
        self.srcCaps = Gst.Caps.from_string(
            'application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)JPEG')
        self.src.set_property('caps', self.srcCaps)
        self.src.set_property('port', self.port)

        self.depay = Gst.ElementFactory.make('rtpjpegdepay')
        self.decoder = Gst.ElementFactory.make('jpegdec')
        self.videoconvert = Gst.ElementFactory.make('videoconvert')

        self.sink = Gst.ElementFactory.make('autovideosink')
        self.sink.set_property('sync', False)

        # Добавляем элементы в цепочку
        self.elemList = [self.src, self.depay, self.decoder, self.videoconvert, self.sink]
        for elem in self.elemList:
            self.pipeline.add(elem)

        # Сединяем элементы
        self.src.link(self.depay)
        self.depay.link(self.decoder)
        self.decoder.link(self.videoconvert)
        self.videoconvert.link(self.sink)

    def onFrameCallback(frame):
        pass

    def run(self):
        print('SKVideo_USB_Receiver started')
        self.pipeline.set_state(Gst.State.PLAYING)
        print('GST pipeline PLAYING')

    def stop_kill(self):
        print('SKVideo_USB_Receiver stoped')
        self.pipeline.set_state(Gst.State.NULL)
