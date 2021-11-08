# Research Track: Assignment #1
# Python Robotics Simulator
### Professor [Carmine Recchiuto](https://github.com/CarmineD8)

## Running the code <img src="https://user-images.githubusercontent.com/62358773/139832114-25715dd0-508b-4fca-9c20-05c2cc74376f.gif" width="35" height="35"></h2>

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the `test.py` script to test out the simulator as: `python2 run.py file.py` where `file.py` contains the code.

## Goal of the assignment
The goal for this assignment is to make a robot move continuously around a specific arena: the robot cannot touch any wall, represented by golden tokens, while has to grab all the silver tokens met along the path and put them backward. Once it has completed this action it has to move on and continues as before with the remanining tokens.

## Elements in the project
### Arena
The arena has a given shape, with walls represented by golden tokens and the presence of silver tokens, as follows:
![arena](https://user-images.githubusercontent.com/62358773/139511599-a028eff0-8865-4ff4-8896-819c297a69df.jpg)

### Robot
#### Physical structure
The robot is the following:

![robot](https://user-images.githubusercontent.com/62358773/139828348-cc5e2ea0-5f71-447a-ac7f-8b7ef74f3324.png)

It has distance sensors on all sides, so it can detect a wall from -180° to 180°; the reference of 0° is the front direction and the angle increases by moving in clockwise direction taking as reference the 0° position and decreases in the other rotation direction.

#### Internal structure
##### Motors: Robot API
The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```
The functions used to activate the motor are `drive(speed,time)` and `turn(speed,time)`: the first one makes the robot go straight, for a certain time `time` at a certain speed `speed`, while the second makes it turn, always for a certain time `time` and at a certain speed `speed`; as the robot is given a `speed` > 0 it makes it turn clockwise and if `speed` < 0 on the opposite.

#### Grab/Release functions
The robot, as already said, has two arms (grabbers) able to pick up the silver token and to put it backward when the relative token is at a distance of `d_th` metres (this value is not fixed and it is defined as 0.6 in the code). In order to make the robot grab the token it is used the function `R.grab()` which returns a boolean value, `True` or `False` depending on what the robot has done. The piece of code used is:
```python
vTurn = 40
"""int: Velocity module for turning"""

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
```
so if the `R.grab()` is successful the robot will move the token backward, otherwise it means the robot is not close enough so the program will act properly; to release the token it is used the `R.release()` function.

In the short simulation that follows it can be clearly seen all the main function used by the robot such as: `drive(...)`, `turn(...)`, `grab()` and `release()`

![gr_vid](https://user-images.githubusercontent.com/62358773/140282750-61a88b6e-946c-40e6-b2fe-f2737ae24f28.gif)

### Token
Tokens are of two types, as it can be seen in the arena picture.
Each of them is a `Marker` and is characterised by many properties which describe all its characteristics and position in the space.
Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

although, the mainly used in the program are:
* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_SILVER`, `MARKER_TOKEN_GOLD`).
    
![token_silver](https://user-images.githubusercontent.com/62358773/139828770-26c0fea8-876d-490b-9c89-9173f6215e67.png)

![token_gold](https://user-images.githubusercontent.com/62358773/139828777-54f416ae-9134-4a63-ad3a-b95030e8d72c.png)

  * `dist`: an alias for `centre.length`
  * `rot_y`: an alias for `centre.rot_y`

### Code: main

Inside the `main` there is the code to drive the robot around the arena: there are several functions in order to make the code more readable and avoid having a single block of code.
Thanks to a flowchart it can be described the general structure, moreover also the functions will be analised properly:

![main](https://user-images.githubusercontent.com/62358773/139657231-093e1cf8-2bac-422a-8ffe-86e34e876ab3.jpg)

The program starts with `fnc_in()` responsible of initialising the robot movement in the arena.
The second step is the check of the possible presence of a silver token by `dust,rot_y = find_silver_token()` which looks for a silver token in a pre-determined range of view as we can see more detailed later.
Now the program has to take a decision based of the return of the previous function:
* if the token has been detected so `dist ≠ -1`: the program goes on
* otherwise the program returns to the `fnc_in()` and then continues.

In the case the program detects a silver token it has to check also the possible presence of a wall in the direction of the token using the following function `d,r,b = wall_check(rot_y)`.
By using this function the program can make another important decision in order to complete its task:
* if `d < dist` so it measns the wall is nearer than the token the program has to compute the `avoid collision()` function to drive the robot without touching any wall;
* otherwise it means there are no wall between the robot and the token so the robot can go to grab it using the `catch_token()` function.

In both cases program's next step is the return to the `fnc_in()` function and the restart with the decision block.
To implement this there is an infinite loop made by
```python
while 1:
	...
```

Below there is a brief description and the code for every function used.

* `fnc_in()`:
This function makes the robot start the movement, it is structured as follows:
```python
def fnc_in():
	drive(2*vDrive,0.1) # this function allows the robot moving forward
	avoid_collision() # this function allows the robot avoiding the walls while moving
```
Inside its body there are also the function `drive(speed,time)`, already described, and the `avoid collision()` function, responsible of making the robot stay far from the wall. 

* `avoid_collision()`:
```python
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
```
it can be seen that the presence of a wall is checked in front of the robot, on the right and on the left with a pre-determined range, as it can be seen clearly in the following picture:

![robot_collision](https://user-images.githubusercontent.com/62358773/140342829-5c2310ff-1fa6-4e8d-84f9-7764f7b5cac9.jpg)

Then there are several conditions that can make the program decide if the wall is on the right and if it is on the left: using a `while` loop the robot can rotate till the distance from the wall detected is sufficient to make it start again the driving action.

* `d,r,b = wall_check(rot_token)`:
```python
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
```
it allows the robot checking the presence of a wall in a particular direction, determined by the parameter `rot_token`, that is an angle. Inside the `avoid_collision()` the `wall_check(rot_token)` function can detect a wall in front, on the right or on the left with `rot_token` = 0°, 90°, -90° respectively (the figure above explains it clearly).
As it can be seen walls are characterised by a colour (`MARKER_TOKEN_GOLD`) which distinguishes them from tokens (`MARKER_TOKEN_SILVER`).

The main program checks also if the robot is close enough to the token detected and if there are any walls between it and the token. as said at the beginning if no, the program can catch the token, otherwise it has to avoid walls.

* `catch_token()`:
```python
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
```
this function drives the robot to catch the token by making, if necessary, some corrections during the movement. If the robot is close enough to the token it will grab it, otherwise it will have to move closer. Corrections are made depending of the anglo of rotation of the robot with respect to the token and the range of allineation is determined by the variable `a_th`.

The program contains also the `find_silver_token()` defined as:

```python
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
```
It is shown how the robot sees and looks for silver token in the following picture:

![robot_silver](https://user-images.githubusercontent.com/62358773/140338406-7628e8db-2fa5-437b-969b-8dbcea5e6a3a.jpg)

It can be seen that the range to detect silver tokens is 90°, as already seen in the function above.

It is also given a set of global variables, with a relative brief description, in order to have a better adaptation to any corrections:
```python
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
```
### Video demontration
To show what the robot is asked to do it is given a shprt video-demonstration of the robot moving (it is choosen only a piece due to size restrictions in GitHub video):

https://user-images.githubusercontent.com/62358773/140280059-6e1c5774-05ab-4af9-be92-263e73c91a7e.mov

From the simulation it is crearly evident also the `avoid_collision()` function used to drive the robot and keep it far from walls.

### Future improvements
Since the robot has many distance sensors to be used it could be also useful to detect a possible path to be followed: after an accurate scansion of the free "roads" that can be taken the robot can directly go to its destination, the token, without having to bounce from one side to another to find the correct way.
In the project has not been implemented a system of localization for the tokens but with this additive feature it can be also detected if a token is available immediately or not also wothout having a scansion of the entire arena.
