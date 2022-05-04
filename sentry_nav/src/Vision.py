#!/usr/bin/env python3

import roslib; roslib.load_manifest('gazebo')

import numpy as np

# import sys

import rospy
from std_msgs.msg import String
from gazebo.srv import *

def get_pos(model_name, relative_entity_name):
    # gets position of models from gazebo
    rospy.wait_for_service('/gazebo/get_model_state')
    try:
        gms = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        pos = gms(model_name, relative_entity_name)
        x = pos.pose.position.x
        y = pos.pose.position.y
        coord = [x,y]
        return coord
    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed: {0}".format(e))        
        
def gen_grid(size):
    # creates blank grid as a list
    grid = []
    for x in range(size):
        for y in range(size):
            grid[x][y].append(0)
    return grid
    
def set_grid(grid):
    # get model names from gazebo
    rospy.wait_for_service('/gazebo/get_world_properties')
    try:
        gwp = rospy.ServiceProxy('/gazebo/get_world_properties')
        prop = gwp()
        models = prop.model_names
        # get relative link in each model
        links = []
        for i in models:
            rospy.wait_for_service('/gazebo/get_model_properties')
            try:
                 gmp = rospy.ServiceProxy('gazebo/get_model_properties')
                 m_prop = gmp(models(i))
                 links.append(m_prop.body_names)
            except rospy.ServiceException as e:
                rospy.loginfo("Service call failed: {0}".format(e))

    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed: {0}".format(e))

    # populates the grid with the model positions. Models need to be defined later

    # sentry model - first object in simulation
    sen_pos = get_pos(models(2),links(2)(0))
    sen_x = np.floor(sen_pos[0])
    sen_y = np.floor(sen_pos[1])
    grid[sen_x][sen_y] = 's'

    # player model - second object in sumulation
    play_pos = get_pos(models(0),links(0)(0))
    play_x = np.floor(play_pos[0])
    play_y = np.floor(play_pos[1])
    grid[play_x][play_y] = 'p'
    
    # variable numbers of obstacles. Any models in the simulation after the first two
    for ob in range(3,len(models))
        ob_pos = get_pos(models(ob),links(ob)(0))
        ob_x = np.floor(ob_pos[0])
        ob_y = np.floor(ob_pos[1])
        grid[ob_x][ob_y] = 'b'

        ob_fpos = [ob_x,ob_y]

        pub = rospy.Publisher('Obstacles', int32[] , queue_size=10)

        pub.publish(ob_fpos)
    
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
    rospy.init_node('Vision')

    grid = gen_grid(8)
    grid = set_grid(grid)
    outcome = detection(grid)

    pub = rospy.Publisher('Status', String, queue_size=10)

    pub.publish(outcome)

if __name__ == '__main__':
    turn()