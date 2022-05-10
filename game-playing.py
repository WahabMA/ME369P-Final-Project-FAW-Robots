#!/usr/bin/env python

import random
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from std_msgs.msg import String
from math import atan2
import numpy as np
import roslaunch 
import sys

# models in Gazebo give information as an Odometry object, used for position and orientation data
spypose = Odometry()
playerpose = Odometry()
obs_points=[]
caught = 'dummy'

def getSpyMsg(msg):
    # call back function for spy subscriber
    global spypose
    spypose = msg
    
def getPlayerMsg(msg):
    # callback function for player subscriber
    global playerpose
    playerpose = msg
    
def getMsgInfo(msg):
    # extract position and rotation information from message
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    
    rot_q = msg.pose.pose.orientation
    roll,pitch,theta = euler_from_quaternion([rot_q.x,rot_q.y,rot_q.z,rot_q.w])
    return x,y,theta
        
def setSpyTwist(pub,goal):
    # calculates and publishes spy velocity as twist so it reaches its goal
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
        
def setPlayerTwist(pub,goal):
    # calculates and and publishes player velocity as twist  so it reaches its goal
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

def gen_grid(size):
    # generates a size x size grid of zeros for game logic as a numpy array
    grid = np.zeros((size+1,size))
    return grid
    
def set_grid(grid):
    # populates the grid with model positions for game logic
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
    sen_x,sen_y,temp = getMsgInfo(spypose)
    sen_x = int(np.floor(sen_x))
    sen_y = int(np.floor(sen_y))
    grid[sen_x][sen_y] = '1'

    # player model - second object in sumulation
#    play_pos = get_pos(models(0),links(0)(0))
    play_x, play_y,temp = getMsgInfo(playerpose)
    play_x = int(np.floor(play_x))
    play_y = int(np.floor(play_y))
    grid[play_x][play_y] = '2'

    ob_x = []
    ob_y = []

    for i in range(len(obs_points)):
        ob_x.append(obs_points[i][0])
        ob_y.append(obs_points[i][1])

    for i in range(len(ob_x)):
        ob_x[i] = int(np.floor(ob_x[i]))
        ob_y[i] = int(np.floor(ob_y[i]))
        grid[ob_x[i]][ob_y[i]] = '3'
    
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
    # returns if player is detected or not by the sentry, run once per turn
    ob_x = []
    ob_y = []
    sen_x = -1
    sen_y = -1
    play_x = -2
    play_y = -2
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 1:
                sen_x = x
                sen_y = y
            if grid[x][y] == 2:
                play_x = x
                play_y = y
            if grid[x][y] == 3:
                ob_x.append(x)
                ob_y.append(y)
    # if sen_x == play_x and not (sen_x in ob_x):
    #     return 'Caught!'
    if sen_y == play_y and not (sen_y in ob_y):
        return 'Caught!'
    # if sen_x == play_x:
    #     for pos in range(len(ob_x)):
    #         if ob_x[pos] == sen_x:
    #             if sen_y < play_y and ob_y[pos] > play_y:
    #                 return 'Caught!'
    #             if sen_y > play_y and ob_y[pos] < play_y:
    #                 return 'Caught!'
    if sen_y == play_y:
        for pos in range(len(ob_y)):
            if ob_y[pos] == sen_y:
                if sen_x > play_x and ob_x[pos] < play_x:
                    return 'Caught!'
            
    return 'Unseen'

def turn():
    # generates outcomes at the end of a turn in the game. Publishes outcome of turn
    # rospy.init_node('Vision')
    pub = rospy.Publisher('/Status', String, queue_size=10,latch=True)
    rate = rospy.Rate(10) 
    # 10hz, rate at which messages are published 
    grid = gen_grid(8)
    playersub = rospy.Subscriber('/player/odom',Odometry,getPlayerMsg)
    spysub = rospy.Subscriber("/spy/odom",Odometry,getSpyMsg)
    
    grid = set_grid(grid)
    outcome = detection(grid)
    # rospy.loginfo(outcome)
    pub.publish(outcome)
    rate.sleep()

def callback(data):
    # callback function for status subscriber
    global caught
    caught = data.data
            
def main():
    
    # main function that runs all game logic
    
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

    global obs_points
    a=[1,2,3,4,5,6,7]   # x-values
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
        obs_points.append([x,y])
        counter+=1
        
    # launches world in Gazebo   
    roslaunch_args1=cli_args1[2:]
    roslaunch_file1=roslaunch.rlutil.resolve_launch_arguments(cli_args1)[0]
    launch_files.append((roslaunch_file1,roslaunch_args1))
    
    parent = roslaunch.parent.ROSLaunchParent(uuid,launch_files)
    parent.start()
    
      

    
    usin = 'waiting'
    
    # rospy stuff
    rospy.init_node('game')
    spysub = rospy.Subscriber("/spy/odom",Odometry,getSpyMsg)
    spypub = rospy.Publisher('/spy/cmd_vel',Twist,queue_size=1)
    playersub = rospy.Subscriber('/player/odom',Odometry,getPlayerMsg)
    playerpub = rospy.Publisher('/player/cmd_vel',Twist,queue_size=1)
    
    spyvel = Twist()
    playervel = Twist()
    playerpose.pose.pose.position.x = 0.5
    playerpose.pose.pose.position.y = playery
    spypose.pose.pose.position.x = 8.5
    spypose.pose.pose.position.y = sentryy
    
    sys.stdout.write("Welcome to the game!")
    sys.stdout.write('\n')
    sys.stdout.write('Avoid being seen by the sentry! (obstacles help with hiding)')
    sys.stdout.write('\n')
    sys.stdout.write('Good luck')
    sys.stdout.write('\n')
    
    # while loop for turn to turn gameplay. Takes player input and calculates full turn. Ends once player has been caught
    while not GameOver:
        playerx,playery,playertheta = getMsgInfo(playerpose)
        playerx = round(playerx*2)/2
        playery = round(playery*2)/2
        
        sys.stdout.write('Use WASD to move (q to QUIT)')
        sys.stdout.write('\n')
        sys.stdout.write('Insert Your Next Action: ')
        usin= str(input())
        sys.stdout.write('\n')
        
        if usin.lower() =='w':
            playerx += 1
            if [playerx-0.5,playery-0.5] in obs_points:
                print('Obstacle ahead! Watch out!')
                continue
            playergoal = Point(playerx,playery,0)
        elif usin.lower()=='s':
            playerx -= 1
            if [playerx-0.5,playery-0.5] in obs_points or playerx+0.5 <= 0:
                print('Obstacle or boundary ahead! Watch out!')
                continue
            playergoal = Point(playerx,playery,0)
        elif usin.lower()=='a':
            playery += 1
            if [playerx-0.5,playery-0.5] in obs_points or playery+0.5 > 8:
                print('Obstacle or boundary ahead! Watch out!')
                continue
            playergoal = Point(playerx,playery,0)
        elif usin.lower()=='d':
            playery -= 1
            if [playerx-0.5,playery-0.5] in obs_points or playery+0.5 <= 0:
                print('Obstacle or boundary ahead! Watch out!')
                continue
            playergoal = Point(playerx,playery,0)
        elif usin.lower()=='q':
            GameOver=True
            continue
        else:
            print('Invalid Input, please try again')
            continue
        
        
        # move player
        print('Player moving to (',playery+0.5,',',playerx+0.5,')')
        setPlayerTwist(playerpub,playergoal)

        # move sentry
        spypossiblepos = [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5]
        spygoal = Point(8.5,random.choice(spypossiblepos),0)
        print('Sentry moving to (',spygoal.y+0.5,', 9.0 )')
        setSpyTwist(spypub,spygoal)
        
        # end turn
        turn()
        sub = rospy.Subscriber("/Status",String,callback)
        
        
        if round(playerx*2)/2+0.5 == 9:
            print('You have skadoodled!')
            print('You win! Yay!')
            GameOver=True
            continue
        elif caught in "Caught!":
            sys.stdout.write('You have been skadoodled!')
            sys.stdout.write('\n')
            sys.stdout.write('Game Over')
            sys.stdout.write('\n')
            GameOver=True
            continue
        
        
        
        
        
        
        
if __name__ == '__main__':
    main()
    
        
        
        
    
