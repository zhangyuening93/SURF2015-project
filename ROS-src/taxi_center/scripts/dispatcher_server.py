#!/usr/bin/env python

import sys
from taxi_center.srv import *
import rospy
from dispatcher_class import dispatcher

class dispatcher_server(object):

    def __init__(self):
        rospy.init_node('dispatcher_server')
        self._system = dispatcher()
        s = rospy.Service('dispatcher_service', dispatcher_srv, self.callback)
        print "Dispatcher ready."
        rospy.spin()


    def callback(self, data):
        try:
            output = self._system.move(data.req_0, data.req_1, data.req_2, data.full_0, data.full_1)        
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
    dispatcher_server()
