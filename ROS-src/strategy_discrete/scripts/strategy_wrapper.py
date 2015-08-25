#!/usr/bin/env python

import sys
import rospy
# import TuLiPstrategy_client
# import TuLiPstrategy_client_2
from strategy_discrete.srv import *
from strategy_discrete.msg import *

class TuLiP_client_wrapper(object):

    def __init__(self, arg):
        rospy.init_node('strategy_0', anonymous=True)
        if arg==0:
            self.pub = rospy.Publisher('location_assignment_0', location_assignment, queue_size=10)
        elif arg==1:
            self.pub = rospy.Publisher('location_assignment_1', location_assignment, queue_size=10)
        else:
            print "Arg for strategy_discrete can only be 0 or 1."
        rospy.Subscriber("car_assignment", car_assignment, self.callback, arg)
        self._ID = 0
        rospy.spin()

    def callback(self, data, arg):
        if arg==0:
            print str(self._ID) + ": strategy_level 0 receives command from dispatcher."
            print str(self._ID) + ": Car_0 is ready: %s, is assigned req: %s."%(str(data.ready_0), str(data.car_0))
            response = self.TuLiPstrategy_client('TuLiPstrategy', data.ready_0, data.car_0)
            print str(self._ID) + ": The car has full: %s and has assigned loc: %s"%(str(response.full), str(response.loc))
            # print self._ID
            self._ID = self._ID + 1
        elif arg==1:
            print str(self._ID) + ": strategy_level 1 receives command from dispatcher."
            print str(self._ID) + ": Car_1 is ready: %s, is assigned req: %s."%(str(data.ready_1), str(data.car_1))
            response = self.TuLiPstrategy_client('TuLiPstrategy_2', data.ready_1, data.car_1)
            print str(self._ID) + ": The car has full: %s and has assigned loc: %s"%(str(response.full), str(response.loc))
            # print self._ID
            self._ID = self._ID + 1
        else:
            print "Arg for strategy_discrete can only be 0 or 1."
        # print response
        self.pub.publish(response.loc, response.full)

    # TODO: Modify such that Service Proxy is not always initialized every time it is called.
    def TuLiPstrategy_client(self, strategy_name, *args):
        rospy.wait_for_service(strategy_name)
        try:
            controller = rospy.ServiceProxy(strategy_name, TuLiP_service)
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
        # print sys.argv
        # print len(sys.argv)
        # print "1"
        # if len(sys.argv)==3:
            # print "2"
            # TuLiP_client_wrapper()
        # else:
            # print "3"
            # arg = map(int, sys.argv[1:])
            # print arg
            # print arg[0]
        TuLiP_client_wrapper(int(sys.argv[1]))
    except rospy.ROSInterruptException:
        pass
