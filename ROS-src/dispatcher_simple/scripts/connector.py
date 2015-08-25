#!/usr/bin/env python

import sys
import rospy
from dispatcher_simple.msg import *

class connector(object):

	def __init__(self):
		rospy.init_node('connector', anonymous = True)
		rospy.Subscriber('topic_from', car_assignment, self.callback)
		self.pub = rospy.Publisher('topic_to', car_assignment, queue_size=10)
		rospy.spin()

	def callback(self, data):
		self.pub.publish(data)

if __name__ == "__main__":
	connector()