#!/usr/bin/env python

import rospy
# from TuLiPstrategy_client import *
# from dispatcher_simple.srv import *
import dispatcher_simple.msg
import strategy_discrete.msg

class request_processor(object):

    def __init__(self):
       rospy.init_node('request_processor', anonymous=True)
       self.pub = rospy.Publisher('requests', dispatcher_simple.msg.requests, queue_size=10)
       rospy.Subscriber("req_from_env", dispatcher_simple.msg.req_from_env, self.callback_0)
       rospy.Subscriber("location_assignment_0", strategy_discrete.msg.location_assignment, self.callback_1)
       rospy.Subscriber("location_assignment_1", strategy_discrete.msg.location_assignment, self.callback_2)
       rospy.Subscriber("BluSTL_signal_0", dispatcher_simple.msg.BluSTL_signal, self.callback_3)
       rospy.Subscriber("BluSTL_signal_1", dispatcher_simple.msg.BluSTL_signal, self.callback_4)
       self._req_1 = 0
       self._req_2 = 0
       self._req_3 = 0
       self._full_car_0 = 0
       self._full_car_1 = 0
       self._ready_0 = 1
       self._ready_1 = 1
       self._from_location_assignment_lock = 0
       rospy.spin()
       

    def callback_0(self, data):
        self._req_1 = data.req_1
        self._req_2 = data.req_2
        self._req_3 = data.req_3

    def callback_1(self, data):
        self._full_car_0 = data.full

    def callback_2(self, data):
        self._full_car_1 = data.full

    def callback_3(self, data):
        if data.from_location_assignment == 0:
            self._ready_0 = data.ready
            if self._ready_0 == 1: # TODO: Think about if this is good.
                print "request from processor sent"
                self.pub.publish(self._req_1, self._req_2, self._req_3,
                    self._full_car_1, self._full_car_0, self._ready_0, self._ready_1)
            # rospy.sleep(1) # TODO: Think about how to implement it.
        else:
            self._ready_0 = data.ready
            if self._from_location_assignment_lock == 1:
                if self._ready_0 == 1 or self._ready_1 == 1: # TODO: Think about if this is good.
                    print "request from processor sent"
                    self.pub.publish(self._req_1, self._req_2, self._req_3,
                        self._full_car_1, self._full_car_0, self._ready_0, self._ready_1)
                self._from_location_assignment_lock = 0
            else:
                self._from_location_assignment_lock = 1

    def callback_4(self, data):
        if data.from_location_assignment == 0:
            self._ready_1 = data.ready
            if self._ready_1 == 1: # TODO: Think about if this is good.
                print "request from processor sent"
                self.pub.publish(self._req_1, self._req_2, self._req_3,
                    self._full_car_1, self._full_car_0, self._ready_0, self._ready_1)
            # rospy.sleep(1) # TODO: Think about how to implement it.
        else:
            self._ready_1 = data.ready
            if self._from_location_assignment_lock == 1:
                if self._ready_0 == 1 or self._ready_1 == 1: # TODO: Think about if this is good.
                    print "request from processor sent"
                    self.pub.publish(self._req_1, self._req_2, self._req_3,
                        self._full_car_1, self._full_car_0, self._ready_0, self._ready_1)
                self._from_location_assignment_lock = 0
            else:
                self._from_location_assignment_lock = 1
        
        
if __name__ == "__main__":
    try:
        request_processor()
    except rospy.ROSInterruptException:
        pass