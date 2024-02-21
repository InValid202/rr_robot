#!/usr/bin/env python3

from tkinter import*
import rospy
from std_msgs.msg import Int16
from std_msgs.msg import Bool
from std_msgs.msg import Float32
from std_srvs.srv import Trigger 
from sensor_msgs.msg import JointState
from math import pi

root  = Tk()
root.title("RR Robot remote")
root.geometry("900x400")

canvas = Canvas(root ,width=900, height=400)
canvas.pack()

rospy.init_node("Remote")


class GUI:
	def __init__(self, canvas):
	
	
		# init general variable
		self.guiControlMode = True 
		self.canvas = canvas
		self.servo1_data = 0
		self.servo2_data = 0
		self.onStatus = False
		self.connected = False
		self.model_angle1 = 0
		self.model_angle2 = 0
		
		# init jointState massage
		self.joint_state = JointState()
		self.joint_state.name = ['joint1', 'joint2']
		self.joint_state.position = [self.model_angle1, self.model_angle2]
		self.joint_state.velocity = [0.01, 0.02] #test velo
		self.joint_state.effort = [10.0, 5.0] # test effort
	
		# init ros's part
		self.pub1 = rospy.Publisher("servo_control1", Int16, queue_size = 10) # publisher for servo1
		self.pub2 = rospy.Publisher("servo_control2", Int16, queue_size = 10) # publisher for servo2
		self.pub3 = rospy.Publisher("gui_mode", Bool, queue_size = 10)
		self.pub4 = rospy.Publisher("joint_states", JointState, queue_size = 10) # publisher for urdf model
		self.sub1 = rospy.Subscriber("syncMode", Bool, self.syncCb)
		self.sub2 = rospy.Subscriber("potential1", Float32, self.potent1Cb)
		self.sub3 = rospy.Subscriber("potential2", Float32, self.potent2Cb)
		self.sub4 = rospy.Subscriber("onOff" , Bool, self.onCb)		
		
		# init gui controller part
		
		
		self.gui_label = Label(root, text="GUI Controller", font=("Arial", 16), fg="blue")
		self.gui_label.place(x= 85, y= 20)

		self.angle1 = Scale(root, from_=-90, to=90, orient=HORIZONTAL)
		self.angle1.set(0)
		self.angle1.place(x= 100, y=80)

		self.angle2 = Scale(root, from_=-90, to=90, orient=HORIZONTAL)
		self.angle2.set(0)
		self.angle2.place(x= 100, y=160)


		self.home_botton = Button(root, text = "home" , command = self.home_command)
		self.home_botton.place(x= 115, y=320)

		self.status1_label = Label(root, text="GUI controller's status:", font=("Arial", 12))
		self.status1_label.place(x= 10, y=370)

		self.status_light1 = self.canvas.create_oval(180, 373, 200, 393, fill='green')

		self.line1 = self.canvas.create_line(300, 0, 300, 450, fill='red', width=2)
		
		
		# init current status part
		
		self.current_label = Label(root, text="Current Position", font=("Arial", 16), fg="blue")
		self.current_label.place(x= 380, y= 20)


		self.change_mode_botton = Button(root, text = "change mode" , command = self.change_mode)
		self.change_mode_botton.place(x= 392, y=320)
		
		self.Angle1_label = Label(root, text="First servo's angle     :", font=("Arial", 13))
		self.Angle1_label.place(x=310, y= 100)
		
		self.Angle1_data = Label(root, text="No data", font=("Arial", 12), fg="red")
		self.Angle1_data.place(x=490, y= 100)
		
		self.Angle2_label = Label(root, text="Second servo's angle:", font=("Arial", 13))
		self.Angle2_label.place(x=310, y= 180)
		
		self.Angle2_data = Label(root, text="No data", font=("Arial", 12), fg="red")
		self.Angle2_data.place(x=490, y= 180)
		
		self.connection_label = Label(root, text = "Connection status: ")
		self.connection_label.place(x = 310, y = 370)
		
		
		self.status_light3 = self.canvas.create_oval(445, 373, 465, 393, fill='red') # not debug
		
		self.line2 = self.canvas.create_line(600, 0, 600 ,450, fill='red', width=2)

		
		# init potent controller part

		self.Poten_label = Label(root, text="Potentiometer controller", font=("Arial", 16), fg="blue")
		self.Poten_label.place(x= 640, y= 20)
		
		self.potent1_label = Label(root, text="First potentiometer's data     :", font=("Arial", 13))
		self.potent1_label.place(x=605, y= 100)
		
		self.potent1_data = Label(root, text="No data", font=("Arial", 12), fg="red")
		self.potent1_data.place(x=840, y= 100)
		
		self.potent2_label = Label(root, text="Second potentiometer's data:", font=("Arial", 13))
		self.potent2_label.place(x=605, y= 180)
		
		self.potent2_data = Label(root, text="No data", font=("Arial", 12), fg="red")
		self.potent2_data.place(x=840, y= 180)
		
		self.status_light2 = self.canvas.create_oval(780, 373, 800, 393, fill='red')
		self.status2_label = Label(root, text="Potentiometer's status:", font=("Arial", 12))
		self.status2_label.place(x= 610, y=370)

	
	# Buttons function
	
	def set_command(self):
		if (self.guiControlMode and self.connected):
			angle1_value = Int16()
			angle2_value = Int16()
			angle1_value.data = self.angle1.get()
			angle2_value.data = self.angle2.get()
			
			self.Angle1_data.config(text = f"{self.angle1.get()}")
			self.Angle2_data.config(text = f"{self.angle2.get()}")
			
			self.pub1.publish(angle1_value)
			self.pub2.publish(angle2_value)
			
			# set angle for model in urdf
			
			self.model_angle1 = self.angle1.get() * pi / 180
			self.model_angle2 = self.angle2.get() * pi / 180
			
		 
	def change_mode(self):
		
		self.guiControlMode = not(self.guiControlMode)
		mode = Bool()
		mode.data = self.guiControlMode
		self.pub3.publish(mode)
			
		if (self.guiControlMode):
			self.home_command()
			self.canvas.itemconfig(self.status_light1, fill="green")
			self.canvas.itemconfig(self.status_light2, fill="red")
				
		else :
			self.canvas.itemconfig(self.status_light1, fill="red")
			self.canvas.itemconfig(self.status_light2, fill="green")
		
	def home_command(self):
		if (self.guiControlMode):
			self.angle1.set(0)
			self.angle2.set(0)
			self.set_command()
			
	# callback function for ROS sub
	
	def syncCb(self, guimode_arduino):
		self.guiControlMode = guimode_arduino.data
		if (self.guiControlMode):
			self.canvas.itemconfig(self.status_light1, fill="green")
			self.canvas.itemconfig(self.status_light2, fill="red")	
		else :
			self.canvas.itemconfig(self.status_light1, fill="red")
			self.canvas.itemconfig(self.status_light2, fill="green")

	def check_arduino_connection(self):
		try:
			trigger_service = rospy.ServiceProxy('/connection_service', Trigger)
			response = trigger_service()
			if(response.success and self.onStatus):
				self.canvas.itemconfig(self.status_light3, fill="green")
				self.Angle1_data.config(fg="green")
				self.Angle2_data.config(fg="green")
				self.potent1_data.config(fg="green")
				self.potent2_data.config(fg="green")
				self.connected = True
			else:
				self.canvas.itemconfig(self.status_light3, fill="red")
				self.Angle1_data.config(text = "No data", fg="red")
				self.Angle2_data.config(text = "No data", fg="red")
				self.potent1_data.config(text = "No data", fg="red")
				self.potent2_data.config(text = "No data", fg="red")
				self.connected = False
				
		except rospy.ServiceException as e:
			self.canvas.itemconfig(self.status_light3, fill="red")
			self.Angle1_data.config(text = "No data", fg="red")
			self.Angle2_data.config(text = "No data", fg="red")
			self.potent1_data.config(text = "No data", fg="red")
			self.potent2_data.config(text = "No data", fg="red")
			self.connected = False
		self.canvas.after(250, self.check_arduino_connection)
		
	def model_update(self):
		self.joint_state.header.stamp = rospy.Time.now()
		self.joint_state.position = [self.model_angle1, self.model_angle2]
		self.pub4.publish(self.joint_state)
		self.canvas.after(120, self.model_update)
		
	def gui_servo_update(self):
		self.set_command()
		self.canvas.after(1000, self.gui_servo_update)
		
	def potent1Cb(self, msg):
		if (self.onStatus):
			self.potent1_data.config(text= msg.data)
			if (not self.guiControlMode and self.connected):
				self.servo1_data = (float(msg.data) * 180 / 1023) - 90.0 
				self.Angle1_data.config(text = f"{round(self.servo1_data, 1)}")
				self.model_angle1 = self.servo1_data * pi / 180
				
		
	def potent2Cb(self, msg):
		if (self.onStatus):
			self.potent2_data.config(text= msg.data) 
			if (not self.guiControlMode and self.connected):
				self.servo2_data = (float(msg.data) * 180 / 1023) - 90.0 
				self.Angle2_data.config(text = f"{round(self.servo2_data, 1)}")
				self.model_angle2 = self.servo2_data * pi / 180
				
	def onCb(self, msg):
		self.onStatus = msg.data

gui = GUI(canvas)
gui.check_arduino_connection()
gui.model_update()
gui.gui_servo_update()
root.mainloop()
