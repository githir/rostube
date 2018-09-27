#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2, pafy
import rospy
from cv_bridge import CvBridge, CvBridgeError

from sensor_msgs.msg import Image

rospy.init_node('video_publisher', anonymous=True)
pub = rospy.Publisher('video_raw', Image, queue_size=10)
bridge = CvBridge()

argvs = sys.argv
if len(argvs) == 2:
  url = argvs[1]
else:
  url = "https://www.youtube.com/watch?v=aKX8uaoy9c8"

try:
  videoPafy = pafy.new(url)
  best = videoPafy.getbest(preftype="webm")
  video=cv2.VideoCapture(best.url)
except Exception as e:
  print e
  print "invalud URL"
  exit(-1)


#print "-----------------------------------------------"
#for s in videoPafy.streams:
#  print s

print "-----------------------------------------------"
print "title :", videoPafy.title
print "viewcount :",videoPafy.viewcount, "autor :",videoPafy.author, "length :",videoPafy.length
print "duration :",videoPafy.duration, "likes :",videoPafy.likes, "dislikes :", videoPafy.dislikes
print "-----------------------------------------------"
print "description :\n",videoPafy.description
print "-----------------------------------------------"
fps = 24
print "fps =", fps
print "-----------------------------------------------"

#cap = cv2.VideoCapture(0)

r = rospy.Rate(fps)
seq = 0

while not rospy.is_shutdown():
    # Capture frame-by-frame
    ret, frame = video.read()
    if not ret:
        print "finished."
        break

    # Our operations on the frame come here
  #  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the resulting frame
#    cv2.imshow('frame',frame)
 #   cv2.imshow('frame',gray)

    seq += 1
    msg = Image()
    msg.header.seq = seq
    msg.header.stamp= rospy.Time.now()
    msg.header.frame_id = "camera"
    height, width, channels = frame.shape[:3] 
    msg.height = height 
    msg.width = width 
    msg.encoding = "rgb8"
    msg.is_bigendian = 0
    msg.step = width*1*3
    msg.data = bridge.cv2_to_imgmsg(rgb).data

    pub.publish(msg)

    r.sleep()

# When everything done, release the capture
video.release()
cv2.destroyAllWindows()



## References:
# 1) Is it possible to stream video from https:// (e.g. YouTube) into python with OpenCV?
# https://stackoverflow.com/questions/37555195/is-it-possible-to-stream-video-from-https-e-g-youtube-into-python-with-ope
#
# 2) Getting Started with Videos
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html

# autoware@autoware-pc:~/tool/youtube$ rosmsg show sensor_msgs/Image 
# std_msgs/Header header
#   uint32 seq
#   time stamp
#   string frame_id
# uint32 height
# uint32 width
# string encoding
# uint8 is_bigendian
# uint32 step
# uint8[] data

