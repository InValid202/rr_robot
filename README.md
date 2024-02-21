# rr_robot


Software requirement:
1. Ubuntu 20.04  
2. ROS Noetic
3. Arduino IDE 1.8.15
4. Rosserial Arduino Library 0.7.9
5. Python3
6. Tkinter GUI python library


Source material:
1. Ubuntu 20.04 installation: https://www.youtube.com/watch?v=BnV23ZEI34w
2. ROS Noetic installation: https://www.youtube.com/watch?v=ZA7u2XPmnlo
3. Arduino installation tutorial : https://www.youtube.com/watch?v=QTK1g0P8OUM&list=PLVZDfM16Af8nOa5SLcIAcPFzIGaJhaRgs&index=6&t=5875s


Hardware requirement:
1. Arduino UNO R3       1 
2. Potentiometer        2
3. Button               1
4. MG996R servo 6v      1
5. MG90S  servo 5v      1

Circuit connection:
![circuit](https://github.com/InValid202/rr_robot/assets/125998503/14724ada-29ed-48fb-894d-8f6f49163eba)

Assembly robot preview:
![assembly](https://github.com/InValid202/rr_robot/assets/125998503/4755fe8c-5e7e-4a92-b16d-498a22362662)


Step to install:
1. go into src file of your ROS workspace with this command:

            cd {your catkin workspace}/src
   
      example: cd catkin_ws/src
   
3. clone my rr_robot repository to your current file in terminal with this command:
   
            git clone https://github.com/InValid202/rr_robot.git

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


Ros can't find my package:
1. Ros can't find a rr_robot package even thought you used catkin_make command and followed all 8 installation step above.
   solution. first, go back to home in terminal with this command:

            cd
   
2. edit .bashrc file with this command:

            gedit .bashrc

3. scroll down to bottom of the .bashrc file add this command to .bashrc:

            source ~/{Your ROS workspace}/devel/setup.bash

      example: source ~/catkin_ws/devel/setup.bash


Port's permission error:
1. can't upload code from arduino IDE or run rosserial, you can use this command to give a permission for a port:

            sudo chmod a+rw {your port that connected with arduino}

      example: sudo chmod a+rw /dev/ttyUSB0
