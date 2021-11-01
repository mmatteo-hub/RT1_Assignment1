# Assignment 1
## Running the code
The simulator requires a Python 2.7 installation in order to run the `run.py` file; the file containing the code for the robot behaviour is `assignment.py`.

## Goal of the assignment
The goal for this assignment is to make a robot move continuously around a specific arena: the robot cannot touch any wall, representeed by the golden tokens, while has to grab all the silver tokens met along the path and put them backward. Once it has completed this action it has to move on and continues as before.

## Elements in the project
### Arena
The arena has a shape gien, with the wall represented by the golden tokens in which there are the silver tokens, as follows:
![arena](https://user-images.githubusercontent.com/62358773/139511599-a028eff0-8865-4ff4-8896-819c297a69df.jpg)

### Robot
#### Physical structure
The robot is the following:

![robot](https://user-images.githubusercontent.com/62358773/139511645-fd261847-0718-4f19-81db-dba9c4161575.jpg)

It has distance sensors on all sides, so it can detect a wall from -180° to 180°; the reference of 0° is the front direction, the angle increase by moving in clockwise direction taking as reference the 0° position and decrease in the other rotation direction.

![robot_angles](https://user-images.githubusercontent.com/62358773/139511937-7311faf7-3df1-49b8-9a40-84ec452cc0fa.jpg)

#### Internal structure
##### Motors
The simulated robot is provided of two motors which are responsible of the robot movement: for example to turn on the spot of half, so to put on the reverse the code will be:
```python
R.motors[0].m0.power = 50
R.motors[0].m0.power = -50
```
THe function used to activate the motor are `drive(speed,time)` and `turn(speed,time)`which makes the robot go straight, for a certain time `time` at a certain speed `speed`, and turn, always for a certain time `time` and at a certain speed `speed`; as the robot is made a `speed` > 0 makes the robot turn clockwise and if `speed` < 0 on the opposite.

### Token
Tokens are of two types, as it can be seen in the arean picture.
Each of them is a `Marker` and is characterised by many properties which describe all its characteristic and. position in the space. The mainly used in the program are:
* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER`).
  * `dist`: an alias for `centre.length`
  * `rot_y`: an alias for `centre.rot_y`

## Functions used
#### Grab
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
so if the `R.grab()` is successful the robot will move the token backward, otherwise it means the robot is not close enough so the program will act properly; ot release the token it is used the `R.release()` function.

### Code: main
Inside the main there is the code to drive the robot around the arena, there are several functions in order to make the code more readable and avoid a single block of code.
Thanks to a flowchart it can be described the general structure, moreover also the functions will be analised properly:

![main](https://user-images.githubusercontent.com/62358773/139657231-093e1cf8-2bac-422a-8ffe-86e34e876ab3.jpg)

The first function is the `fnc_in()` which makes the robot starting the movement, it is structured as follows:
```python
def fnc_in():
	drive(2*vDrive,0.2)
	avoid_collision()
```
there is the function `drive(speed,time)`, already described, and the `avoid collision()`, responsible of making the robot stay far from the wall. This function is:
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
The function `wall_check(rot_token)` seen is:
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
