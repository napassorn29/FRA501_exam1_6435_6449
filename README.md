# FRA501_exam1_6435_6449
 This package is associated to FRA501 : Robotics DevOps class in FIBO, KMUTT for the reason to study about developing system by using ROS2. The relevant topics are include:
- Publisher/Subscriber
- Service/Client
- Custom interface
- Parameter in a class
- Launch file
- How to pass arguments to python node

# proposition
This package contains launch file which spawn 4 turtles from turtlesim_plus package. Each of them will droping 20 pizzas to form a shape of alphabets "F", "I", "B" and "O".

# Installation
1.) Clone the repo to the src directory of your workspace. You must unzip and put each folder in the src directory.
2.) Build "turtlesim_control" and "turtlesim_interfaces" in your workspace.
```
cd ~/[your_workspace]
colcon build --packages-select turtlesim_plus_control turtlesim_plus_interfaces
source install/setup.bash
```

# Testing out turtlesim_control
- Terminal 1: Run launch file in terminal
```
ros2 launch turtlesim_plus_control following.launch.py
```

# Schematics of System
![image](https://github.com/napassorn29/FRA501_exam1_6435_6449/assets/119843578/3024b439-d3fc-4076-bb44-5a4f58a6dbe2)
Package : turtlesim_plus_control 
Node
- turtlesim_plus
  service : /remove_turtle,/spawn_turtle,/spawn_pizza
- controller
  service : /remove_turtle,/spawn_turtle
- scheduler
  service : /spawn_pizza
- yaml_generator
  service : - 
- observer
  service : -
Service
- /remove_turtle
- /spawn_turtle
- /spawn_pizza
  

