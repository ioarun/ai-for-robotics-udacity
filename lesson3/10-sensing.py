
# Write a function in the class robot called sense()
# that takes self as input
# and returns a list, Z, of the four bearings to the 4
# different landmarks. you will have to use the robot's
# x and y position, as well as its orientation, to
# compute this.

from math import *
import random

# --------
# 
# the "world" has 4 landmarks.
# the robot's initial coordinates are somewhere in the square
# represented by the landmarks.
#
# NOTE: Landmark coordinates are given in (y, x) form and NOT
# in the traditional (x, y) format!

landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]] # position of 4 landmarks in (y, x) form.
world_size = 100.0 # world is NOT cyclic. Robot is allowed to travel "out of bounds"

# ------------------------------------------------
# 
# this is the robot class
#

class robot:

    # --------
    # init: 
    #	creates robot and initializes location/orientation
    #

    def __init__(self, length = 10.0):
        self.x = random.random() * world_size # initial x position
        self.y = random.random() * world_size # initial y position
        self.orientation = random.random() * 2.0 * pi # initial orientation
        self.length = length # length of robot
        self.bearing_noise  = 0.0 # initialize bearing noise to zero
        self.steering_noise = 0.0 # initialize steering noise to zero
        self.distance_noise = 0.0 # initialize distance noise to zero



    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), 
                                                str(self.orientation))


    # --------
    # set: 
    #	sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    # --------
    # set_noise: 
    #	sets the noise parameters
    #

    def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.bearing_noise  = float(new_b_noise)
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    # --------
    # sense:
    #   obtains bearings from positions
    #
    
    def sense(self, add_noise=1):
        Z = []
       	for i in range(len(landmarks)):
       		bearing_angle = atan2(landmarks[i][0] - self.y, landmarks[i][1] - self.x) - self.orientation
       		
       		if add_noise:
       			bearing_angle += random.gauss(0.0, self.bearing_noise)

       		# avoid angles greater than 2pi
       		bearing_angle %= 2*pi
       		Z.append(bearing_angle)
       		
        return Z # Return vector Z of 4 bearings.
    
    
## --------
## TEST CASES:



##
## 1) The following code should print the list [6.004885648174475, 3.7295952571373605, 1.9295669970654687, 0.8519663271732721]
##
##
# length = 20.
# bearing_noise  = 0.0
# steering_noise = 0.0
# distance_noise = 0.0

# myrobot = robot(length)
# myrobot.set(30.0, 20.0, 0.0)
# myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

# print 'Robot:        ', myrobot
# print 'Measurements: ', myrobot.sense()

    

##
## 2) The following code should print the list [5.376567117456516, 3.101276726419402, 1.3012484663475101, 0.22364779645531352]
##
##
##length = 20.
##bearing_noise  = 0.0
##steering_noise = 0.0
##distance_noise = 0.0
##
##myrobot = robot(length)
##myrobot.set(30.0, 20.0, pi / 5.0)
##myrobot.set_noise(bearing_noise, steering_noise, distance_noise)
##
##print 'Robot:        ', myrobot
##print 'Measurements: ', myrobot.sense()
##