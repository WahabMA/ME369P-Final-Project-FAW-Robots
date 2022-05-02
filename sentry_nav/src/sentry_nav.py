#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2

x = 0.0
y = 0.0 
theta = 0.0

def newOdom(msg):
    global x
    global y
    global theta
    
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    
    rot_q = msg.pose.pose.orientation
    roll,pitch,theta = euler_from_quaternion([rot_q.x,rot_q.y,rot_q.z,rot_q.w])
    
rospy.init_node('test')

sub = rospy.Subscriber("/spy/odom",Odometry,newOdom)
pub = rospy.Publisher('/spy/cmd_vel',Twist,queue_size=1)

speed = Twist()

r = rospy.Rate(50)

goal = Point(4,5,0)

while True:
    inc_x = goal.x - x
    inc_y = goal.y - y
    angle_to_goal = atan2(inc_y,inc_x)
    
    if 0 < inc_x < 0.01 and 0 < inc_y < 0.01:
        speed.linear.x = 0.0
        speed.angular.z = 0.0
    elif angle_to_goal - theta > 0.1:
        speed.linear.x = 0.0
        speed.angular.z = 0.3
    elif angle_to_goal - theta < -0.1:
        speed.linear.x = 0.0
        speed.angular.z = -0.3
    else:
        speed.linear.x = 0.1
        speed.angular.z = 0.0
    
        
    pub.publish(speed)
    r.sleep()
