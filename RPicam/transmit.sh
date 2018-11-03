HOST=192.168.1.113
RTPBIN_PARAMS="drop-on-latency=true"
DEVICE='/dev/video0'
CAPS='image/jpeg,width=800,height=600,framerate=10/1'
#CAPS='image/jpeg,width=640,height=480,framerate=30/1'

gst-launch-1.0 -v rtpbin name=rtpbin $RTPBIN_PARAMS                                  \
        v4l2src device=$DEVICE ! $CAPS ! jpegparse ! rtpjpegpay ! rtpbin.send_rtp_sink_0 \
                  rtpbin.send_rtp_src_0 ! udpsink port=5000 host=$HOST                     \
                  rtpbin.send_rtcp_src_0 ! udpsink port=5001 sync=false async=false    \
                  udpsrc port=5005 ! rtpbin.recv_rtcp_sink_0
