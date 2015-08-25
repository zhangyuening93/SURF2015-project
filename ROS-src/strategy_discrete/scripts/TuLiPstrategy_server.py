#!/usr/bin/env python

import sys
from strategy_discrete.srv import *
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
            output = self._system.move(data.ready, data.req)        
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
