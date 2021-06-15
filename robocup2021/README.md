# robocup2021

Robocup_development project

## Instalation

First install necessary turtlebot2 packages. (Follow the instructions in the videos)

https://youtu.be/rniyH8dY5t4

Next clone the repository of gazebo models (you can also download other models but be sure to mention where you got it from)

```bash
git clone https://github.com/osrf/gazebo_models.git
```
then copy the models into ur gazebo model path

then go to workspace source folder

clone this repository

```bash
cd ..
catkin_make
```

## Usage

The robot simulator package is a demo package with all the necessary configurations to launch an env and robot.

To launch the follow_meworld in gazebo
```bash
roslaunch robot_simulator world.launch
```

To launch the robot in the world in gazebo
```bash
roslaunch robot_simulator gazebo.launch
```

To launch the robot in world and rviz
```bash
roslaunch robot_simulator simulate.launch
```

Once you have created your world, perform mapping to generate map of the world.

1st launch the world

```bash
roslaunch robot_simulator simulate.launch
```
on another terminal 

```bash
roslaunch robot_simulator gmapping.launch
```
on another terminal 

```bash
roslaunch turtlebot_teleop keyboard_teleop.launch 
```
make sure to reduce the robot speed as slower mapping have higher accuracy...

then you can control the robot in the world to generate map.

https://www.youtube.com/watch?v=yv0FhmqPfUo

