#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
import numpy as np
import roslaunch 
import sys

   
            
def main():
    
    # To randomize the starting position of both robots
    GameOver=False
    col = [0,1,2,3,4,5,6,7]
    y1=np.random.choice(col)
    playery=0.5+y1
    col.remove(y1)
    playerx=0.5
    current_player=[playerx,playery]

    y2=np.random.choice(col)
    sentryy=0.5+y2
    sentryx=8.5
    current_sentry=[sentryx, sentryy]

    obs_points=[]
    a=[1,2,3,4,5,6,7] # x-values
    b=[0,1,2,3,4,5,6,7] # y-values

    counter=1
    

    # To initialize the position of both robots
    arg_1 = 'first_tb3_y_pos:='+str(playery)
    arg_2 = 'second_tb3_y_pos:= '+str(sentryy)

    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)

    cli_args = ['turtlebot3_gazebo','SPYxROS.launch', arg_1,arg_2]
    roslaunch_args=cli_args[1:]
    roslaunch_file=roslaunch.rlutil.resolve_launch_arguments(cli_args)[0]
    launch_files=[(roslaunch_file,roslaunch_args)]
    
    sys.stdout.write("Welcome to the game!")
    sys.stdout.write('\n')
    sys.stdout.write('Avoid being seen by the sentry! (obstacles help with hiding)')
    sys.stdout.write('\n')
    cli_args1=['my_wall_urdf','wall.launch']
    while counter<6:
        x=np.random.choice(a)
        y=np.random.choice(b)
        # Repeat the process 
        arg_1= 'x'+str(counter)+':='+str(x)
        arg_2= 'y'+str(counter)+':='+str(y)
        arg_3= 'model'+str(counter)+':=wall'+str(counter)       
        cli_args1.append(arg_1)
        cli_args1.append(arg_2)
        cli_args1.append(arg_3)
        a.remove(x)
        b.remove(y)
        counter+=1
            
    roslaunch_args1=cli_args1[2:]
    roslaunch_file1=roslaunch.rlutil.resolve_launch_arguments(cli_args1)[0]
    launch_files.append((roslaunch_file1,roslaunch_args1))
    #sys.stdout.write(launch_files)
    
    parent = roslaunch.parent.ROSLaunchParent(uuid,launch_files)
    parent.start()

    sys.stdout.write('Good luck')
    sys.stdout.write('\n')
    usin = 'waiting'
    while not GameOver:
        sys.stdout.write('Use WASD to move (q to QUIT)')
        sys.stdout.write('\n')
        sys.stdout.write('Insert Your Next Action: ')
        usin= str(input())
        sys.stdout.write('\n')
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
    
        
        
        
    
