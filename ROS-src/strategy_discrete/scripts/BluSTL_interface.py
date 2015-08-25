#!/usr/bin/env python

import sys
import rospy
# from strategy_discrete.srv import *
from strategy_discrete.msg import *
from dispatcher_simple.msg import *

class BluSTL_interface(object):

    def __init__(self):
        rospy.init_node('BluSTL_interface', anonymous=True)
        self.pub = rospy.Publisher('BluSTL_signal', BluSTL_signal, queue_size=10)
        self.pub_2 = rospy.Publisher('Matlab_input', Matlab_input, queue_size=10)
        rospy.Subscriber('location_assignment', location_assignment, self.callback_0)
        rospy.Subscriber('Matlab_output', Matlab_output, self.callback_1)
        self._current_loc = -1
        self._ready = 1
        self._ID = 0
        self._lock = 0
        rospy.spin()

    def callback_0(self, data):
        self._lock = 1
        print str(self._ID) + ": BluSTL_interface receives command from strategy."
        flag = 0
        if self._current_loc == -1:
            self._ready = 1
        elif self._current_loc==data.loc and self._ready == 1:
            self._ready = 1
        elif self._current_loc!=data.loc and self._ready == 1:
            self._ready = 0
            flag = 1
        else:
            self._ready = 0
        self._current_loc = data.loc
        rospy.sleep(1) # This is to give priority to request_processor to update full first.
        self.pub.publish(self._ready, 1)
        print str(self._ID) + ": BluSTL_interface has sent ready pair: %s"%str(self._ready)
        self._ID = self._ID + 1
        if flag == 1:
            self.pub_2.publish(self._current_loc)
        self._lock = 0

    def callback_1(self, data):
        print str(self._ID) + ": BluSTL_interface receives result from Matlab."
        if self._lock==0:
            if data.succeed == 1:
                self._ready = 1
                self.pub.publish(self._ready, 0)
                print "BluSTL_interface has sent ready: %s"%str(self._ready)
            else:
                print "BluSTL fails to reach target location. Will keep trying..."
                self.pub_2.publish(self._current_loc)
        else:
            if data.succeed == 1:
                self._ready = 1
                print "BluSTL_interface has changed ready but not sent: %s"%str(self._ready)
            else:
                print "BluSTL fails to reach target location. Will keep trying..."
                self.pub_2.publish(self._current_loc)

if __name__ == "__main__":
    try:
        BluSTL_interface()
    except rospy.ROSInterruptException:
        pass
       

