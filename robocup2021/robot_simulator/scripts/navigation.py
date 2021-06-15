#!/usr/bin/env python

"""
    RoboCup@Home Education | oc@robocupathomeedu.org
    navi.py - enable turtlebot to navigate to predefined waypoint location
"""

import rospy

import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from std_msgs.msg import Float32MultiArray
from sound_play.msg import SoundRequest
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient
import numpy as np
import tf

original = 0

global start
start = 1
global move
move = 0
global name1_flag
name1_flag = 0
global start_flag
start_flag = 0
global male_1_flag
male_1_flag = 0
global female_1_flag
female_1_flag = 0
global male_2_flag
male_2_flag = 0
global drink1_flag
drink1_flag = 0
global drink1
drink1 = "abc"
global name1
name1 = "abc"
global waiting
waiting = 0


class NavToPoint:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        soundhandle = SoundClient()
        listener = tf.TransformListener()

        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient(
            "move_base", MoveBaseAction)

        rospy.loginfo("Waiting for move_base action server...")

        # Wait for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(120))
        rospy.loginfo("Connected to move base server")

        # A variable to hold the initial pose of the robot to be set by the user in RViz
        initial_pose = PoseWithCovarianceStamped()
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped,
                         self.update_initial_pose)
        rospy.Subscriber('/lm_data', String, self.checkmsg)
        # Get the initial pose from the user
        rospy.loginfo(
            "*** Click the 2D Pose Estimate button in RViz to set the robot's initial pose...")
        rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)

        # Make sure we have the initial pose
        while initial_pose.header.stamp == "" or start_flag == 0:
            rospy.sleep(1)
            rospy.loginfo("start_flag state %s", start_flag)

        rospy.loginfo("Ready to go")
        rospy.sleep(1)

        locations = dict()

        # Location A
        A_x = 4.75
        A_y = -3.54
        A_theta = 0

        quaternion = quaternion_from_euler(0.0, 0.0, A_theta)
        locations['A'] = Pose(Point(A_x, A_y, 0.000), Quaternion(
            quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

        # Location C
        C_x = 1.79
        C_y = 4.69
        C_theta = 0

        quaternion = quaternion_from_euler(0.0, 0.0, C_theta)
        locations['C'] = Pose(Point(C_x, C_y, 0.000), Quaternion(
            quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

        # Location D
        D_x = 1.79
        D_y = -3.696
        D_theta = 4.712

        quaternion = quaternion_from_euler(0.0, 0.0, C_theta)
        locations['D'] = Pose(Point(D_x, D_y, 0.000), Quaternion(
            quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

        self.goal = MoveBaseGoal()
        rospy.loginfo("Starting navigation test")

        while not rospy.is_shutdown():
            self.goal.target_pose.header.frame_id = 'map'
            self.goal.target_pose.header.stamp = rospy.Time.now()

            # Robot will go to point A
            if start == 1:
                rospy.loginfo("Going to point A")
                rospy.sleep(2)
                self.goal.target_pose.pose = locations['A']
                self.move_base.send_goal(self.goal)
                global waiting
                waiting = self.move_base.wait_for_result(rospy.Duration(300))
                waiting = 1
                if waiting == 1:
                    rospy.loginfo("Reached point A")
                    rospy.sleep(1)
                    global name1_flag
                    name1_flag = 0

                    global male_1_flag
                    male_1 = listener.frameExists("object_1")
                    rospy.loginfo("found male 1? %s", male_1)
                    if (male_1 == 1 and male_1_flag == 0):
                        global male_1_flag
                        male_1_flag = 1
                        rospy.loginfo("detected male 1")

                    global female_1_flag
                    female_1 = listener.frameExists("object_10")
                    rospy.loginfo("found female 2? %s", female_1)
                    if (female_1 == 1 and female_1_flag == 0):
                        global female_1_flag
                        female_1_flag = 1
                        rospy.loginfo("detected female 1")

                    if (female_1_flag == 1 or male_1_flag == 1):
                        while start == 1:
                            global name1_flag
                            if name1_flag == 0:
                                soundhandle.say('May i have your name please')
                                rospy.loginfo("May i have your name please")
                            rospy.sleep(100)

            if start == 2:
                rospy.loginfo("Going to point C")
                rospy.sleep(2)
                self.goal.target_pose.pose = locations['C']
                self.move_base.send_goal(self.goal)
                waiting = self.move_base.wait_for_result(
                    rospy.Duration(300))
                if waiting == 1:
                    rospy.loginfo("Reached point C")
                    rospy.sleep(2)
                    global male_2_flag
                    male_2 = listener.frameExists("object_3")
                    # rospy.loginfo("found john 1 status %s", male_1)
                    if (male_2 == 1 and male_2_flag == 0):
                        rospy.loginfo(
                            "found someone name is john and his fravourite drink is milk")
                        soundhandle.say(
                            'found someone name is john and his fravourite drink is milk')
                        rospy.sleep(2)
                        global male_2_flag
                        male_2_flag = 1
                        # rospy.loginfo("assign male flag 2")
                        self.goal.target_pose.pose = locations['D']
                        self.move_base.send_goal(self.goal)
                        waiting = self.move_base.wait_for_result(
                            rospy.Duration(300))
                        if waiting == 1:
                            rospy.loginfo("Reached point D")
                            global move
                            move = 1
                    soundhandle.say('here is an empty seat')
                    rospy.loginfo("here is an empty seat")
                    rospy.sleep(2)
                    soundhandle.say('The name of the guest is ')
                    rospy.loginfo("The name of the guest is ")
                    rospy.sleep(2)
                    global name1
                    soundhandle.say(name1)
                    rospy.loginfo(name1)
                    rospy.sleep(1)
                    global drink1
                    soundhandle.say('The fravourite drink is ')
                    rospy.loginfo("The fravourite drink is ")
                    rospy.sleep(2)
                    soundhandle.say(drink1)
                    rospy.loginfo(drink1)
                    rospy.sleep(1)
                    global start
                    start = 3

    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose
        if original == 0:
            self.origin = self.initial_pose.pose.pose
            global original
            original = 1

    def checkmsg(self, msg):
        # Print the recognized words on the screen
                # rospy.loginfo(msg.data)
        if msg.data.find('GO') > -1:
            global start_flag
            start_flag = 1
            global name1_flag
            global waiting

        global start
        global name1
        global name1_flag
        global drink1
        global drink1_flag
        global name2
        global name2_flag
        global drink2
        global drink2_flag
        global waiting

        # rospy.loginfo("msg data is  %s",msg.data)
        # rospy.loginfo("name1 is  %s",name1)
        # rospy.loginfo("name1 flag is  %s",name1_flag)
        # rospy.loginfo("drink1 is  %s",drink1)
        # rospy.loginfo("drink1 flag is  %s",drink1_flag)
        # rospy.loginfo("name2 is  %s",name2)
        # rospy.loginfo("name2 flag is  %s",name2_flag)
        # rospy.loginfo("drink2 is  %s",drink2)
        # rospy.loginfo("drink2 flag is  %s",drink2_flag)
        # rospy.loginfo("start is  %s",start)
        # rospy.loginfo("waiting is  %s",waiting)

        soundhandle = SoundClient()
        if name1 != "abc" and name1_flag == 0:
            if msg.data.find('CORRECT') > -1:
                global name1_flag
                name1_flag = 1
                # global name1
                # name1 = msg.data
                rospy.loginfo("name stored")
                soundhandle.say('What is your favourite drink')
                rospy.loginfo("What is your favourite drink")
                rospy.sleep(2)

        if name1_flag == 0 and start == 1 and waiting == 1:
            rospy.sleep(4)
            soundhandle.say('received')
            rospy.loginfo("received")
            rospy.sleep(1)
            rospy.loginfo("Received data is %s", msg.data)
            rospy.loginfo(
                "Please say correct if your name is correct if not say your name again")
            soundhandle.say(
                'Please say correct if your name is correct if not say your name again')
            rospy.sleep(3)
            global name1
            name1 = msg.data
            rospy.loginfo(name1)
            rospy.sleep(3)

        if name1_flag == 1 and start == 1 and waiting == 1 and drink1_flag == 0:
            rospy.sleep(4)
            soundhandle = SoundClient()
            soundhandle.say('received')
            rospy.loginfo("received")
            rospy.sleep(1)
            rospy.loginfo("Received data is  %s", msg.data)
            rospy.loginfo(
                "Please say the word yes to confirm your drink")
            soundhandle.say(
                'Please say the word yes to confirm your drink')
            rospy.sleep(3)
            global drink1
            drink1 = msg.data
            rospy.loginfo(drink1)
            rospy.sleep(3)

        if drink1 != "abc" and name1_flag == 1 and drink1_flag == 0:
            if msg.data.find('YES') > -1:
                global drink1_flag
                drink1_flag = 1
                rospy.loginfo("drink stored")
                global start
                start = 2
                rospy.loginfo("please follow me to your seat")
                soundhandle.say('please follow me to your seat')

    def cleanup(self):
        rospy.loginfo("Shutting down navigation	....")
        self.move_base.cancel_goal()


if __name__ == "__main__":
    rospy.init_node('navi_point')
    try:
        NavToPoint()
        rospy.spin()
    except:
        pass
