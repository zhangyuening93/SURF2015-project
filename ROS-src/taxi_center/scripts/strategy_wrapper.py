#!/usr/bin/env python

import sys
import rospy
from taxi_center.srv import *
from taxi_center.msg import *
from std_msgs.msg import Bool

class strategy_wrapper(object):

    def __init__(self):
        rospy.init_node('strategy', anonymous=True)
        s = rospy.Service('status_full', status_full, self.callback_service)
        self.pub = rospy.Publisher('location_assignment', location_assignment, queue_size=10)
        rospy.Subscriber("taxi_assignment", taxi_assignment, self.callback)
        rospy.Subscriber("BluSTL_signal", Bool, self.callback_2)
        self.full = 0
        self._ID = 0
        rospy.spin()

    def callback(self, data):
        print str(self._ID) + ": strategy_level receives command from dispatcher."
        namespace = 'Taxi'
        print str(self._ID) + ': '+ namespace +' is assigned req: %s %s %s .'%(str(data.req_0), str(data.req_1), str(data.req_2))
        # We use default value of ready = 0, 
        # because it will not have any consequences 
        # other than having the loc be the same.

        response = self.TuLiPstrategy_client(data.req_0, data.req_1, data.req_2, 0)
        # This is added for this particular example that has bridge.
        # print str(self._ID) + ': '+ namespace +' has full: %s and has assigned loc: %s %s %s %s'%(str(response.full), str(response.loc_0), str(response.loc_1), str(response.loc_2), str(response.des))
        print str(self._ID) + ': '+ namespace +' has full: %s and has assigned loc: %s %s %s %s %s'%(str(response.full), str(response.loc_0), str(response.loc_1), str(response.loc_2), str(response.bridge), str(response.des))
        
        self.full = response.full
        self._ID = self._ID + 1
        # print response
        # TODO: May not actually need response, loc will not change, 
        # and we just want a state transition.
        # self.pub.publish(response.loc_0, response.loc_1, response.loc_2, response.des)

    def callback_2(self, data):
        print str(self._ID) + ": strategy_level receives signal from BluSTL_signal."
        namespace = 'Taxi'
        # We use default value of all req = 0
        response = self.TuLiPstrategy_client(0, 0, 0, 1)
        # This is added for this particular example that has bridge.
        # print str(self._ID) + ': '+ namespace +' has full: %s and has assigned loc: %s %s %s %s'%(str(response.full), str(response.loc_0), str(response.loc_1), str(response.loc_2), str(response.des))
        print str(self._ID) + ': '+ namespace +' has full: %s and has assigned loc: %s %s %s %s %s'%(str(response.full), str(response.loc_0), str(response.loc_1), str(response.loc_2), str(response.bridge), str(response.des))
        self.full = response.full
        self._ID = self._ID + 1
        # print response
        # This is added for this particular example that has bridge.
        # self.pub.publish(response.loc_0, response.loc_1, response.loc_2, response.des)
        self.pub.publish(response.loc_0, response.loc_1, response.loc_2, response.bridge, response.des)

    def callback_service(self, data):
        return self.full

    # TODO: Modify such that Service Proxy is not always initialized every time it is called.
    def TuLiPstrategy_client(self, *args):
        rospy.wait_for_service('strategy_service')
        try:
            controller = rospy.ServiceProxy('strategy_service', strategy_srv)
            try:
                request = strategy_srvRequest(*args)
            except TypeError, e:
                print e
                sys.exit(1)
            response = controller(request)
            return response
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e


if __name__ == "__main__":
    try:
        strategy_wrapper()
    except rospy.ROSInterruptException:
        pass
