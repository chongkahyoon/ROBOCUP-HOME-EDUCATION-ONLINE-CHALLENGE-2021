#!/usr/bin/env python

import rospy, os, sys

import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from sound_play.msg import SoundRequest
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient

import tf

original = 0
global move
move = 0
global male_1_flag
male_1_flag = 0
global female_1_flag
female_1_flag = 0
global female_2_flag
female_2_flag = 0
global old_flag
old_flag = 0
global start
start = 1
global waiting
waiting = 0
global start_flag
start_flag = 0
global name1_flag
name1_flag = 0
global drink1_flag
drink1_flag = 0
global name1
name1 = "abc"
global drink1
drink1 = "abc"
global name2_flag
name2_flag = 0
global drink2_flag
drink2_flag = 0
global name2
name2 = "abc"
global drink1
drink2 = "abc"
global name3_flag
name3_flag = 0
global age_1
age_1 = "abc"
global age_2
age_2 = "abc"
global age1_flag
age1_flag = 0
global age2_flag
age2_flag = 0



class NavToPoint:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        soundhandle = SoundClient()
        listener = tf.TransformListener()
	# Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        rospy.loginfo("Waiting for move_base action server...")

        # Wait for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(120))
        rospy.loginfo("Connected to move base server")
        
        # A variable to hold the initial pose of the robot to be set by the user in RViz
        initial_pose = PoseWithCovarianceStamped()
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)
        rospy.Subscriber('/lm_data', String, self.checkmsg)



	# Get the initial pose from the user
        rospy.loginfo("*** Click the 2D Pose Estimate button in RViz to set the robot's initial pose...")
        rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)
        
        # Make sure we have the initial pose
        while initial_pose.header.stamp == "" or start_flag == 0:
        	rospy.sleep(1)
        	rospy.loginfo("start_flag state %s",start_flag)
			
            
        rospy.loginfo("Ready to go")
        soundhandle = SoundClient()
        soundhandle.say('Ready to go')
	rospy.sleep(2)

	locations = dict()

	# Location A
	A_x = 4.75
	A_y = -2.73
	A_theta = -0.14

	# quaternion[2] = -0.84
	# quaternion[3] = 0.53
	quaternion = quaternion_from_euler(0.0, 0.0, A_theta)
	locations['A'] = Pose(Point(A_x, A_y, 0.000), Quaternion(
		quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	# Location B
	B_x = 2.71
	B_y = 4.49
	B_theta = 2.937

	quaternion = quaternion_from_euler(0.0, 0.0, B_theta)
	locations['B'] = Pose(Point(B_x, B_y, 0.000), Quaternion(
		quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	# Location C
	C_x = 1.27
	C_y = 5.61
	C_theta = 2.937

	quaternion = quaternion_from_euler(0.0, 0.0, C_theta)
	locations['C'] = Pose(Point(C_x, C_y, 0.000), Quaternion(
		quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	# Location D
	D_x = 1.25
	D_y = 5.14
	D_theta = 1.6

	quaternion = quaternion_from_euler(0.0, 0.0, D_theta)
	locations['D'] = Pose(Point(D_x, D_y, 0.000), Quaternion(
		quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	# Location E
	E_x = 1.32
	E_y = 4.43
	E_theta = 3.002

	quaternion = quaternion_from_euler(0.0, 0.0, E_theta)
	quaternion[2] = 0.998
	quaternion[3] = 0.055
	locations['E'] = Pose(Point(E_x, E_y, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))
	
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
		waiting = self.move_base.wait_for_result(rospy.Duration(300))
		global waiting
		waiting = 1
		if waiting == 1:
			rospy.loginfo("Reached point A")
			rospy.sleep(1)
			name1_flag = 0

			global female_1_flag
			female_1 = listener.frameExists("object_1")
			rospy.loginfo("found female 1? %s", female_1)
			if (female_1 == 1 and female_1_flag == 0):
				global female_1_flag
				female_1_flag = 1
				rospy.loginfo("detected female1")

			global female_2_flag
			female_2 = listener.frameExists("object_4")
			rospy.loginfo("found female 2? %s", female_2)
			if (female_2 == 1 and female_2_flag == 0):
				global female_2_flag
				female_2_flag = 1
				rospy.loginfo("detected female2")

			if female_1_flag == 1 or female_2_flag == 1:
				while start == 1:
					global name1_flag
					if name1_flag == 0:
						soundhandle.say('please tell me your name')
						rospy.loginfo("please tell me your name")
						rospy.sleep(30)


	  if start == 2:
		rospy.loginfo("Going to next point")
		global age_1
		if age_1.find('ELEVEN')>-1:
			rospy.loginfo("point C")
			self.goal.target_pose.pose = locations['C']
			self.move_base.send_goal(self.goal)
			waiting = self.move_base.wait_for_result(rospy.Duration(300))
		else:
			rospy.loginfo("point B")
			self.goal.target_pose.pose = locations['B']
			self.move_base.send_goal(self.goal)
			waiting = self.move_base.wait_for_result(rospy.Duration(300))
			waiting = self.move_base.wait_for_result(rospy.Duration(300))
		if waiting == 1:
			rospy.loginfo("Reached point")
			rospy.sleep(3)
			global male_1_flag
			male_1 = listener.frameExists("object_5")
			# rospy.loginfo("found john 1 status %s", male_1)
			if (male_1 == 1 and male_1_flag == 0):
				rospy.loginfo("this is john and his favourite drink is milk")
				soundhandle.say('this is john and his favourite drink is milk')
				rospy.sleep(2)
				global male_1_flag
				male_1_flag = 1
				# rospy.loginfo("assign male flag 1")
				self.goal.target_pose.pose = locations['D']
				self.move_base.send_goal(self.goal)
				waiting = self.move_base.wait_for_result(rospy.Duration(300))
				if waiting == 1:
					rospy.loginfo("Reached point D")
					global move
					move = 1
			seat_1 = listener.frameExists("object_2")
			rospy.loginfo("found empty seat? %s", seat_1)
			if seat_1 == 1:
   				soundhandle.say('here is an empty seat')
				rospy.loginfo("here is an empty seat")
			rospy.sleep(2)
			soundhandle.say('The name of the guest is ')
			rospy.loginfo("The name of the guest is ")
			rospy.sleep(3)
			global name1
			soundhandle.say(name1)
			rospy.loginfo(name1)
			rospy.sleep(1)
			global drink1
			soundhandle.say('The favourite drink is ')
			rospy.loginfo("The favourite drink is ")
			rospy.sleep(2)
			soundhandle.say(drink1)
			rospy.loginfo(drink1)
			rospy.sleep(1)
			global start
			start = 3

	  if start == 3:
		rospy.loginfo("Going to point A")
		rospy.sleep(2)
		self.goal.target_pose.pose = locations['A']
	  	self.move_base.send_goal(self.goal)
		waiting = self.move_base.wait_for_result(rospy.Duration(300))
		if waiting == 1:
			rospy.loginfo("Reached point A")
			rospy.sleep(1)
			
			global female_1_flag
			female_1 = listener.frameExists("object_1")
			rospy.loginfo("found female 1? %s", female_1)
			if (female_1 == 1 and female_1_flag == 0):
				global female_1_flag
				female_1_flag = 1
				rospy.loginfo("detected female1")

			global female_2_flag
			female_2 = listener.frameExists("object_4")
			rospy.loginfo("found female 2? %s", female_2)
			if (female_2 == 1 and female_2_flag == 0):
				global female_2_flag
				female_2_flag = 1
				rospy.loginfo("detected female2")

			if female_1_flag == 1 and female_2_flag == 1:
				while start == 3:
					global name2_flag
					if name2_flag == 0:
						soundhandle.say('please tell me your name')
						rospy.loginfo("please tell me your name")
						rospy.sleep(30)

	  if start == 4:
		rospy.loginfo("Going to next point")
		global age_2
		if age_2.find('ELEVEN')>-1:
			rospy.loginfo("point C")
			self.goal.target_pose.pose = locations['C']
			self.move_base.send_goal(self.goal)
			waiting = self.move_base.wait_for_result(rospy.Duration(300))
		else:
			rospy.loginfo("point B")
			self.goal.target_pose.pose = locations['B']
			self.move_base.send_goal(self.goal)
			waiting = self.move_base.wait_for_result(rospy.Duration(300))
			waiting = self.move_base.wait_for_result(rospy.Duration(300))
		if waiting == 1:
			rospy.loginfo("Reached point")
			rospy.sleep(1)
			global male_1
			global male_1_flag
			male_1 = listener.frameExists("object_24")
			if (male_1 == 1 and male_1_flag == 0):
				rospy.loginfo("found someone name is john and his fravourite drink is milk")
				soundhandle.say('found someone name is john and his fravourite drink is milk')
				rospy.sleep(2)
				male_1_flag = 1
				self.goal.target_pose.pose = locations['E']
				self.move_base.send_goal(self.goal)
				waiting = self.move_base.wait_for_result(rospy.Duration(300))
				if waiting == 1:
					rospy.loginfo("Reached point E")
					global start
		    		start = 6
			seat_2 = listener.frameExists("object_6")
			rospy.loginfo("found empty seat? %s", seat_1)
			if seat_2 == 1:
   				soundhandle.say('here is an empty sofa seat')
				rospy.loginfo("here is an empty sofa seat")
			rospy.sleep(3)
			soundhandle.say('The name of the guest is ')
			rospy.loginfo("The name of the guest is ")
			rospy.sleep(3)
			global name2
			soundhandle.say(name2)
			rospy.loginfo(name2)
			rospy.sleep(1)
			global drink2
			soundhandle.say('The favourite drink is ')
			rospy.loginfo("The favourite drink is ")
			rospy.sleep(2)
			soundhandle.say(drink2)
			rospy.loginfo(drink2)
			rospy.sleep(2)
			global start
			if start == 4:
				start = 0

	  # After reached point A, robot will go back to initial position
	  elif start == 0:
		rospy.loginfo("Going back home")
		soundhandle = SoundClient()
		soundhandle.say('Thank you')
		rospy.sleep(2)
		self.goal.target_pose.pose = self.origin
		self.move_base.send_goal(self.goal)
		waiting = self.move_base.wait_for_result(rospy.Duration(300))
		if waiting == 1:
		    rospy.loginfo("Reached home")
		    rospy.sleep(2)

	  rospy.Rate(5).sleep()


    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose
	if original == 0:
		self.origin = self.initial_pose.pose.pose
		global original
		original = 1

    def checkmsg(self, msg):
        # Print the recognized words on the screen
		# rospy.loginfo(msg.data)
		if msg.data.find('GO')>-1:
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
		global age_1
		global age_2
		global age1_flag
		global age2_flag


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
			if msg.data.find('CORRECT')>-1:
				global name1_flag
				name1_flag = 1
				# global name1
				# name1 = msg.data
				rospy.loginfo("name stored")
				soundhandle.say('What is your favourite drink')
				rospy.loginfo("What is your favourite drink")
				rospy.sleep(2)

		if name1_flag == 0 and start == 1 and waiting == 1:
			soundhandle = SoundClient()
			if msg.data != "YES" and msg.data != "CORRECT" and msg.data != "":
				soundhandle.say('received')
				rospy.loginfo("received")
				rospy.sleep(1)
				rospy.loginfo("Received data is %s",msg.data)
				rospy.loginfo("Please reply the word correct or repeat your name once again")
				soundhandle.say('Please reply the word correct or repeat your name once again')
				rospy.sleep(3)
				global name1
				name1 = msg.data
				rospy.loginfo(name1)
				soundhandle.say(name1)
			rospy.sleep(3)
			
		if drink1 != "abc" and name1_flag == 1 and drink1_flag == 0:
			if msg.data.find('CORRECT')>-1:
				global drink1_flag
				drink1_flag = 1
				rospy.loginfo("drink stored")
				rospy.loginfo("What is your age")
				soundhandle.say('What is your age')
				rospy.sleep(2)

		if name1_flag == 1 and start == 1 and waiting == 1 and drink1_flag == 0:
			soundhandle = SoundClient()
			if msg.data != "YES" and msg.data != "CORRECT" and msg.data != "":
				soundhandle.say('received')
				rospy.loginfo("received")
				rospy.sleep(1)
				rospy.loginfo("Received data is  %s",msg.data)
				rospy.loginfo("Please reply the word correct or repeat your drink once again")
				soundhandle.say('Please reply the word correct or repeat your drink once again')
				rospy.sleep(3)
				global drink1
				drink1 = msg.data
				soundhandle.say(drink1)
				rospy.loginfo(drink1)
			rospy.sleep(2)

		if drink1_flag == 1 and start == 1 and waiting == 1 and age1_flag == 0:
			soundhandle = SoundClient()
			if msg.data != "YES" and msg.data != "CORRECT" and msg.data != "":
				soundhandle.say('received')
				rospy.loginfo("received")
				rospy.sleep(1)
				rospy.loginfo("Received data is  %s",msg.data)
				rospy.loginfo("Please reply the word yes or repeat your age once again")
				soundhandle.say('Please reply the word yes or repeat your age once again')
				rospy.sleep(3)
				global age_1
				age_1 = msg.data
				soundhandle.say(age_1)
				rospy.loginfo(age_1)
			rospy.sleep(2)

		if age_1 != "abc" and age1_flag == 0 and drink1_flag == 1:
			if msg.data.find('YES')>-1:
				global age1_flag
				age1_flag = 1
				rospy.loginfo("age stored")
				global start
				start = 2
				rospy.loginfo("please follow me to your seat")
				soundhandle.say('please follow me to your seat')
		###########################################################
		if name2 != "abc" and name2_flag == 0 and start == 3:
			if msg.data.find('CORRECT')>-1:
				global name2_flag
				name2_flag = 1
				rospy.loginfo("name stored")
				soundhandle.say('What is your favourite drink')
				rospy.loginfo("What is your favourite drink")
				rospy.sleep(2)

		if name2_flag == 0 and start == 3 and waiting == 1:
			soundhandle = SoundClient()
			if msg.data != "YES" and msg.data != "CORRECT" and msg.data != "":
				soundhandle.say('received')
				rospy.loginfo("received")
				rospy.sleep(1)
				rospy.loginfo("Received data is %s",msg.data)
				soundhandle.say('Please reply the word correct or repeat your name once again')
				rospy.loginfo("Please reply the word correct or repeat your name once again")
				rospy.sleep(3)
				global name2
				name2 = msg.data
				soundhandle.say(name2)
				rospy.loginfo(name2)
				rospy.loginfo("feedback is  %s",msg.data)
			rospy.sleep(2)

		if drink2 != "abc" and name2_flag == 1 and drink2_flag == 0 and start == 3:
			if msg.data.find('CORRECT')>-1:
				global drink2_flag
				drink2_flag = 1
				rospy.loginfo("drink stored")
				rospy.loginfo("What is your age")
				soundhandle.say('What is your age')
				rospy.sleep(2)

		if name2_flag == 1 and start == 3 and waiting == 1 and drink2_flag == 0:
			soundhandle = SoundClient()
			if msg.data != "YES" and msg.data != "CORRECT" and msg.data != "":
				soundhandle.say('received')
				rospy.loginfo("received")
				rospy.sleep(1)
				rospy.loginfo("Received data is %s",msg.data)
				rospy.loginfo("Please reply the word correct or repeat your drink once again")
				soundhandle.say('Please reply the word correct or repeat your drink once again')
				rospy.sleep(3)
				global drink2
				drink2 = msg.data
				soundhandle.say(drink2)
				rospy.loginfo(drink2)
			rospy.sleep(2)
   
		if drink2_flag == 1 and start == 3 and waiting == 1 and age2_flag == 0:
			soundhandle = SoundClient()
			if msg.data != "YES" and msg.data != "CORRECT" and msg.data != "":
				soundhandle.say('received')
				rospy.loginfo("received")
				rospy.sleep(1)
				rospy.loginfo("Received data is  %s",msg.data)
				rospy.loginfo("Please reply the word yes or repeat your age once again")
				soundhandle.say('Please reply the word yes or repeat your age once again')
				rospy.sleep(3)
				global age_2
				age_2 = msg.data
				rospy.loginfo(age_2)
				soundhandle.say(age_2)
			rospy.sleep(2)
   
		if age_2 != "abc" and age2_flag == 0 and drink2_flag == 1:
			if msg.data.find('YES')>-1:
				global age2_flag
				age2_flag = 1
				rospy.loginfo("age stored")
				global start
				start = 4
				rospy.loginfo("please follow me to your seat")
				soundhandle.say('please follow me to your seat')
		#######################################################################


    def cleanup(self):
        rospy.loginfo("Shutting down navigation	....")
        self.move_base.cancel_goal()

if __name__=="__main__":
	rospy.init_node('navi_point')
	listener = tf.TransformListener()
	try:
		NavToPoint()
		rospy.spin()
	except:
		pass
