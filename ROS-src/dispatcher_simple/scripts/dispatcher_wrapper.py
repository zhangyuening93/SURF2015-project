#!/usr/bin/env python

import rospy
from dispatcher_simple.srv import *
from dispatcher_simple.msg import *

class TuLiP_client_wrapper(object):

    def __init__(self):
        rospy.init_node('dispatcher', anonymous=True)
        self.pub = rospy.Publisher('car_assignment', car_assignment, queue_size=10)
        rospy.Subscriber("requests", requests, self.callback)
        self._ID = 0
        rospy.spin()

    def callback(self, data):
        arguments = list()
        arguments.append(data.req_1)
        arguments.append(data.req_2)
        arguments.append(data.req_3)
        arguments.append(data.full_car_1)
        arguments.append(data.full_car_0)
        print str(self._ID) + ": dispatcher receives request: %s"%str(arguments)
        response = self.TuLiPstrategy_client(*arguments)
        # print response
        print str(self._ID) + ": response is car_0: %s, car_1:%s, ready_0:%s, ready_1:%s."%(str(response.car_0), str(response.car_1), str(data.ready_0), str(data.ready_1))
        # print self._ID
        self._ID = self._ID + 1
        self.pub.publish(response.car_0, response.car_1, data.ready_0, data.ready_1)

    def TuLiPstrategy_client(self, *args):
        rospy.wait_for_service('TuLiPstrategy')
        try:
            controller = rospy.ServiceProxy('TuLiPstrategy', TuLiP_service)
            try:
                request = TuLiP_serviceRequest(*args)
                # print "TuLiP_serviceRequest:"
                # print str(request) + '\n'
            except TypeError, e:
                print e
                sys.exit(1)
            response = controller(request)
            return response
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e


if __name__ == "__main__":
    try:
        TuLiP_client_wrapper()
    except rospy.ROSInterruptException:
        pass