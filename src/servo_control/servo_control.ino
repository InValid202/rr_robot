#include <Servo.h>
#include <ros.h>
#include <std_msgs/Int16.h>
#include <std_msgs/Bool.h>
#include <std_msgs/Float32.h>
#include <std_srvs/Trigger.h>
Servo myservo1;
Servo myservo2;


bool guiControlMode = true;
unsigned long previousMillis = 0;
int count;
const unsigned long interval = 750; 

const int led_pin = 3;
const int button_pin = 7;

bool last_reading;
bool published = true;
bool on_status = false;
// bool on_status = true; // debug mode 

std_msgs::Float32 potent1;
std_msgs::Float32 potent2;
std_msgs::Bool guimode_arduino; 
std_msgs::Bool on_status_msg;


void servoCb1(const std_msgs::Int16& receivedMsg1)
{
  if (guiControlMode && on_status)
  {
    int servo_angle1 = receivedMsg1.data + 90;
    if (servo_angle1 >= 0 && servo_angle1 <= 180)
    {
      myservo1.write(servo_angle1);
    }
  }
  
}

void servoCb2(const std_msgs::Int16& receivedMsg2)
{
  if (guiControlMode && on_status)
  {
    int servo_angle2 = receivedMsg2.data + 90;
    if (servo_angle2 >= 0 && servo_angle2 <= 180)
    {
      myservo2.write(servo_angle2);
    }
  }
}

void mode_control(const std_msgs::Bool& receivedMsg3)
{
  guiControlMode = receivedMsg3.data;
}

void connectionCallback(const std_srvs::Trigger::Request &req, std_srvs::Trigger::Response &res)
{
  res.success = true;
  res.message = "Service triggered successfully";
}

ros::NodeHandle nh;

// init Subscriber
ros::Subscriber<std_msgs::Int16> sub1("servo_control1", &servoCb1); // subscriber for servo1 with GUI
ros::Subscriber<std_msgs::Int16> sub2("servo_control2", &servoCb2); // subscriber for servo2 with GUI
ros::Subscriber<std_msgs::Bool> sub3("gui_mode", &mode_control); // subscriber for mode  

// init Publisher 
ros::Publisher pub1("potential1", &potent1); // publisher for potent1
ros::Publisher pub2("potential2", &potent2); // publisher for potent2
ros::Publisher pub3("syncMode", &guimode_arduino); // reset signal to reset mode when GUI's mode in ui isn't GUI control
ros::Publisher pub4("onOff", &on_status_msg); // check on off status

//inti Service
ros::ServiceServer<std_srvs::Trigger::Request, std_srvs::Trigger::Response> service("/connection_service", &connectionCallback);

void setup() 
{
  
  myservo1.attach(9, 500, 2500);
  myservo2.attach(8, 500, 2500);
  nh.initNode();

  nh.advertise(pub1);
  nh.advertise(pub2);
  nh.advertise(pub3);
  nh.advertise(pub4);
  
  nh.subscribe(sub1);
  nh.subscribe(sub2);
  nh.subscribe(sub3);

  nh.advertiseService(service);
  
  pinMode(button_pin, INPUT);

  digitalWrite(button_pin, HIGH);

  last_reading = !digitalRead(button_pin);

  // on_status_msg.data = true; // debug mode

  count = 0;

}

void loop() 
{
  
  unsigned long currentMillis = millis();
  bool reading = ! digitalRead(button_pin);

  if (last_reading != reading)
  {
      published = false;
  }
  
  if(count >= 200)
  {
    
    guimode_arduino.data = guiControlMode;
    pub3.publish(&guimode_arduino); // syn GUI mode
    pub4.publish(&on_status_msg); // syn on off status
    count = 0;
  }
  
  if(currentMillis - previousMillis >= interval)
  {
    
    previousMillis = currentMillis;
    
    if (!published)
    {
      if (reading)
      {
        on_status = !on_status;
        on_status_msg.data = on_status;
        
      }
      published = true;
    }
    
    if (on_status)
    {
      float RValue1 = analogRead(A0); 
      float RValue2 = analogRead(A3); 
      digitalWrite(led_pin, HIGH);
        
//      float RPercent1 = (static_cast<float>(RValue1) / 1016) * 180.0;
//      float RPercent2 = (static_cast<float>(RValue2) / 1016) * 180.0;

      float RPercent1 = map(RValue1, 0, 1024, 0, 180);
      float RPercent2 = map(RValue2, 0, 1024, 0, 180);
    
      potent1.data = RValue1;
      potent2.data = RValue2;
    
      pub1.publish(&potent1);
      pub2.publish(&potent2);
      if (!guiControlMode)
      {  
        myservo1.write(RPercent1);
        myservo2.write(RPercent2);
      }
    }  
    else
    {
      digitalWrite(led_pin, LOW);
    }
  }
  
  
  count++;
  last_reading = reading;
  nh.spinOnce();
  delay(1);
}
