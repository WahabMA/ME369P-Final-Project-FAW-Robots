#!/usr/bin/env python3


import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
import random
import sys


spypose = Odometry()
playerpose = Odometry()
playerpose.pose.pose.position.x = 0.5
playerpose.pose.pose.position.y = 0.5

def getSpyMsg(msg):
    global spypose
    spypose = msg
    
def getPlayerMsg(msg):
    global playerpose
    playerpose = msg

def getMsgInfo(msg):
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    
    rot_q = msg.pose.pose.orientation
    roll,pitch,theta = euler_from_quaternion([rot_q.x,rot_q.y,rot_q.z,rot_q.w])
    return x,y,theta

def setSpyTwist(pub,goal):
    inc_x = 0
    inc_y = 0
    vel = Twist()
    while not(0 < abs(inc_x) < 0.1) or not(0 < abs(inc_y) < 0.1):
        x,y,theta = getMsgInfo(spypose)
        # print(x,y)
        inc_x = goal.x - x
        inc_y = goal.y - y
        angle_to_goal = atan2(inc_y,inc_x)
        
        if 0 < abs(inc_x) < 0.1 and 0 < abs(inc_y) < 0.1:
            vel.linear.x = 0.0
            vel.angular.z = 0.0
        elif angle_to_goal - theta > 0.1:
            vel.linear.x = 0.0
            vel.angular.z = 0.2
        elif angle_to_goal - theta < -0.1:
            vel.linear.x = 0.0
            vel.angular.z = -0.2
        else:
            vel.linear.x = 0.3
            vel.angular.z = 0.0
        pub.publish(vel)
        r.sleep()
        
def setPlayerTwist(pub,goal):
    inc_x = 0
    inc_y = 0
    vel = Twist()
    while not(0 < abs(inc_x) < 0.1) or not(0 < abs(inc_y) < 0.1):
        x,y,theta = getMsgInfo(playerpose)
        # print(x,y)
        inc_x = goal.x - x
        inc_y = goal.y - y
        angle_to_goal = atan2(inc_y,inc_x)
        
        if 0 < abs(inc_x) < 0.1 and 0 < abs(inc_y) < 0.1:
            vel.linear.x = 0.0
            vel.angular.z = 0.0
        elif angle_to_goal - theta > 0.1:
            vel.linear.x = 0.0
            vel.angular.z = 0.2
        elif angle_to_goal - theta < -0.1:
            vel.linear.x = 0.0
            vel.angular.z = -0.2
        else:
            vel.linear.x = 0.3
            vel.angular.z = 0.0
        pub.publish(vel)
        r.sleep()

rospy.init_node('overall_nav')

spysub = rospy.Subscriber("/spy/odom",Odometry,getSpyMsg)
spypub = rospy.Publisher('/spy/cmd_vel',Twist,queue_size=1)
playersub = rospy.Subscriber('/player/odom',Odometry,getPlayerMsg)
playerpub = rospy.Publisher('/player/cmd_vel',Twist,queue_size=1)
# obstaclessub = rospy.Subscriber('/obstacles',obstacles)

spyvel = Twist()
playervel = Twist()

r = rospy.Rate(50)

spypossiblepos = [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5]

while True:
    
    playerx,playery,playertheta = getMsgInfo(playerpose)
    playerx = round(playerx*2)/2
    playery = round(playery*2)/2
    
    validInput = False
    while not validInput:
        player_input = input("Enter your next move --> ")
        if player_input in ['w','W']:
            playergoal = Point(playerx+1,playery,0)
            validInput = True
        elif player_input in ['s','S']:
            playergoal = Point(playerx-1,playery,0)
            validInput = True
        elif player_input in ['d','D']:
            playergoal = Point(playerx,playery-1,0)
            validInput = True
        elif player_input in ['a','A']:
            playergoal = Point(playerx,playery+1,0)
            validInput = True
        else:
            print('invalid move')
    # print(playergoal)
    # print(playerx,playery)
    setPlayerTwist(playerpub,playergoal)
    
    spyx,spyy,spytheta = getMsgInfo(spypose)
    spygoal = Point(8.5,random.choice(spypossiblepos),0)
    # print(spygoal)
    # print(spyx,spyy)
    setSpyTwist(spypub,spygoal)
    
    

