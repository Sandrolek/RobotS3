#!/usr/bin/env bash
raspivid -t 999999 -h 720 -w 1080 -fps 10 -hf -b 2000000 -o - | gst-launch-1.0 -v fdsrc ! \
h264parse !  rtph264pay config-interval=1 pt=96 ! gdppay ! \
tcpserversink host=192.168.1.105 port=5000
