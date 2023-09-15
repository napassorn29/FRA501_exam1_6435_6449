# FRA501_exam1_6435_6449
turtlesim_plus_control ใช้สำหรับการสอบวิชา FRA501 : Robotics DevOps เพื่อศึกษาการทำงานของระบบ ROS2 ในหัวข้อ Node, Publisher, Subscriber, Service, Parameter และนำความรู้มาประยุกต์ใช้ โดยมีหัวข้อที่เกี่ยวข้อคือ 
- Publisher/Subscriber
- Service/Client
- Custom interface
- Parameter in a class
- Launch file
- How to pass arguments to python node

# proposition
สร้าง Workspace ที่ประกอบไปด้วย Packages สำหรับ Spawn หุ่นยนต์เต่าจาก Package
TurtleSim Plus จำนวน 4 ตัว โดยที่หุ่นยนต[เต่าทั้ง 4 ตัวจะต้องเดินไปทิ้ง Pizza เป็นอักษร FIBO

# Installation
1.) Clone the repo to the src directory of your workspace. You must unzip and put each folder in the src directory.
2.) Build "turtlesim_control" and "turtlesim_interfaces" in your workspace.

# Testing out turtlesim_control
1.) Terminal 1: Run turtlesim_node
2.) Terminal 2: Start a controller
3.) Terminal 3: Start & run a scheduler (change the workspace name in the command)
4.) Terminal 4 & 5: While running those 3 terminals, you can monitor the heartbeat from each custom node

# Schematics of System
