#!/usr/bin/env python

import rospy
from taxi_center.srv import *
from taxi_center.msg import *

class dispatcher_wrapper(object):

    def __init__(self):
        rospy.init_node('dispatcher', anonymous=True)
        self.pub = rospy.Publisher('taxi_assignment_0', taxi_assignment, queue_size=10)
        self.pub_2 = rospy.Publisher('taxi_assignment_1', taxi_assignment, queue_size=10)
        rospy.Subscriber("requests", requests, self.callback)
        self._ID = 0
        rospy.spin()

    def callback(self, data):
        arguments = list()
        arguments.append(data.req_0)
        arguments.append(data.req_1)
        arguments.append(data.req_2)
        arguments.append(data.full_0)
        arguments.append(data.full_1)
        print str(self._ID) + ": dispatcher receives request: %s"%str(arguments)
        response = self.TuLiPstrategy_client(*arguments)
        # print response
        print str(self._ID) + ": response is taxi_0: %s %s %s, taxi_1: %s %s %s."%(str(response.taxi_0_0), str(response.taxi_0_1), str(response.taxi_0_2), str(response.taxi_1_0), str(response.taxi_1_1), str(response.taxi_1_2))
        self._ID = self._ID + 1
        self.pub.publish(response.taxi_0_0, response.taxi_0_1, response.taxi_0_2)
        self.pub_2.publish(response.taxi_1_0, response.taxi_1_1, response.taxi_1_2)


    def TuLiPstrategy_client(self, *args):
        rospy.wait_for_service('dispatcher_service')
        try:
            controller = rospy.ServiceProxy('dispatcher_service', dispatcher_srv)
            try:
                request = dispatcher_srvRequest(*args)
            except TypeError, e:
                print e
                sys.exit(1)
            response = controller(request)
            return response
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e


if __name__ == "__main__":
    try:
        dispatcher_wrapper()
    except rospy.ROSInterruptException:
        pass