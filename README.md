# rr_robot

software requirement:
1. Ubuntu 20.04  
2. ROS Noetic
3. Arduino IDE 1.8.15
4. Rosserial Arduino Library 0.7.9
5. Python3
6. Tkinter GUI python library

Hardware requirement:
1. Arduino UNO R3       1 
2. Potentiometer        2
3. Button               1
4. MG996R servo 6v      1
5. MG90S  servo 5v      1

Step to install:
1. go into src file of your ROS workspace with this command:

            cd {your catkin workspace}/src
   
   example: cd catkin_ws/src
   
3. clone my rr_robot repository to your current file in terminal with this command:
   
            git clone git@github.com:InValid202/rr_robot.git

4. go back from src to catkin workspace with this command in terminal:

            cd ..
   
5. use this command in your current folder in terminal:

            catkin_make

6. go to src file of rr_robot package and add permission to execute gui python file:

            cd src/rr_robot/src

7. add permission to execute gui python file

            chmod +x remote_gui_realtime.py

8. launch a launch file in rr_robot package with your port that connect with your Arduino (you can check port in your Arduino IDE):

            roslaunch rr_robot rr_robot.launch port:="{Your port}"

   example: roslaunch rr_robot rr_robot.launch port:="dev/ttyUSB0"


            
