#!/usr/bin/env python

import rospy

def TuLiP_client_wrapper():
    while True:
        arguments = map(int, raw_input("Please enter requests.\n").split(','))
        print "Requesting %s"%str(arguments) 
        response = TuLiPstrategy_client(*arguments)
        print(response)

def TuLiPstrategy_client(*args):
    rospy.wait_for_service('TuLiPstrategy')
    try:
        controller = rospy.ServiceProxy('TuLiPstrategy', TuLiP_service)
        try:
            request = TuLiP_serviceRequest(*args)
            print "TuLiP_serviceRequest:"
            print str(request) + '\n'
        except TypeError, e:
            print e
            sys.exit(1)
        response = controller(request)
        return response
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
    TuLiP_client_wrapper()
