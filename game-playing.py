#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
import numpy as np
import roslaunch 
import sys


def newOdom (msg):
    global x
    global y
    global theta
    
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y
    
    rot_q=msg.pose.pose.orientation 
    (roll, pitch, theta)=euler_from_quaternion([rot_q.x,rot_q.y,rot_q.z,rot_q.w])
    
rospy.init_node("speed_controller")

sub = rospy.Subscriber("/odometry/filtered", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist,queue_size=1)

speed = Twist()

r=rospy.Rate(4)

def goTo(nx,ny):
    global x
    global y
    global theta
    
    goal=Point ()
    goal.x=nx
    goal.y=ny
    
    while not rospy.is_shutdown() and not(theta==0 and goal.x==x and goal.y==y):
        inc_x=goal.x-x
        inc_y=goal.y-y
        
        angle_to_goal=atan2(inc_y, inc_x)
        
        if abs(angle_to_goal-theta)>0:
            speed.linear.x=0.0
            speed.angular.z=0.3
        elif (abs(inc_x) and abs(inc_y))>0:
            speed.linear.x=0.5
            speed.angukar.z=0.0
        elif abs(theta)>0:
            speed.linear.x=0.0
            speed.angular.z=0.3
        else:
            speed.linear.x=0.0
            speed.angular.z=0.0
            
        pub.publish(speed)
        r.sleep()
            
def main():
    # To randomize the starting position of both robots
    GameOver=False
    y1=np.randint(8)
    playery=0.5+y1
    playerx=0.5
    current_player=[playerx,playery]

    y2=np.randint(8)
    sentryy=0.5+y2
    sentryx=8.5
    current_sentry=[sentryx, sentryy]

    obs_points=[]
    a=[1,2,3,4,5,6,7]
    b=[0,1,2,3,4,5,6,7]

    counter=0

    # To initialize the position of both robots
    arg_1 = 'first_tb3_y_pos:='+playery
    arg_2 = 'second_tb3_y_pos:= '+sentryy

    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)

    cli_args = ['turtlebot3_gazebo', 'SPYxROS.launch', arg_1,arg_2]
    roslaunch_args=cli_args[2:]
    roslaunch_file=[(roslaunch.rutil.resolve_launch_arguments(cli_args)[0], roslaunch_args)]

    parent = roslaunch.parent.ROSLaunchParent(uuid,roslaunch_file)
    parent.start()
    
    # Print statements to the terminal to explain
    sys.stdout.write("Welcome to the game!")
    sys.stdout.write('\n')
    sys.stdout.write('Avoid being seen by the sentry! (obstacles help with hiding)')
    sys.stdout.write('\n')
    sys.stdout.write('Enter the number of obstacles you want (int, recommend 4): ')
    obs = int(input())
    sys.stdout.write('\n')
    if obs==4:
        sys.stdout.write('Wow, are you really gonna listen to me?')
        sys.stdout.write('\n')
    while counter<obs:
        x=np.random.choice(a)
        y=np.random.choice(b)
        if [x,y] not in obs_points:
            # Repeat the process 
            arg_1= 'x:='+x
            arg_2= 'y:='+y
            arg_3= 'model:=wall'+counter
            uuid = roslaunch.rutil.get_or_generate_uuid(None, False)
            roslaunch.configure_logging(uuid)
            cli_args=['my_wall_urdf','wall.launch',arg_1,arg_2,arg_3]
            roslaunch_args=cli_args[2:]
            roslaunch_file=[roslaunch.rutil.resolve_launch_arguments(cli_args)[0],roslaunch_args]
            parent=roslaunch.parent.ROSLaunchParent(uuid,roslaunch_file)
            parent.start()
            counter+=1
    sys.stdout.write('Good luck')
    usin = 'waiting'
    while not GameOver:
        sys.stdout.write('Use WASD to move (q to QUIT)')
        sys.stdout.write('\n')
        sys.stdout.write('Insert Your Next Action: ')
        usin= str(input())
        sys.stdout.write('\m')
        # Add logic here to get the current position of the player and the obstacles
        
        # Inside the if statements we run logic to see if the player can move there and then set up the motion
        if usin.lower() =='w':
            pass
        elif usin.lower()=='a':
            pass
        elif usin.lower()=='s':
            pass
        elif usin.lower()=='d':
            pass
        elif usin.lower()=='q':
            GameOver=True
        else:
            sys.stdout.write('Invalid Input, please try again')
            continue
        # Outside of the if statements we run the sentry and player at the same time 
        
        # Finally we check to see if player and spy are in the same row, if they are then check if there is an obstacle 
        # between them, if not, the player dies
        
        
        
        
        
        
        
        
        
        
    
