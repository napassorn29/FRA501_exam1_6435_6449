# FRA501_exam1_6435_6449
 This package is associated to FRA501 : Robotics DevOps class in FIBO, KMUTT for the reason to study about developing system by using ROS2. The relevant topics are include:

# proposition
This package contains launch file which spawn 4 turtles from turtlesim_plus package. Each of them will droping 20 pizzas to form a shape of alphabets "F", "I", "B" and "O".

# Installation

1.) Clone the repo to the src directory of your workspace. You must unzip and put each folder in the src directory.

2.) place "turtlesim_plus_control" and "turtlesim_plus_control_interfaces" in src 

3.) install "turtlesim_plus" in https://github.com/tchoopojcharoen/turtlesim_plus?fbclid=IwAR288upqzOTEiJuaYzbuu524Q-GatM03M-T5lKkmDtIZWXEHwY0r6hikyqs 

4.) place "turtlesim_plus" in src 

5.) check in src will have 3 file : "turtlesim_plus_control","turtlesim_plus_control_interfaces" and "turtlesim_plus"

6.) Build "turtlesim_plus_control" and "turtlesim_plus_control_interfaces" in your workspace.
```
cd ~/[your_workspace]
colcon build 
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
- turtlesim_plus : have service : /remove_turtle,/spawn_turtle,/spawn_pizza
- controller : have service : /spawn_pizza
- scheduler : no service
- yaml_generator : no service
- observer : no service

Service
- /remove_turtle
- /spawn_turtle
- /spawn_pizza



  

