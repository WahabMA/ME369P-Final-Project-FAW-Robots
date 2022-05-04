import roslib; roslib.load_manifest('gazebo')

import numpy as np

# import sys

import rospy
from gazebo.srv import *

def get_pos(model):
    # gets position of models from gazebo
    rospy.wait_for_service('/gazebo/get_model_state')
    try:
        gms = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        pos = gms(model)
        x = pos.pose.position.x
        y = pos.pose.position.y
        coord = [x,y]
        return coord
    except rospy.ServiceException:
        print("Service call failed")        
        
def gen_grid(size):
    # creates blank grid as a list
    grid = []
    for x in range(size):
        for y in range(size):
            grid[x][y].append(0)
    return grid
    
def set_grid(grid):
    # populates the grid with the model positions. Models need to be defined later
    sen_pos = get_pos(sentry)
    sen_x = np.floor(sen_pos[0])
    sen_y = np.floor(sen_pos[1])
    grid[sen_x][sen_y] = 's'
    
    play_pos = get_pos(player)
    play_x = np.floor(play_pos[0])
    play_y = np.floor(play_pos[1])
    grid[play_x][play_y] = 'p'
    
    # need to figure out way to have a variable number of obstacles
    
    ob_pos = get_pos(obstacle1)
    ob_x = np.floor(ob_pos[0])
    ob_y = np.floor(ob_pos[1])
    grid[ob_x][ob_y] = 'b'
    
    ob_pos = get_pos(obstacle2)
    ob_x = np.floor(ob_pos[0])
    ob_y = np.floor(ob_pos[1])
    grid[ob_x][ob_y] = 'b'
    
    ob_pos = get_pos(obstacle3)
    ob_x = np.floor(ob_pos[0])
    ob_y = np.floor(ob_pos[1])
    grid[ob_x][ob_y] = 'b'
    
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

if __name__ == '__main__':
    grid = gen_grid(8)
    grid = set_grid(grid)
    outcome = detection(grid)
    if outcome in 'Caught!':
        print('You have been caught!')
