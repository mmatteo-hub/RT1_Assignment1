from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

free_th = 0.85
"""float: Distance to detect if the robot is free to drive or not"""

R = Robot()
""" instance of the class Robot"""

view_range = 35
"""int: Range of view for the Robot"""

see_angle = 45
"""int: Angle of vision for the robot to detect the silver token"""

vTurn = 20
"""int: Velocity module for turning"""

vTurn_dir = 4
"""int: Velocity module for turning while nearby a wall"""

vDrive = 20
"""int: Velocity module for driving"""

def drive(speed, seconds):
	R.motors[0].m0.power = speed
    	R.motors[0].m1.power = speed
    	time.sleep(seconds)
    	R.motors[0].m0.power = 0
    	R.motors[0].m1.power = 0

def turn(speed, seconds):
	R.motors[0].m0.power = speed
    	R.motors[0].m1.power = -speed
    	time.sleep(seconds)
    	R.motors[0].m0.power = 0
    	R.motors[0].m1.power = 0

def find_silver_token():
	dist=100
    	for token in R.see():
        	if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -see_angle <= token.rot_y <= see_angle:
            		dist=token.dist
	    		rot_y=token.rot_y
    	if dist==100:
		return -1, -1
    	else:
   		return dist, rot_y

def wall_check(rot_token):
	dist=100
    	for token in R.see():
        	if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and (rot_token - view_range) <= token.rot_y <= (rot_token + view_range):
            		dist=token.dist
	    		rot_y=token.rot_y
    	if dist==100:
		return -1, -1, False
    	else:
   		return dist, rot_y, True
	
def avoid_collision():
	dist,rot,boolean = wall_check(0) # Robot watches in front of it to detect the wall distance, rotation and if it is present
	dist_r,rot_r,boolean_r = wall_check(90) # Robot watches on its right to detect a wall
	dist_l,rot_l,boolean_l = wall_check(-90) # Robot watches on its left to detect a wall
	if dist_r == -1 or dist_l == -1:
		print("No walls...")
	if dist_r > dist_l:
		print("Wall on my left ... turn right!")
		while(free_th > dist): # Turn until it is free to move; re-calculates the distance from the wall
			turn(vTurn, 0.2)
			dist,rot,boolean = wall_check(0)
		print("OK, now it's ok.")
	else:
		print("Wall on my right ... turn left!")
		while(free_th > dist):
			turn(-vTurn, 0.2) # Turn until it is free to move; re-calculates the distance from the wall
			dist,rot,boolean = wall_check(0)
		print("OK, now it's ok.")	
	
def catch_token(dist,rot_y):
	if dist <= d_th:
      		print("Found it!")
      		if R.grab(): 
      			print("Gotcha!")
    			turn(vTurn, 3)
	    		R.release()
	    		print("Released")
	    		turn(-vTurn,3)
	    		print("Move on!!!")
		else:
            		print("Aww, I'm not close enough.")
	elif -a_th <= rot_y <= a_th:
		drive(vDrive, 0.5)
	elif rot_y < -a_th: 
		print("Left a bit...")
		turn(-vTurn_dir, 0.25)
	elif rot_y > a_th:
		print("Right a bit...")
		turn(+vTurn_dir, 0.25)
	
def fnc_in():
	drive(2*vDrive,0.1)
	avoid_collision()
	drive(vDrive,0.1)
	
def main():
	while 1:
		fnc_in()
		dist,rot_y = find_silver_token()
		if dist != -1: # token detected
			print("Token seen!")
			d,r,b = wall_check(rot_y) # Checks the presence of a wall in front of the robot
			if d < dist: # I see a wall
				print("There is a wall. I've to avoid it.")
				avoid_collision()
			else:
				print("No wall! Let's get it!")
				catch_token(dist,rot_y)

main()


