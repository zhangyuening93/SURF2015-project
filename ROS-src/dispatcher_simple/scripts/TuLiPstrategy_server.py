#!/usr/bin/env python

import sys
from dispatcher_simple.srv import *
import rospy
from TuLiPstrategy import strategy

class TuLiPstrategy_server(object):

    def __init__(self):
        rospy.init_node('TuLiPstrategy_server')
        self._system = strategy()
        s = rospy.Service('TuLiPstrategy', TuLiP_service, self.callback)
        print "TuLiP strategy ready."
        rospy.spin()


    def callback(self, data):
        try:
            output = self._system.move(data.req_1, data.req_2, data.req_3, data.full_car_1, data.full_car_0)        
        except ValueError, e:
            print e
            sys.exit(1)
        except Exception, e:
            print e
            sys.exit(1)
        except:
            print "Unexpected error."
            sys.exit(1)
        return output



if __name__ == "__main__":
    TuLiPstrategy_server()
