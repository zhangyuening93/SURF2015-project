#!/usr/bin/env python

import sys
import rospy
import numpy as np
from taxi_center.msg import *

class difference_cal(object):

    def __init__(self):
        rospy.init_node('difference_cal', anonymous=True)
        self.pub = rospy.Publisher('disturbance_signal_0', sensor, queue_size=10)
        self.pub_2 = rospy.Publisher('disturbance_signal_1', sensor, queue_size=10)
        rospy.Subscriber('position_0', position, self.callback_0)
        rospy.Subscriber('position_1', position, self.callback_1)
        self._position_0_x = list()
        self._position_0_y = list()
        self._position_0_ID = -1
        self._position_1_x = list()
        self._position_1_y = list()
        self._position_1_ID = -1
        self._horizon = 10
        rospy.spin()

    def callback_0(self, data):
        # print "difference_cal receives position_0 update. Processing...."
        self._position_0_x = data.x
        self._position_0_y = data.y
        self._position_0_ID = data.ID
        if not self._position_1_x:
            self._position_1_x = [-1]*len(self._position_0_x)
            self._position_1_y = [-1]*len(self._position_0_x)
        w1 = list(np.float16(np.array(self._position_0_x)) - np.float16(np.array(self._position_1_x)))
        w2 = list(np.float16(np.array(self._position_0_y)) - np.float16(np.array(self._position_1_y)))
        if self._position_0_ID < self._horizon:
            if abs(w1[self._position_0_ID])<0.3 and abs(w2[self._position_0_ID])<0.3:
                rospy.loginfo("The two car are getting close.")
        else:
            if abs(w1[self._horizon])<0.3 and abs(w2[self._horizon])<0.3:
                rospy.loginfo("The two car are getting close.")
        w3 = list()
        for i in range(len(w1)):
            if abs(w1[i])<1 and abs(w2[i])<1:
                w3.append(1)
            else:
                w3.append(0)
        # print w3
        # w1 = [0]*len(w1)
        # w2 = [0]*len(w1)
        # w4 = [0]*len(w1)
        # print list(self._position_1_x)
        # print list(self._position_1_y)
        self.pub.publish(w3, list(self._position_1_x), list(self._position_1_y), self._position_0_ID)
        # print "disturbance_signal_0 sent with w3 = %s, and ID = %s."%(str(w3), str(self._position_0_ID))
        if self._position_0_ID < self._horizon:
            print "disturbance_signal_0 ID = %s. pos is %s, %s."%(str(self._position_0_ID),str(self._position_0_x[self._position_0_ID]), str(self._position_0_y[self._position_0_ID]))
        else:
            print "disturbance_signal_0 ID = %s. pos is %s, %s."%(str(self._position_0_ID),str(self._position_0_x[self._horizon]), str(self._position_0_y[self._horizon]))

    def callback_1(self, data):
        # print "difference_cal receives position_1 update. Processing...."
        self._position_1_x = data.x
        self._position_1_y = data.y
        self._position_1_ID = data.ID
        if not self._position_0_x:
            self._position_0_x = [-1]*len(self._position_1_x)
            self._position_0_y = [-1]*len(self._position_1_x)
        w1 = list(np.float16(np.array(self._position_0_x)) - np.float16(np.array(self._position_1_x)))
        w2 = list(np.float16(np.array(self._position_0_y)) - np.float16(np.array(self._position_1_y)))
        if self._position_1_ID < self._horizon:
            if abs(w1[self._position_1_ID])<0.3 and abs(w2[self._position_1_ID])<0.3:
                rospy.loginfo("The two car are getting close.")
        else:
            if abs(w1[self._horizon])<0.3 and abs(w2[self._horizon])<0.3:
                rospy.loginfo("The two car are getting close.")
        w3 = list()
        for i in range(len(w1)):
            if abs(w1[i])<1 and abs(w2[i])<1:
                w3.append(1)
            else:
                w3.append(0)
        # print w3
        # w1 = [0]*len(w1)
        # w2 = [0]*len(w1)
        # w4 = [0]*len(w1)
        # print list(self._position_0_x)
        # print list(self._position_0_y)

        self.pub_2.publish(w3, list(self._position_0_x), list(self._position_0_y), self._position_1_ID)
        # print "disturbance_signal_1 sent with w3 = %s, and ID = %s."%(str(w3), str(self._position_1_ID))
        if self._position_1_ID < self._horizon:
            print "disturbance_signal_1 ID = %s. pos is %s, %s."%(str(self._position_1_ID),str(self._position_1_x[self._position_1_ID]), str(self._position_1_y[self._position_1_ID]))
        else:
            print "disturbance_signal_1 ID = %s. pos is %s, %s."%(str(self._position_1_ID),str(self._position_1_x[self._horizon]), str(self._position_1_y[self._horizon]))

if __name__ == "__main__":
    try:
        difference_cal()
    except rospy.ROSInterruptException:
        pass
       

