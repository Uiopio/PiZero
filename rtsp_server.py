#!/usr/bin/env python
# -*- coding:utf-8 vi:ts=4:noexpandtab
# Simple RTSP server. Run as-is or with a command-line to replace the default pipeline

import os
import gi
import threading
import time
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

loop = GLib.MainLoop()
# GLib.threads_init()
Gst.init(None)

W = 640
H = 480


# старый пайплайн (работает)
piplineRtspEduBot = "v4l2src device=/dev/video0 ! video/x-raw, width=320, height=240, framerate=10/1, pixel-aspect-ratio=1/1 ! \
                                gdkpixbufoverlay location=battery.png offset-x=0 offset-y=0 overlay-height=40 overlay-width=40 ! v4l2h264enc ! rtph264pay name=pay0 pt=96"
pipline2 = " v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480 ! videoconvert ! \
                                          rsvgoverlay location=test.svg ! videoconvert ! xvimagesink alsasrc device=plughw:CARD=2,DEV=0 ! audioconvert ! autoaudiosink "
"""xvimagesink"""

""" videotestsrc pattern=smpte ! video/x-raw, width=640, height=480, framerate=30/1 ! autovideoconvert ! rsvgoverlay name=overlay ! autovideoconvert ! x264enc ! rtph264pay name=pay0 pt=96 """

class PotatoCamFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        GstRtspServer.RTSPMediaFactory.__init__(self)

    def do_create_element(self, url):
        pipeline_str = "v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480 ! autovideoconvert ! x264enc ! rtph264pay name=pay0 pt=96"

        pipeline = Gst.parse_launch(pipeline_str) # Создание пайплайна
        print(pipeline_str)
        return pipeline


###################
"""Возвращает ip"""
###################
def getIP():
    res = os.popen('hostname -I | cut -d\' \' -f1').readline().replace('\n','') #получаем IP, удаляем \n
    return res



# Порт: 5554. Камера: potato.
class PotatoServer():
    def __init__(self):
        self.PotatoServer = GstRtspServer.RTSPServer.new()
        self.PotatoServer.set_service('5554')

        self.potatoCam = PotatoCamFactory()
        self.potatoCam.set_shared(True)

        m = self.PotatoServer.get_mount_points()
        m.add_factory("/potato", self.potatoCam)

        self.PotatoServer.attach(None)

        port_PotatoServer = self.PotatoServer.get_bound_port()
        print('RTSP server started: rtsp://%s:%d/front' % (getIP(), port_PotatoServer))


if __name__ == '__main__':
    print(4)
    s1 = PotatoServer()

    loop.run()
    print(6)