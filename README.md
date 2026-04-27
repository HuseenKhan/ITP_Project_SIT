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

  
## Running Python Scripts Using Shared Folder in Docker
Create a shared folder on the Raspberry Pi:
```bash
mkdir -p /home/pi/SharedFolder
```

Save your Python scripts inside this folder:
```bash
/home/pi/SharedFolder
```

Open the ROS2 Docker startup file:
``` nano /home/pi/ros2_humble.sh ```
-Add the following volume line inside the Docker command:
-v /home/pi/SharedFolder:/home/pi/SharedFolder \
-The updated Docker script should look like this:
#!/bin/bash
xhost +
docker run -it \
--privileged=true \
--net=host \
--env="DISPLAY" \
--env="QT_X11_NO_MITSHM=1" \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-v /home/pi/SharedFolder:/home/pi/SharedFolder \
--security-opt apparmor:unconfined \
-v /dev/input:/dev/input \
-v /dev/video0:/dev/video0 \
yahboomtechnology/ros-humble:4.1.2 \
/bin/bash /root/1.sh

-After starting the Docker container, go to the shared folder inside Docker:
-cd /home/pi/SharedFolder
-Run your Python script:
-python3 your_script.py

```
## Contact
For enquiries, support, or suggestions, please feel free to contact:
- huseen0207@outlook.com  
- huseeen.khan@singaporetech.edu.sg
