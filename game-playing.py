#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from std_msgs.msg import String, Int32
from math import atan2
import numpy as np
import roslaunch 
import sys
import rospy
from std_msgs.msg import String
from turtle import position
from nav_msgs.msg import Odometry
from ast import List

from gazebo_msgs.msg import ModelStates
global obpose

spypose = Odometry()
playerpose = Odometry()

global caught

def getSpyMsg(msg):
    global spypose
    spypose = msg
    
def getPlayerMsg(msg):
    global playerpose
    playerpose = msg

def getObMsg(msg):
    global obpose
    obpose.append(msg)

def getMsgInfo(msg):
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    
    return x,y     
        
def gen_grid(size):
    # creates blank grid as a list
    grid = []
    for x in range(size):
        for y in range(size):
            grid[x][y].append(0)
    return grid
    
def set_grid(grid):
    # get model names from gazebo
#    rospy.wait_for_service('/gazebo/get_world_properties')
#    try:
#        gwp = rospy.ServiceProxy('/gazebo/get_world_properties')
#        prop = gwp()
#        models = prop.model_names
        # get relative link in each model
#        links = []
#        for i in models:
#            rospy.wait_for_service('/gazebo/get_model_properties')
#            try:
#                 gmp = rospy.ServiceProxy('gazebo/get_model_properties')
#                 m_prop = gmp(models(i))
#                 links.append(m_prop.body_names)
#            except rospy.ServiceException as e:
#                rospy.loginfo("Service call failed: {0}".format(e))

#    except rospy.ServiceException as e:
#        rospy.loginfo("Service call failed: {0}".format(e))

    # populates the grid with the model positions. Models need to be defined later

    # sentry model - first object in simulation
#    sen_pos = get_pos(models(2),links(2)(0))
    sen_x,sen_y = getMsgInfo(spypose)
    sen_x = np.floor(sen_x)
    sen_y = np.floor(sen_y)
    grid[sen_x][sen_y] = 's'

    # player model - second object in sumulation
#    play_pos = get_pos(models(0),links(0)(0))
    play_x, play_y = getMsgInfo(playerpose)
    play_x = np.floor(play_x)
    play_y = np.floor(play_y)
    grid[play_x][play_y] = 'p'

    ob_x = []
    ob_y = []

    for i in range(len(obpose)):
        if i%2 == 0:
            ob_x.append(obpose[i])
        else:
            ob_y.append(obpose[i])

    for i in range(len(ob_x)):
        ob_x[i] = np.floor(ob_x[i])
        ob_y[i] = np.floor(ob_y[i])
        grid[ob_x[i]][ob_y[i]] = 'b'
    
    # variable numbers of obstacles. Any models in the simulation after the first two
 #   for ob in range(3,len(models)):
 #       ob_pos = get_pos(models(ob),links(ob)(0))
 #       ob_x = np.floor(ob_pos[0])
 #       ob_y = np.floor(ob_pos[1])
 #       grid[ob_x][ob_y] = 'b'

#        ob_fpos = [ob_x,ob_y]

#        pub = rospy.Publisher('obstacles', int32 , queue_size=10)

#        pub.publish(ob_x, ob_y)
    
    return grid

def detection(grid):
    # checks if player is detected our not, should be run once per turn
    ob_x = []
    ob_y = []
    for x in grid:
        for y in grid[0]:
            if grid[x][y] == 's':
                sen_x = x
                sen_y = y
            if grid[x][y] == 'p':
                play_x = x
                play_y = y
            if grid[x][y] == 'b':
                ob_x.append(x)
                ob_y.append(y)
    if sen_x == play_x and not (sen_x in ob_x):
        return 'Caught!'
    if sen_y == play_y and not (sen_y in ob_y):
        return 'Caught!'
    if sen_x == play_x:
        for pos in ob_x:
            if ob_x[pos] == sen_x:
                if sen_y < play_y and ob_y[pos] > play_y:
                    return 'Caught!'
                if sen_y > play_y and ob_y[pos] < play_y:
                    return 'Caught!'
    if sen_y == play_y:
        for pos in ob_y:
            if ob_y[pos] == sen_y:
                if sen_x < play_x and ob_x[pos] > play_x:
                    return 'Caught!'
                if sen_x > play_x and ob_y[pos] < play_x:
                    return 'Caught!'
            
    return 'Unseen'

def turn():
    # generates outcomes at the end of a turn in the game
    global obpose
    rospy.init_node('Vision')
    pub = rospy.Publisher('Status', String, queue_size=10)
    rate = rospy.Rate(10) 
    # 10hz, rate at which messages are published 
    while obpose < 10:
        obsub = rospy.Subscriber("Obstacle",Int32,getObMsg)
        grid = gen_grid(8)
        playersub = rospy.Subscriber('/player/odom',Odometry,getPlayerMsg)
        spysub = rospy.Subscriber("/spy/odom",Odometry,getSpyMsg)
        obpose = []
        grid = set_grid(grid)
        outcome = detection(grid)
        rospy.loginfo(outcome) 
        pub.publish(outcome)
        rate.sleep()

def callback(data):
    global caught
    caught = data
            
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
    
    pub = rospy.Publisher("Obstacle",List, queue_size=10)
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
        obs_points.append([x,y])
        counter+=1
        pub.publish([x,y])
        
            
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
        caught = ' '
        
        sub = rospy.Subscriber("Status",String,callback)
        

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
        elif caught == "Caught!":
            sys.stdout.write('You have been skadoodled!')
            sys.stdout.write('\n')
            sys.stdout.write('Game Over')
            sys.stdout.write('\n')
            GameOver=True
        else:
            sys.stdout.write('Invalid Input, please try again')
            continue
            
        turn()
        # Outside of the if statements we run the sentry and player at the same time 
        
        # Finally we check to see if player and spy are in the same row, if they are then check if there is an obstacle 
        # between them, if not, the player dies
        
        
        
        
        
        
if __name__ == '__main__':
    main()
    
        
        
        
    
