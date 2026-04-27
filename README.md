# Next-Gen Robotics: Real-Time Command and Control via 5G/Wi-Fi Edge AI

## Overview
This project is developed as part of an ITP (Integrated Team Project) for Computer Engineering (CEG) students at the Singapore Institute of Technology (SIT).

The goal is to enable real-time command and control of a robotic system using 5G/Wi-Fi and Edge AI concepts.

## Hardware
- Yahboom Car Robot, Laptop 

## Implementation
- Devlop multiple Python scripts for real-time command and control
- Deploy pretrained lightweight AI models onto edge servers

## Key Features
- Real-time control
- Low latency
- Practical robotics implementation

## Application
- Smart robotics
- Remote control systems
- Automation

## Running the Car Control GUI

The project includes a Python file named `car_control.py`.

This file provides a simple GUI interface for controlling the Yahboom car robot. The user can control the car using buttons such as:

- Forward
- Backward
- Left
- Right
- Stop
  
## Running Python Scripts in Yahboom Docker Environment
To save files inside the Yahboom robot and run via Docker environemnt to access ROS, follow these steps:
Create a shared folder on the Raspberry Pi:
```bash
mkdir -p /home/pi/Your_Folder_Name
```

Save your Python scripts inside this folder:
```bash
/home/pi/Your_Folder_Name
```

Open the ROS2 Docker startup file:
```bash
nano /home/pi/ros2_humble.sh
```
Add the following volume line inside the Docker command:
```bash
-v /home/pi/SharedFolder:/home/pi/SharedFolder \
```
The updated Docker script should look like this:
```bash
#!/bin/bash
xhost +
docker run -it \
--privileged=true \
--net=host \
--env="DISPLAY" \
--env="QT_X11_NO_MITSHM=1" \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-v /home/pi/Your_Folder_name:/home/pi/Your_Folder_name \
--security-opt apparmor:unconfined \
-v /dev/input:/dev/input \
-v /dev/video0:/dev/video0 \
yahboomtechnology/ros-humble:4.1.2 \
/bin/bash /root/1.sh
```

After starting the Docker container, go to the shared folder inside Docker:
```bash
cd /home/pi/SharedFolder
```
Run your Python script:
```bassh
python3 your_script.py
```
## Contact
For enquiries, support, or suggestions, please feel free to contact:
- huseen0207@outlook.com  
- huseeen.khan@singaporetech.edu.sg
