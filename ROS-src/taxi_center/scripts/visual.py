#!/usr/bin/env python

from Tkinter import *
import rospy
import numpy as np
from taxi_center.msg import *
from std_msgs.msg import Bool,Int8

class Application(Frame):
    """This is visualization for taxi center."""

    def __init__(self, master, publisher):
        self.pub = publisher
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

        self.req_1_status = 0
        self.req_2_status = 0
        self.req_3_status = 0  
        
    def create_widgets(self):
        self.canvas = Canvas(self, height=500, width=500, bg="white")
        self.configure_canvas(380, 230, 10, 50)
        self.canvas.grid(row=1, column=1, columnspan=3)

        mycolor = '#40E0D0'

        self.button1 = Button(self, text="request: 0", command=self.callback_pub_0, bg=mycolor)
        self.button1.grid(row=2, column=1)
        self.button2 = Button(self, text="request: 1", command=self.callback_pub_1, bg=mycolor)
        self.button2.grid(row=2, column=2)
        self.button3 = Button(self, text="request: 2", command=self.callback_pub_2, bg=mycolor)
        self.button3.grid(row=2, column=3)

        self.info = Text(self, height=33, width=50, wrap=WORD)
        self.info.grid(row=1, column=4)
       

    def configure_canvas(self, pos_0_x, pos_0_y, pos_1_x, pos_1_y):
        self.canvas.create_rectangle(50, 300, 100, 350, fill="yellow")
        self.canvas.create_rectangle(50, 50, 100, 100, fill="yellow")
        self.canvas.create_rectangle(150, 100, 200, 150, fill="yellow")
        self.canvas.create_rectangle(450, 300, 500, 350, fill="yellow")
        # This is added for this particular example that has bridge.
        self.canvas.create_rectangle(350, 200, 400, 250, fill="yellow")

        self.canvas.create_rectangle(210, 210, 240, 290, fill="red")

        self.canvas.create_text(50+25, 300+25, text="loc0")
        self.canvas.create_text(50+25, 50+25, text="loc1")
        self.canvas.create_text(150+25, 100+25, text="loc2")
        self.canvas.create_text(450+25, 300+25, text="des")
        # This is added for this particular example that has bridge.
        self.canvas.create_text(350+25, 200+25, text="bridge")

        self.car_0_shape = self.canvas.create_rectangle(pos_0_x-10, pos_0_y-10, pos_0_x+10, pos_0_y+10, fill="blue")
        self.car_1_shape = self.canvas.create_rectangle(pos_1_x-10, pos_1_y-10, pos_1_x+10, pos_1_y+10, fill="blue")

        self.car_0_text = self.canvas.create_text(pos_0_x, pos_0_y, text="1")
        self.car_1_text = self.canvas.create_text(pos_1_x, pos_1_y, text="2")


    def update_position_0(self, pos_x, pos_y):
        self.canvas.delete(self.car_0_shape)
        self.car_0_shape = self.canvas.create_rectangle(pos_x-10, pos_y-10, pos_x+10, pos_y+10, fill="blue")
        self.canvas.delete(self.car_0_text)
        self.car_0_text = self.canvas.create_text(pos_x, pos_y, text="1")
        
    def update_position_1(self, pos_x, pos_y):
        self.canvas.delete(self.car_1_shape)
        self.car_1_shape = self.canvas.create_rectangle(pos_x-10, pos_y-10, pos_x+10, pos_y+10, fill="blue")
        self.canvas.delete(self.car_1_text)
        self.car_1_text = self.canvas.create_text(pos_x, pos_y, text="2")

    def display_message(self, message):
        self.info.insert(0.0, message)

    def update_button(self, req_1, req_2, req_3):
        # print "will update button now."
        mycolor = '#40E0D0'
        if req_1:
            self.button1.configure(bg=mycolor)
            self.req_1_status = 0
        if req_2:
            self.button2.configure(bg=mycolor)
            self.req_2_status = 0
        if req_3:
            self.button3.configure(bg=mycolor)
            self.req_3_status = 0
        # print "button should be updated now."
        self.pub.publish(self.req_1_status, self.req_2_status, self.req_3_status)

    def callback_pub_0(self):
        self.req_1_status = 1
        self.button1.configure(bg="red")
        self.pub.publish(self.req_1_status, self.req_2_status, self.req_3_status)

    def callback_pub_1(self):
        self.req_2_status = 1
        self.button2.configure(bg="red")
        self.pub.publish(self.req_1_status, self.req_2_status, self.req_3_status)

    def callback_pub_2(self):
        self.req_3_status = 1
        self.button3.configure(bg="red")
        self.pub.publish(self.req_1_status, self.req_2_status, self.req_3_status)
        

class GUI_taxi_center(object):
    """This is the interface for GUI and ros."""

    def __init__(self, master):
        #ros publisher and subscriber.
        rospy.init_node('visualization', anonymous=True)
        self.pub = rospy.Publisher('req_from_env', req_from_env, queue_size=10)
        rospy.Subscriber('position_0', position, self.callback_sub_0)
        rospy.Subscriber('position_1', position, self.callback_sub_1)
        rospy.Subscriber('taxi_assignment_0', taxi_assignment, self.callback_sub_2)
        rospy.Subscriber('taxi_assignment_1', taxi_assignment, self.callback_sub_2)
        rospy.Subscriber('Matlab_input_0', Int8, self.callback_sub_3)
        rospy.Subscriber('Matlab_input_1', Int8, self.callback_sub_4)
        rospy.Subscriber('Matlab_output_0', Bool, self.callback_sub_5)
        rospy.Subscriber('Matlab_output_1', Bool, self.callback_sub_6)
        

        #GUI
        self.app = Application(master, self.pub)
        self.position_0_x = 380
        self.position_0_y = 230
        self.position_1_x = 10
        self.position_1_y = 50
        self._horizon = 10

        self._loc_0 = -1
        self._loc_1 = -1
        
    def callback_sub_0(self, data):
        if data.ID < self._horizon:
            self.position_0_x = int(data.x[data.ID]*100)
            self.position_0_y = int(data.y[data.ID]*100)
        else:
            self.position_0_x = int(data.x[self._horizon]*100)
            self.position_0_y = int(data.y[self._horizon]*100)
        self.app.update_position_0(self.position_0_x, self.position_0_y)
        w1 = self.position_0_x-self.position_1_x
        w2 = self.position_0_y-self.position_1_y
        if abs(w1)<20 and abs(w2)<20:
            message = "Car 1: Two car crashes with w1=%s, w2=%s. \n"%(str(w1), str(w2))
            self.app.display_message(message)


    def callback_sub_1(self, data):
        if data.ID < self._horizon:
            self.position_1_x = int(data.x[data.ID]*100)
            self.position_1_y = int(data.y[data.ID]*100)
        else:
            self.position_1_x = int(data.x[self._horizon]*100)
            self.position_1_y = int(data.y[self._horizon]*100)
        self.app.update_position_1(self.position_1_x, self.position_1_y)
        w1 = self.position_0_x-self.position_1_x
        w2 = self.position_0_y-self.position_1_y
        if abs(w1)<20 and abs(w2)<20:
            message = "Car 2: Two car crashes with w1=%s, w2=%s. \n"%(str(w1), str(w2))
            self.app.display_message(message)


    def callback_sub_2(self, data):
        # print "callback is called."
        req_1_finish = 0
        req_2_finish = 0
        req_3_finish = 0
        if data.req_0:
            req_1_finish = 1
        if data.req_1:
            req_2_finish = 1
        if data.req_2:
            req_3_finish = 1
        self.app.update_button(req_1_finish, req_2_finish, req_3_finish)

    def callback_sub_3(self, data):
        self._loc_0 = data.data

    def callback_sub_4(self, data):
        self._loc_1 = data.data

    def callback_sub_5(self, data):
        if data.data:
            if self._loc_0 >= 0 and self._loc_0 <= 2:
                message = "Car 1: Reaches loc " + str(self._loc_0) + ". \n"
                self.app.display_message(message)
            # This is added for this particular example that has bridge.
            elif self._loc_0 == 3:
                message = "Car 1: Reaches bridge. \n"
                self.app.display_message(message)
            elif self._loc_0 == -1:
                message = "Car 1: Reaches des. \n"
                self.app.display_message(message)

    def callback_sub_6(self, data):
        if data.data:
            if self._loc_1 >= 0 and self._loc_1 <= 2:
                message = "Car 2: Reaches loc " + str(self._loc_1) + ". \n"
                self.app.display_message(message)
            # This is added for this particular example that has bridge.
            elif self._loc_1 == 3:
                message = "Car 2: Reaches bridge. \n"
                self.app.display_message(message)
            elif self._loc_1 == -1:
                message = "Car 2: Reaches des. \n"
                self.app.display_message(message)

            
        

if __name__=="__main__":
    root = Tk()
    root.title("Taxi Center")
    my_GUI = GUI_taxi_center(root)
    root.mainloop()