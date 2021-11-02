# Assignment 1

## Running the code
<img src="https://user-images.githubusercontent.com/62358773/139832114-25715dd0-508b-4fca-9c20-05c2cc74376f.gif" width="75"></h2>
The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the `test.py` script to test out the simulator as: `python2 run.py file.py` where `file.py` contains the code.

## Goal of the assignment
The goal for this assignment is to make a robot move continuously around a specific arena: the robot cannot touch any wall, representeed by the golden tokens, while has to grab all the silver tokens met along the path and put them backward. Once it has completed this action it has to move on and continues as before.

## Elements in the project
### Arena
The arena has a shape gien, with the wall represented by the golden tokens in which there are the silver tokens, as follows:
![arena](https://user-images.githubusercontent.com/62358773/139511599-a028eff0-8865-4ff4-8896-819c297a69df.jpg)

### Robot
#### Physical structure
The robot is the following:

![robot](https://user-images.githubusercontent.com/62358773/139828348-cc5e2ea0-5f71-447a-ac7f-8b7ef74f3324.png)

It has distance sensors on all sides, so it can detect a wall from -180° to 180°; the reference of 0° is the front direction, the angle increase by moving in clockwise direction taking as reference the 0° position and decrease in the other rotation direction.

#### Internal structure
##### Motors: Robot API
The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```
THe function used to activate the motor are `drive(speed,time)` and `turn(speed,time)`which makes the robot go straight, for a certain time `time` at a certain speed `speed`, and turn, always for a certain time `time` and at a certain speed `speed`; as the robot is made a `speed` > 0 makes the robot turn clockwise and if `speed` < 0 on the opposite.

#### Grab/Release functions
The robot, as already said, has two arms (grabbers) able to pick up the silver token and to put it backward when the relative token is at a distance of 0.4 metres (this value is not fixed but it is a good measure for the robot dimensions). In order to make the robot grab the token we use the function `R.grab()` which returns a boolean value depending on what the robot has done. The piece of code we use is:
```python
vTurn = 20
"""int: Velocity module for turn"""

if R.grab(): 
    print("Gotcha!")
    turn(vTurn, 3)
    R.release()
    print("Released")
    turn(-vTurn,3)
    print("Move on!!!")
else:
    print("Aww, I'm not close enough.")
```
so if the `R.grab()` is successful the robot will move the token backward, otherwise it means the robot is not close enough so the program will act properly; to release the token it is used the `R.release()` function.

### Token
Tokens are of two types, as it can be seen in the arean picture.
Each of them is a `Marker` and is characterised by many properties which describe all its characteristic and. position in the space. The mainly used in the program are:
* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_SILVER`, `MARKER_TOKEN_GOLD`).
  
![token_silver](https://user-images.githubusercontent.com/62358773/139828770-26c0fea8-876d-490b-9c89-9173f6215e67.png)

![token_gold](https://user-images.githubusercontent.com/62358773/139828777-54f416ae-9134-4a63-ad3a-b95030e8d72c.png)

  * `dist`: an alias for `centre.length`
  * `rot_y`: an alias for `centre.rot_y`

### Code: main

Inside the main there is the code to drive the robot around the arena, there are several functions in order to make the code more readable and avoid a single block of code.
Thanks to a flowchart it can be described the general structure, moreover also the functions will be analised properly:

![main](https://user-images.githubusercontent.com/62358773/139657231-093e1cf8-2bac-422a-8ffe-86e34e876ab3.jpg)

* `fnc_in()`:
The first function is the `fnc_in()` which makes the robot starting the movement, it is structured as follows:
```python
def fnc_in():
	drive(2*vDrive,0.2)
	avoid_collision()
```
there is the function `drive(speed,time)`, already described, and the `avoid collision()`, responsible of making the robot stay far from the wall. 

* `avoid_collision()`:
```python
def avoid_collision():
	dist,rot,boolean = wall_check(0) # Robot watches in front of it to detect the wall distance, rotation and if it is present
	dist_r,rot_r,boolean_r = wall_check(90) # Robot watches on its right to detect a wall
	dist_l,rot_l,boolean_l = wall_check(-90) # Robot watches on its left to detect a wall
	if dist_r == -1 or dist_l == -1:
		print("No walls...")
	if dist_r > dist_l:
		print("Wall on my left ... turn right!")
		while(dist < free_th): # Turn until it is free to move; re-calculates the distance from the wall
			turn(vTurn, 0.2)
			dist,rot,boolean = wall_check(0)
		print("OK, now it's ok.")
	else:
		print("Wall on my right ... turn left!")
		while(dist < free_th):
			turn(-vTurn, 0.2) # Turn until it is free to move; re-calculates the distance from the wall
			dist,rot,boolean = wall_check(0)
		print("OK, now it's ok.")	
```
it can be seen that the presence of a wall is checked in front of the robot, on the right and on the left; then there are several conditions that can make the program decide if the wall is on the right and if it is on the left: using a `while` loop the robot can rotate till the distance from the wall detected is sufficient to make it start again the driving action.

* `d,r,b = wall_check(rot_token)`:
```python
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
```
it allows the robot checking the presence of a wall in a particular direction, determined by the parameter `rot_token`, that is an angle. Inside the `avoid_collision()` the `wall_check(rot_token)` can detect a wall in front, on the right or on the left with `rot_token`=0, 90, -90 respectively.
As it can be seen the wall are characterised by a colour (`MARKER_TOKEN_GOLD`) which distinguishes them from the token (`MARKER_TOKEN_SILVER`).

the main program now checks if the robot is close enough to the token detected: the function returns `d` which is the wall distance and if `d`< `dist`it means there is a wall so the program starts again the `avoid_collision()`, otherwise there are no dangerous wall so the robot can catch the token

* `catch_token()`:
```python
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
```
this function drives the robot to catch the token  by making some corrections during the movement.

The program contains also the `find_silver_token()` defined as:

```python
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
```
and a set of global variables, in order to have a better adaptation to any corrections:
```python
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
```
