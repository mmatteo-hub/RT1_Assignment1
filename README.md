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
#### Grab
The robot, as already said, has two arms (grabbers) able to pick up the silver token and to put it backward when the relative token is at a distance of 0.4 metres (this value is not fixed but it is a good measure for the robot dimensions). In order to make the robot grab the token we use the function `R.grab()` which returns a boolean value depending on what the robot has done. The piece of code we use is:
```python
if R.grab()
    ...
else
    ...
```
so if the `R.grab()` is successful the robot will move the token backward, otherwise it means the robot is not close enough so the program will act properly.
