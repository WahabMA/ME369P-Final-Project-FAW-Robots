#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
import numpy as np
import roslaunch 
import sys
import rospkg



def newOdom (msg):
    global x
    global y
    global theta
    
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y
    
    rot_q=msg.pose.pose.orientation 
    (roll, pitch, theta)=euler_from_quaternion([rot_q.x,rot_q.y,rot_q.z,rot_q.w])
    

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
    rospack = rospkg.RosPack()
    
    # To randomize the starting position of both robots
    GameOver=False
    y1=np.random.randint(8)
    playery=0.5+y1
    playerx=0.5
    current_player=[playerx,playery]

    y2=np.random.randint(8)
    sentryy=0.5+y2
    sentryx=8.5
    current_sentry=[sentryx, sentryy]

    obs_points=[]
    a=[1,2,3,4,5,6,7]
    b=[0,1,2,3,4,5,6,7]

    counter=0
    

    # To initialize the position of both robots
    arg_1 = 'first_tb3_y_pos:='+str(playery)
    arg_2 = 'second_tb3_y_pos:= '+str(sentryy)

    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    
    launch_path = rospack.get_path('turtlebot3_gazebo')+'/SPYxROS.launch'

    cli_args = ['turtlebot3_gazebo','SPYxROS.launch', arg_1,arg_2]
    roslaunch_args=cli_args[1:]
    roslaunch_file=roslaunch.rlutil.resolve_launch_arguments(cli_args)[0]
    launch_files=[(roslaunch_file,roslaunch_args)]
    
    sys.stdout.write("Welcome to the game!")
    sys.stdout.write('\n')
    sys.stdout.write('Avoid being seen by the sentry! (obstacles help with hiding)')
    sys.stdout.write('\n')
    cli_args1=['my_wall_urdf','wall.launch']
    while counter<5:
        x=np.random.choice(a)
        y=np.random.choice(b)
        # Repeat the process 
        launch_path1 = rospack.get_path('my_wall_urdf')+'/wall.launch'
        arg_1= 'x:='+str(x)
        arg_2= 'y:='+str(y)
        arg_3= 'model:=wall'+str(counter)       
        cli_args1=[arg_1,arg_2,arg_3]
        roslaunch_args1=cli_args1[1:]
        roslaunch_file1=roslaunch.rlutil.resolve_launch_arguments(cli_args1)[0]
        launch_files.append((roslaunch_file1,roslaunch_args1))
        counter+=1
            
    #sys.stdout.write(launch_files)
    
    parent = roslaunch.parent.ROSLaunchParent(uuid,launch_files)
    parent.start()
    
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
        
        
        
        
        
        
if __name__ == '__main__':
    main()
    
        
        
        
    
