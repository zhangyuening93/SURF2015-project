#!/usr/bin/env python

import sys
import rospy
import numpy as np
# from strategy_discrete.srv import *
from strategy_discrete.msg import *
# from dispatcher_simple.msg import *

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
        rospy.spin()

    def callback_0(self, data):
        # print "difference_cal receives position_0 update. Processing...."
        # print data.x
        # print data.y
        self._position_0_x = data.x
        self._position_0_y = data.y
        # print self._position_0_x
        # print self._position_0_y
        self._position_0_ID = data.ID
        # xmin = self._position_0_x + 0.1
        # xmax = self._position_0_x + 0.6
        # ymin = self._position_0_y - 0.3
        # ymax = self._position_0_y + 0.3
        # if self._position_1_x > xmin and self._position_1_x < xmax and self._position_1_y > ymin and self._position_1_y < ymax:
        #     w1 = 1
        # else:
        #     w1 = 0
        # xmin = self._position_0_x - 0.3
        # xmax = self._position_0_x + 0.3
        # ymin = self._position_0_y + 0.1
        # ymax = self._position_0_y + 0.6
        # if self._position_1_x > xmin and self._position_1_x < xmax and self._position_1_y > ymin and self._position_1_y < ymax:
        #     w2 = 1
        # else:
        #     w2 = 0
        # xmin = self._position_0_x - 0.6
        # xmax = self._position_0_x - 0.1
        # ymin = self._position_0_y - 0.3
        # ymax = self._position_0_y + 0.3
        # if self._position_1_x > xmin and self._position_1_x < xmax and self._position_1_y > ymin and self._position_1_y < ymax:
        #     w3 = 1
        # else:
        #     w3 = 0
        # xmin = self._position_0_x - 0.3
        # xmax = self._position_0_x + 0.3
        # ymin = self._position_0_y - 0.6
        # ymax = self._position_0_y - 0.1
        # if self._position_1_x > xmin and self._position_1_x < xmax and self._position_1_y > ymin and self._position_1_y < ymax:
        #     w4 = 1
        # else:
        #     w4 = 0
        if not self._position_1_x:
            self._position_1_x = [-1]*len(self._position_0_x)
            self._position_1_y = [-1]*len(self._position_0_x)
        w1 = list(np.float16(np.array(self._position_0_x)) - np.float16(np.array(self._position_1_x)))
        # print w1
        w2 = list(np.float16(np.array(self._position_0_y)) - np.float16(np.array(self._position_1_y)))
        # print w2
        if abs(w1[0])<0.3 and abs(w2[0])<0.3:
            rospy.loginfo("The two car are too close with distance of x and y: %s, %s", str(w1[0]), str(w1[2]))
        w3 = list()
        for i in range(len(w1)):
            if abs(w1[i])<1 and abs(w2[i])<1:
                w3.append(1)
            else:
                w3.append(0)
        # print w3
        w1 = [0]*len(w1)
        w2 = [0]*len(w1)
        w4 = [0]*len(w1)
        # print list(self._position_1_x)
        # print list(self._position_1_y)
        
        self.pub.publish(w1, w2, w3, w4, list(self._position_1_x), list(self._position_1_y), self._position_0_ID)
        # print "disturbance_signal_0 sent with w3 = %s, and ID = %s."%(str(w3), str(self._position_0_ID))
        print "disturbance_signal_0 ID = %s."%(str(self._position_0_ID))

    def callback_1(self, data):
        # print "difference_cal receives position_1 update. Processing...."
        self._position_1_x = data.x
        self._position_1_y = data.y
        self._position_1_ID = data.ID
        # xmin = self._position_1_x + 0.1
        # xmax = self._position_1_x + 0.6
        # ymin = self._position_1_y - 0.3
        # ymax = self._position_1_y + 0.3
        # if self._position_0_x > xmin and self._position_0_x < xmax and self._position_0_y > ymin and self._position_0_y < ymax:
        #     w1 = 1
        # else:
        #     w1 = 0
        # xmin = self._position_1_x - 0.3
        # xmax = self._position_1_x + 0.3
        # ymin = self._position_1_y + 0.1
        # ymax = self._position_1_y + 0.6
        # if self._position_0_x > xmin and self._position_0_x < xmax and self._position_0_y > ymin and self._position_0_y < ymax:
        #     w2 = 1
        # else:
        #     w2 = 0
        # xmin = self._position_1_x - 0.6
        # xmax = self._position_1_x - 0.1
        # ymin = self._position_1_y - 0.3
        # ymax = self._position_1_y + 0.3
        # if self._position_0_x > xmin and self._position_0_x < xmax and self._position_0_y > ymin and self._position_0_y < ymax:
        #     w3 = 1
        # else:
        #     w3 = 0
        # xmin = self._position_1_x - 0.3
        # xmax = self._position_1_x + 0.3
        # ymin = self._position_1_y - 0.6
        # ymax = self._position_1_y - 0.1
        # if self._position_0_x > xmin and self._position_0_x < xmax and self._position_0_y > ymin and self._position_0_y < ymax:
        #     w4 = 1
        # else:
        #     w4 = 0
        if not self._position_0_x:
            self._position_0_x = [-1]*len(self._position_1_x)
            self._position_0_y = [-1]*len(self._position_1_x)
        w1 = list(np.float16(np.array(self._position_0_x)) - np.float16(np.array(self._position_1_x)))
        w2 = list(np.float16(np.array(self._position_0_y)) - np.float16(np.array(self._position_1_y)))
        if abs(w1[0])<0.3 and abs(w2[0])<0.3:
            rospy.loginfo("The two car are too close with distance of x and y: %s, %s", str(w1[0]), str(w1[2]))
        w3 = list()
        for i in range(len(w1)):
            if abs(w1[i])<1 and abs(w2[i])<1:
                w3.append(1)
            else:
                w3.append(0)
        # print w3
        w1 = [0]*len(w1)
        w2 = [0]*len(w1)
        w4 = [0]*len(w1)
        # print list(self._position_0_x)
        # print list(self._position_0_y)

        self.pub_2.publish(w1, w2, w3, w4, list(self._position_0_x), list(self._position_0_y), self._position_1_ID)
        # print "disturbance_signal_1 sent with w3 = %s, and ID = %s."%(str(w3), str(self._position_1_ID))
        print "disturbance_signal_1 ID = %s."%(str(self._position_1_ID))

if __name__ == "__main__":
    try:
        difference_cal()
    except rospy.ROSInterruptException:
        pass
       

