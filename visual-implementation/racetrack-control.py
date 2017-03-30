import pygame
import random
import time
from math import *
from copy import deepcopy

display_width = 800
display_height = 800

world_size = display_width

red = (200, 0, 0)
blue = (0, 0, 255)
green = (0, 155, 0)
yellow = (200, 200, 0)
white = (255, 255, 255)
black = (0, 0, 0)
grey = (67, 70, 75)

car_length = 80.0
car_width = 60.0

wheel_length = 20
wheel_width = 6

max_steering_angle = pi/4

car_img = pygame.image.load("car60_40.png")
track_img= pygame.image.load("../images/racetrack2.png")


origin = (display_width/2, display_height/2)

pygame.init()

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Moving robot")
clock = pygame.time.Clock()

screen.fill(white)

class robot:
	def __init__(self):
		self.x = random.random()*world_size
		self.y = random.random()*world_size
		self.orientation = random.random() * 2.0 * pi
		self.steering_angle = 0.0
		self.steering_drift = 0.0
		self.forward_noise = 0.0
		self.turn_noise	= 0.0
		self.sense_noise = 0.0
	
	def set(self, x, y, orientation, steering_angle):
		if x >= world_size or x < 0:
			raise ValueError, 'X coordinate out of bound'
		if y >= world_size or y < 0:
			raise ValueError, 'Y coordinate out of bound'
		if orientation >= 2*pi or orientation < 0:
			raise ValueError, 'Orientation must be in [0..2pi]'
		if abs(steering_angle) > max_steering_angle:
		    raise ValueError, 'Exceeding max steering angle'

		self.x = x
		self.y = y
		self.orientation = orientation
		self.steering_angle = steering_angle

	def set_steering_drift(self, steering_drift):
		self.steering_drift = steering_drift


	def set_noise(self, f_noise, t_noise, s_noise):
		self.forward_noise = f_noise
		self.turn_noise = t_noise
		self.sense_noise = s_noise


	def move(self, turn, forward):
		theta = self.orientation # initial orientation
		alpha = turn # steering angle
		dist = forward # distance to be moved
		length = car_length # length of the robot
		if abs(alpha) > max_steering_angle:
		    raise ValueError, 'Exceeding max steering angle'

		if dist < 0.0:
		    raise ValueError, 'Moving backwards is not valid' 

		# in local coordinates of robot
		beta = (dist/length)*tan(alpha) # turning angle
		# print degrees(beta)
		_x = _y = _theta = 0.0
		if beta > 0.001 or beta < -0.001:
		    radius = dist/beta # turning radius
		    cx = self.x - sin(theta)*radius # center of the circle
		    cy = self.y - cos(theta)*radius # center of the circle

		    # Uncomment to see the center of the circle the robot is going about
		    # pygame.draw.circle(screen, red, (int(cx), int(cy)), 5)
		    # pygame.display.update()

		    # in global coordinates of robot
		    _x = cx + sin(theta + beta)*radius
		    _y = cy + cos(theta + beta)*radius
		    _theta = (theta + beta)%(2*pi)

		else: # straight motion
		    _x = self.x + dist*cos(theta)
		    _y = self.y - dist*sin(theta)
		    _theta = (theta + beta)%(2*pi)

		self.x = _x
		self.y = _y
		self.orientation = _theta
		self.steering_angle = alpha

		self.x %= world_size
		self.y %= world_size

	def sense(self, landmarks_loc, add_noise=False):
		Z = []
		for i in range(len(landmarks_loc)):
			dist = sqrt((self.x - landmarks_loc[i][0])**2 + ((self.y - landmarks_loc[i][1])**2))
			if add_noise:
				dist += random.gauss(0.0, self.sense_noise)

			Z.append(dist)

		return Z


	def cte(self, radius):
		cte = 0
		x, y, orientation = self.x, self.y, self.orientation
		if x <= 250:
			dx = x - 250
			dy = y - 400
			cte = sqrt(dx**2+dy**2) - 200
		elif 250 < x and x < 550:
			if (0 <= orientation and orientation < pi/2) or (3 * pi / 2 < orientation and orientation < 2 * pi):
				# print y
				cte = -(y - 200)
			else:
			    cte = (y - 600)
		else:
			dx = x - 550
			dy = y - 400
			cte = sqrt(dx**2+dy**2) - 200
		return cte

def pd(robot, diff_CTE):
	# p > d > i
	return 0.01*(robot.y - origin[1]) + 0.05*diff_CTE

def draw_path(path, color):
	pygame.draw.lines(screen, color, False, [(i[1], i[0]) for i in path], 4)
	pygame.draw.line(screen, color, (path[0][1], path[0][0]),(path[len(path) - 1][1], path[len(path) - 1][0]), 4)

def smoother(path, fix, weight_data = 0.2, weight_smooth = 0.2, tolerance = 0.00001):

    change = tolerance
    newpath = deepcopy(path)

    while change >= tolerance:
        change = 0
        for i in range(len(path)):
            for j in range(len(path[0])):
               
                newpath[i][j] += weight_smooth*(newpath[(i-1)%len(path)][j] + newpath[(i+1)%len(path)][j] - 2.0*newpath[i][j]) + \
                (weight_smooth / 2.0)*(2.0*newpath[(i-1)%len(path)][j] - newpath[(i-2)%len(path)][j] - newpath[i][j]) +\
                (weight_smooth / 2.0)*(2.0*newpath[(i+1)%len(path)][j] - newpath[(i+2)%len(path)][j] - newpath[i][j])
    
    return newpath


def draw_rect(center, corners, rotation_angle, color):
	c_x = center[0]
	c_y = center[1]
	delta_angle = rotation_angle
	rotated_corners = []

	for p in corners:
		temp = []
		length = sqrt((p[0] - c_x)**2 + (c_y - p[1])**2)
		angle = atan2(c_y - p[1], p[0] - c_x)
		angle += delta_angle
		temp.append(c_x + length*cos(angle))
		temp.append(c_y - length*sin(angle))
		rotated_corners.append(temp)
	
	# draw rectangular polygon --> car body
	rect = pygame.draw.polygon(screen, color, (rotated_corners[0],rotated_corners[1],rotated_corners[2],rotated_corners[3]))

def draw_track(cx,cy,radius,color):
	# pygame.draw.line(screen, color, (cx-radius, cy-radius), (cx-radius, cy+radius), 200)
	# pygame.draw.line(screen, color, (cx-radius, cy-radius), (3*cx, cy-radius), 200)
	# pygame.draw.line(screen, color, (3*cx, cy-radius), (3*cx, cy+radius), 200)
	# pygame.draw.line(screen, color, (cx-radius, cy+radius), (3*cx, cy+radius), 200)

	pygame.draw.arc(screen, white, (cx-radius,cy-radius,2*radius,2*radius), radians(90), radians(270), 5)
	pygame.draw.line(screen, white, (cx, cy-radius), (cx+300, cy-radius), 5)
	pygame.draw.arc(screen, white, (cx-radius+300,cy-radius,2*radius,2*radius), -pi/2,pi/2, 5)
	pygame.draw.line(screen, white, (cx, cy+radius), (cx+300, cy+radius), 5)



def draw_robot(robot):
	car_x = robot.x 
	car_y = robot.y 
	orientation = robot.orientation
	steering_angle = robot.steering_angle

	p1 = [car_x-car_length/4,car_y-car_width/2]
	p2 = [car_x+(0.75*car_length),car_y-car_width/2]
	p3 = [car_x+(0.75*car_length),car_y+car_width/2]
	p4 = [car_x-car_length/4,car_y+car_width/2]

	# car body
	draw_rect([car_x, car_y], [p1, p2, p3, p4], orientation, yellow)

	# heading direction
	# h = [car_x+car_length/2,car_y]
	# length = car_length/2
	# angle = atan2(car_y - h[1], h[0] - car_x)
	# angle += orientation
	# h[0] = car_x + length*cos(angle)
	# h[1] = car_y - length*sin(angle)

	# wheels
	# rotate center of wheel1
	w1_c_x = car_x
	w1_c_y = car_y - car_width/3
	length = sqrt((w1_c_x - car_x)**2 + (car_y - w1_c_y)**2)
	angle = atan2(car_y - w1_c_y, w1_c_x - car_x)
	angle += orientation
	w1_c_x = car_x + length*cos(angle)
	w1_c_y = car_y - length*sin(angle)

	# draw corners of wheel1
	w1_p1 = [w1_c_x-wheel_length/2, w1_c_y-wheel_width/2]
	w1_p2 = [w1_c_x+wheel_length/2, w1_c_y-wheel_width/2]
	w1_p3 = [w1_c_x+wheel_length/2, w1_c_y+wheel_width/2]
	w1_p4 = [w1_c_x-wheel_length/2, w1_c_y+wheel_width/2]
	draw_rect([w1_c_x, w1_c_y], [w1_p1, w1_p2, w1_p3, w1_p4], orientation, black)





	w2_c_x = car_x + car_length/2
	w2_c_y = car_y - car_width/3
	length = sqrt((w2_c_x - car_x)**2 + (car_y - w2_c_y)**2)
	angle = atan2(car_y - w2_c_y, w2_c_x - car_x)
	angle += orientation
	w2_c_x = car_x + length*cos(angle)
	w2_c_y = car_y - length*sin(angle)

	w2_p1 = [w2_c_x-wheel_length/2, w2_c_y-wheel_width/2]
	w2_p2 = [w2_c_x+wheel_length/2, w2_c_y-wheel_width/2]
	w2_p3 = [w2_c_x+wheel_length/2, w2_c_y+wheel_width/2]
	w2_p4 = [w2_c_x-wheel_length/2, w2_c_y+wheel_width/2]
	draw_rect([w2_c_x, w2_c_y], [w2_p1, w2_p2, w2_p3, w2_p4], steering_angle + orientation, black)
	# rect = pygame.draw.polygon(screen, black, (w2_p1,w2_p2,w2_p3,w2_p4))


	w3_c_x = car_x + car_length/2
	w3_c_y = car_y + car_width/3
	length = sqrt((w3_c_x - car_x)**2 + (car_y - w3_c_y)**2)
	angle = atan2(car_y - w3_c_y, w3_c_x - car_x)
	angle += orientation
	w3_c_x = car_x + length*cos(angle)
	w3_c_y = car_y - length*sin(angle)

	w3_p1 = [w3_c_x-wheel_length/2, w3_c_y-wheel_width/2]
	w3_p2 = [w3_c_x+wheel_length/2, w3_c_y-wheel_width/2]
	w3_p3 = [w3_c_x+wheel_length/2, w3_c_y+wheel_width/2]
	w3_p4 = [w3_c_x-wheel_length/2, w3_c_y+wheel_width/2]
	draw_rect([w3_c_x, w3_c_y], [w3_p1, w3_p2, w3_p3, w3_p4], steering_angle + orientation, black)
	# rect = pygame.draw.polygon(screen, black, (w3_p1,w3_p2,w3_p3,w3_p4))



	w4_c_x = car_x
	w4_c_y = car_y + car_width/3
	length = sqrt((w4_c_x - car_x)**2 + (car_y - w4_c_y)**2)
	angle = atan2(car_y - w4_c_y, w4_c_x - car_x)
	angle += orientation
	w4_c_x = car_x + length*cos(angle)
	w4_c_y = car_y - length*sin(angle)

	w4_p1 = [w4_c_x-wheel_length/2, w4_c_y-wheel_width/2]
	w4_p2 = [w4_c_x+wheel_length/2, w4_c_y-wheel_width/2]
	w4_p3 = [w4_c_x+wheel_length/2, w4_c_y+wheel_width/2]
	w4_p4 = [w4_c_x-wheel_length/2, w4_c_y+wheel_width/2]
	draw_rect([w4_c_x, w4_c_y], [w4_p1, w4_p2, w4_p3, w4_p4], orientation, black)

	# pygame.draw.line(screen, red, (h[0], h[1]),(int(car_x), int(car_y)), 1)

	# draw axle
	pygame.draw.line(screen, black, (w1_c_x, w1_c_y),(w4_c_x, w4_c_y), 1)

	# draw mid of axle
	pygame.draw.circle(screen, red, (int(car_x), int(car_y)), 3)


# col, row
# path  = [[200, 200],[200, 250],[200, 300], [200, 350],[200, 400],[200, 450],[200, 500],[200, 550],[200, 600],\
# [250, 600], [300, 600], [350, 600],[400, 600],[450, 600], [500, 600], [550, 600], [600, 600],[600, 550], [600, 500],[600, 450],[600, 400],\
# [600, 350],[600, 300],[600, 250],[600, 200], [550, 200],[500, 200],[450, 200],[400, 200], [350, 200],[300, 200],[250, 200]]

# fixed_pts = [0 for _ in range(len(path))]
# fixed_pts[0] = 1
# fixed_pts[4] = 1
# fixed_pts[8] = 1
# fixed_pts[12]= 1

robot = robot()
# robot.set_noise(0.1, 0.01, 5.0)

orientation = 90.0
steering_angle = 0.0
#in radians
robot.set(50, 400,radians(orientation), steering_angle)

exit = False

delta_forward = 0.0
delta_steer = 0.0

previous_CTE = robot.cte(200)
CTE = robot.cte(200)
int_crosstrack_error = 0.0
crosstrack_error = robot.cte(200)
while exit == False:

	screen.fill(white)
	screen.blit(track_img, (0, 100))
	# Uncomment following to see the exact racetrack
	#draw_track(250, 400, 200, grey)
	# draw_path(path, red)

	draw_robot(robot)

	# pygame.draw.line(screen, green, (display_width/2, 0), (display_width/2, display_height), 1)
	# pygame.draw.line(screen, black, (0, display_height/2), (display_width, display_height/2), 1)

	pygame.display.update()
	clock.tick(100)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				delta_steer = radians(1)
			elif event.key == pygame.K_RIGHT:
				delta_steer = -radians(1)
			elif event.key == pygame.K_UP:
				delta_forward = 5.0
			elif event.key == pygame.K_DOWN:
				delta_forward = -5.0
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
				delta_steer = 0.0
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				delta_forward = 0.0

	diff_crosstrack_error = -crosstrack_error
	crosstrack_error = robot.cte(200)
	diff_crosstrack_error += crosstrack_error
	int_crosstrack_error += crosstrack_error
	steering_angle = - 0.1 * crosstrack_error \
	        - 0.5 * diff_crosstrack_error
	if steering_angle > max_steering_angle:
		steering_angle = max_steering_angle
	elif steering_angle < -max_steering_angle:
		steering_angle = -max_steering_angle
	print crosstrack_error
	robot.move(steering_angle, 2)
