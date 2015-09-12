#!/usr/bin/env python

import sys
from taxi_center.srv import *
import rospy
from strategy_class import strategy

class strategy_server(object):

    def __init__(self):
        rospy.init_node('strategy_server')
        self._system = strategy()
        s = rospy.Service('strategy_service', strategy_srv, self.callback)
        print "Strategy ready."
        rospy.spin()


    def callback(self, data):
        try:
            output = self._system.move(data.req_0, data.req_1, data.req_2, data.ready)        
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
    strategy_server()
