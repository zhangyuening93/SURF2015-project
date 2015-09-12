#!/usr/bin/env python

import rospy
from taxi_center.msg import *
from taxi_center.srv import *

class request_processor(object):

    def __init__(self):
        rospy.init_node('request_processor', anonymous=True)
        self.pub = rospy.Publisher('requests', requests, queue_size=10)
        rospy.Subscriber("req_from_env", req_from_env, self.callback)
        rate = rospy.Rate(1)
        self._req_0 = 0
        self._req_1 = 0
        self._req_2 = 0
        while not rospy.is_shutdown():
            full_0 = self.TuLiPstrategy_client('status_full_0', 1)
            full_0 = full_0.full
            full_1 = self.TuLiPstrategy_client('status_full_1', 1)
            full_1 = full_1.full
            self.pub.publish(self._req_0, self._req_1, self._req_2, full_0, full_1)
            rate.sleep()

    def callback(self, data):
        self._req_0 = data.req_0
        self._req_1 = data.req_1
        self._req_2 = data.req_2

    def TuLiPstrategy_client(self, namespace, *args):
        rospy.wait_for_service(namespace)
        try:
            controller = rospy.ServiceProxy(namespace, status_full)
            try:
                request = status_fullRequest(*args)
            except TypeError, e:
                print e
                sys.exit(1)
            response = controller(request)
            return response
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
        
        
if __name__ == "__main__":
    try:
        request_processor()
    except rospy.ROSInterruptException:
        pass