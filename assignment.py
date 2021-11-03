from __future__ import print_function

import time
from sr.robot import *

# Global variables defined to have a more readable code and a more velocity to correct parameters during testing
a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.6
""" float: Threshold for the control of the orientation"""

free_th = 0.85
"""float: Distance to detect if the robot is free to drive or not"""

R = Robot()
""" instance of the class Robot"""

view_range = 35
"""int: Range of view for the Robot"""

see_angle = 45
"""int: Angle of vision for the robot to detect the silver token"""

vTurn = 40
"""int: Velocity module for turning"""

vTurn_dir = 9.5
"""int: Velocity module for turning while nearby a wall"""

vDrive = 40
"""int: Velocity module for driving"""

# Function to make the robot drive: a positive 'speed' value makes the robot move forward, a negative 'speed' value makes the robot move backward; the time is the interval the movement lasts
def drive(speed, seconds):
	R.motors[0].m0.power = speed
    	R.motors[0].m1.power = speed
    	time.sleep(seconds)
    	R.motors[0].m0.power = 0
    	R.motors[0].m1.power = 0

# Function to make the robot turn: a positive 'speed' value makes the robot turn right, a negative 'speed' value makes the robot turn left; the time is the interval the movement lasts
def turn(speed, seconds):
	R.motors[0].m0.power = speed
    	R.motors[0].m1.power = -speed
    	time.sleep(seconds)
    	R.motors[0].m0.power = 0
    	R.motors[0].m1.power = 0

# Function to make the robot detect the presence of a silver token in the arena
def find_silver_token():
	dist=100
    	for token in R.see():
        	if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -see_angle <= token.rot_y <= see_angle:
        	# the token rotation is determined only in a range of view, determined by the global variable 'see_angle'
            		dist=token.dist
	    		rot_y=token.rot_y
    	if dist==100: # it means no token has been detected
		return -1, -1 # int this case, the function returns are negative distance, negative angle
    	else: # it means a token has been detected
   		return dist, rot_y # in this case, the function return are the distance, the rotation of the token

# Function to make the robot check the presence of a wall
def wall_check(rot_token):
	dist=100
    	for token in R.see():
        	if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and (rot_token - view_range) <= token.rot_y <= (rot_token + view_range):
        	# in the if statement there are conditions in and because all of them have to be satisfied to detect a wall corectly.
        	# In particular the robot has a range of view, determined by the global varable 'view_range' and can detect walls only in the direction passed as parameter to the function
            		dist=token.dist
	    		rot_y=token.rot_y
    	if dist==100: # it means no wall has been detected
		return -1, -1, False # int this case, the function returns are negative distance, negative angle and a False boolean
    	else: # it means a wall has been detected
   		return dist, rot_y, True # in this case, the function return are the distance, the rotation of the wall and a True boolean
	
# Function to make the robot drive around the arena avoiding wall collisions and turning properly when necessary
def avoid_collision():
	dist,rot,boolean = wall_check(0) # Robot watches in front of it to detect the wall distance, rotation and if it is present
	dist_r,rot_r,boolean_r = wall_check(90) # Robot watches on its right to detect a wall
	dist_l,rot_l,boolean_l = wall_check(-90) # Robot watches on its left to detect a wall
	if dist_r == -1 or dist_l == -1: # Conditions of not wall detected
		print("No walls...")
	if dist_r > dist_l: # Check if the left wall is nearer than the right one
		print("Wall on my left ... turn right!")
		while(free_th > dist): # Turns until it is free to move: the distance is defined by the global variable 'free_th'
			turn(vTurn, 0.25) # turns right (vTurn > 0) to avoid the wall on the left
			dist,rot,boolean = wall_check(0) # Re-calculate the distance after every turn to check the while condition
		print("OK, now it's ok.")
	else:
		print("Wall on my right ... turn left!")
		while(free_th > dist): # Turns until it is free to move: the distance is defined by the global variable 'free_th'
			turn(-vTurn, 0.25) # turn left (vTurn < 0) to avoid the wall on the right
			dist,rot,boolean = wall_check(0) # Re-calculate the distance after every turn to check the while condition
		print("OK, now it's ok.")	
	
# Function to make the robot grab the silver token detected
def catch_token(dist,rot_y):
	if dist <= d_th: # it means that the token is as near as necessary to be grabbed
      		print("Found it!")
      		if R.grab(): # returns a True boolean if the robot has been able to grab the token
      			print("Gotcha!")
    			turn(vTurn, 1.5) # turns right (clockwise) to put the token backward, in respect to its current direction
	    		R.release() # releases the token
	    		print("Released")
	    		drive(-vDrive/2,0.8) # drive backward to take space for the next action
	    		turn(-vTurn,1.5) # turns again, this time on the left (anticlockwise) to re-take the direction and proceed in the arena
	    		print("Move on!!!")
		else:# the R.grab() returns a False boolean so the token cannot be grabbed and the robot has to move nearer to it
            		print("Aww, I'm not close enough.")
	elif -a_th <= rot_y <= a_th: # checks if the token rotation is inside a certain angle range, defined by the gloab varible 'a_th'
		drive(vDrive, 0.5) # If this condition is satisfied the robot move forward to the token
	elif rot_y < -a_th: # checks is the token is more on the left in respect to the direction of the robot, which is the 0 degree
		print("Left a bit...")
		turn(-vTurn_dir, 0.2) # if the condition is satified the robot turns on the left
	elif rot_y > a_th: # checks is the token is more on the right in respect to the direction of the robot, which is the 0 degree
		print("Right a bit...")
		turn(+vTurn_dir, 0.2) # if the condition is satified the robot turns on the right

# Function defined only to minimise the main code: it contains two other functions that initialises the robot movement
def fnc_in():
	drive(2*vDrive,0.1) # this function allows the robot moving forward
	avoid_collision() # this function allows the robot avoiding the walls while moving
	
# main function of the code
def main():
	while 1: # 'while 1' allows the program running until it is stopped
		fnc_in() # starts the movement
		dist,rot_y = find_silver_token() # checks the presence of a silver token in the arena
		if dist != -1: # token detected
			print("Token seen!")
			d,r,b = wall_check(rot_y) # checks the presence of a wall the direction of the token
			if d < dist: # the wall detected is nearer than the token
				print("There is a wall. I've to avoid it.")
				avoid_collision() # calls the function to make the robot drive avoiding walls
			else: # there are no walls between the robot and the token
				print("No wall! Let's get it!")
				catch_token(dist,rot_y) # the robot can go to catch the token

# the main function is called here
main()


