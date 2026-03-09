# Week 1 – Post Lab Answers

## 1. Define the following terms

Node  
A node is an executable program in ROS2 that performs computation such as controlling a robot, processing sensor data, or planning motion.

Topic  
A topic is a communication channel used by nodes to exchange messages.

Package  
A package is a folder containing ROS2 code, dependencies, configuration files, and build instructions.

Workspace  
A workspace is a directory where multiple ROS2 packages are stored, built, and managed together.

---

## 2. Why is sourcing required?

Sourcing is required to configure the environment variables so that the system can locate ROS2 packages, libraries, and executables. Without sourcing the workspace setup file, ROS2 will not recognize newly created packages or nodes.

---

## 3. What is the purpose of `colcon build`?

The `colcon build` command compiles and builds all packages inside the workspace. It generates several folders including:

build – intermediate compilation files  
install – installed packages and executables  
log – build process logs

---

## 4. What does the console_scripts entry in setup.py do?

The `console_scripts` section registers Python functions as executable commands in ROS2. It allows ROS2 to run a node using the command:

ros2 run <package_name> <executable_name>

---

## 5. Publisher and Subscriber Diagram

Publisher Node
      |
      |   Topic (/cmd_vel)
      v
Subscriber Node

The publisher sends messages to the topic and the subscriber receives those messages.
