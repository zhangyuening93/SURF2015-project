#!/usr/bin/env python

import rospy
from taxi_center.msg import *
from std_msgs.msg import Bool, Int8

class BluSTL_interface(object):

    def __init__(self):
        rospy.init_node('BluSTL_interface', anonymous=True)
        self.pub = rospy.Publisher('BluSTL_signal', Bool, queue_size=10)
        self.pub_2 = rospy.Publisher('Matlab_input', Int8, queue_size=10)
        rospy.Subscriber('location_assignment', location_assignment, self.callback_0)
        rospy.Subscriber('Matlab_output', Bool, self.callback_1)
        self._current_loc = -1
        self._ready = 0
        self._ID = 0
        rospy.spin()

    # TODO: add lock
    def callback_0(self, data):
        print str(self._ID) + ": BluSTL_interface receives command from strategy."
        if data.loc_0:
            loc = 0
        elif data.loc_1:
            loc = 1
        elif data.loc_2:
            loc = 2
        elif data.des:
            loc = -1
        # This is added for this particular example that has bridge.
        elif data.bridge:
            loc = 3
        if self._current_loc==loc and self._ready == 1:
            self._ready = 1
            rospy.sleep(1)
            self.pub.publish(self._ready)
            print str(self._ID) + ": BluSTL_interface has sent ready."
        elif self._current_loc!=loc and self._ready == 1:
            self._ready = 0
            self._current_loc = loc
            self.pub_2.publish(self._current_loc)
            print str(self._ID) + ": BluSTL_interface has sent command to Matlab: %s."%(str(self._current_loc))
        self._ID = self._ID + 1


    def callback_1(self, data):
        print str(self._ID) + ": BluSTL_interface receives result from Matlab."
        if data.data == 1:
            self._ready = 1
            self.pub.publish(self._ready)
            print "BluSTL_interface has sent ready."
        else:
            print "BluSTL fails to reach target location. Will keep trying..."
            self.pub_2.publish(self._current_loc)


if __name__ == "__main__":
    try:
        BluSTL_interface()
    except rospy.ROSInterruptException:
        pass
       

