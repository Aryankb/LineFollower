#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Float32MultiArray
from geometry_msgs.msg import Twist
import math
import time

class LineControllerNode(Node):
    def __init__(self):
        super().__init__("line_controller_node")
        self.subscription = self.create_subscription(
            Float32MultiArray,
            "ir_data",
            self.ir_data_callback,
            10
        )
        self.subscription_us = self.create_subscription(
            Float32MultiArray,
            "us_data",
            self.ultrasonic_data_callback,
            10
        )
        self.publisher_ = self.create_publisher(Twist, "/cmd_vel", 10)
        self.threshold_distance = 40  # Set your threshold distance here
        self.ultrasonic_triggered = False
        self.twist_data=None




    def ir_data_callback(self, msg):

        if not self.ultrasonic_triggered:
        # Assuming msg.data contains [v1, v2, v3, v4, v5]
            v1, v2, v3, v4, v5 = msg.data 
            
            twist_msg = Twist()

            
            if (v1==0 and v2==0 and v3==0 and v4==0 and v5==0) :
                twist_msg.linear.x=-0.1
                twist_msg.angular.z=0.0

                # print("straight",float(twist_msg.linear.x))
            elif (v1==1 and v2==1 and v3==1 and v4==1 and v5==1) :
                twist_msg.linear.x=-0.0
                twist_msg.angular.z=0.0


                # print("stop",float(twist_msg.linear.x))
            elif (v1==1 and v2==0 and v3==0 and v4==0 and v5==0):
                twist_msg.linear.x=-0.05
                twist_msg.angular.z=-1.2
                # while(twist_msg.linear.x<0.22 or twist_msg.angular.z>-2.0):
                #     if(twist_msg.linear.x<0.22):
                #         twist_msg.linear.x+=0.01

                #     if(twist_msg.angular.z>-2.0):
                #         twist_msg.angular.z-=0.01

                #     time.sleep(0.2)

                # print("v1 black")
            
            elif (v1==0 and v2==1 and v3==0 and v4==0 and v5==0):
                twist_msg.linear.x=-0.1
                twist_msg.angular.z=-1.0
                # while(twist_msg.linear.x<0.22 or twist_msg.angular.z>-1.0):
                #     if(twist_msg.linear.x<0.22):
                #         twist_msg.linear.x+=0.01

                #     if(twist_msg.angular.z>-1.0):
                #         twist_msg.angular.z-=0.01

                #     time.sleep(0.2)

                # print("v2 vlack")

            elif (v1==0 and v2==0 and v3==1 and v4==0 and v5==0) or (v1==0 and v2==1 and v3==1 and v4==1 and v5==0):
                twist_msg.linear.x=-0.15
                twist_msg.angular.z=0.0
                # while(twist_msg.linear.x<0.22):
                #     twist_msg.linear.x+=0.01
                #     time.sleep(0.5)
                

                # print("v3 vlack",float(twist_msg.linear.x))

            elif (v1==0 and v2==0 and v3==0 and v4==1 and v5==0) :
                twist_msg.linear.x=-0.1
                twist_msg.angular.z=1.0
                # while(twist_msg.linear.x<0.22 or twist_msg.angular.z<1.0):
                #     if(twist_msg.linear.x<0.22):
                #         twist_msg.linear.x+=0.01

                #     if(twist_msg.angular.z<1.0):
                #         twist_msg.angular.z+=0.01

                #     time.sleep(0.2)
                # print("v4 vlack")

            elif (v1==0 and v2==0 and v3==0 and v4==0 and v5==1):
                twist_msg.linear.x=-0.05
                twist_msg.angular.z=1.2
                # while(twist_msg.linear.x<0.22 or twist_msg.angular.z<2.0):
                #     if(twist_msg.linear.x<0.22):
                #         twist_msg.linear.x+=0.01

                #     if(twist_msg.angular.z<2.0):
                #         twist_msg.angular.z+=0.01

                #     time.sleep(0.2)
                # print("v5 vlack")

            elif (v1==0 and v2==0 and (v3==0 or v4==1 or v5==1)):
                twist_msg.linear.x=-0.0
                twist_msg.angular.z=1.2

            elif ((v1==1 or v2==1 or v3==1) and v4==0 and v5==0):
                twist_msg.linear.x=-0.0
                twist_msg.angular.z=-1.2


            
        
            
            





            # Publish Twist message to cmd_vel
            self.publisher_.publish(twist_msg)
        
    def ultrasonic_data_callback(self, msg):
        distance, faltu = msg.data
        if distance < self.threshold_distance:
            
            self.ultrasonic_triggered = True
            self.send_twist_messages()
            print("obstical detected")

            self.ultrasonic_triggered = False
            
            

    def send_twist_messages(self):
        # Send array of velocities as twist messages
        self.twist_array = [
            (0.0,1.0,0.5),
            (-0.1,0.0,6),
            (0.0,-1.0,1),
            (-0.1,0.0,6)
            
        ]
        # for linear, angular in twist_array:
        #     twist_msg = Twist()
        #     twist_msg.linear.x = linear
        #     twist_msg.angular.z = angular
        #     self.publisher_.publish(twist_msg)
        #     # Add a delay between each twist message if needed
        #     self.get_logger().info(f"Twist message sent: Linear={linear}, Angular={angular}")
        #     time.sleep(1)  # Example delay, adjust as needed        
          # seconds
    
    # Define the publishing rate (high frequency)
        publishing_rate = 100  # Hz (100 times per second)
        print("avoiding ")
        for linear, angular,duration_per_twist in self.twist_array:
            twist_msg = Twist()
            twist_msg.linear.x = linear
            twist_msg.angular.z = angular
            
            # Calculate the number of iterations based on the desired duration
            iterations = int(duration_per_twist * publishing_rate)
            
            # Publish the twist message at a high frequency for the specified duration
            for _ in range(iterations):
                self.publisher_.publish(twist_msg)
                # self.get_logger().info(f"Twist message sent: Linear={linear}, Angular={angular}")
                
                # Sleep for a short duration to achieve the desired publishing rate
                time.sleep(1.0 / publishing_rate)







def main(args=None):
    rclpy.init(args=args)
    node = LineControllerNode()
    try:
        rclpy.spin(node)
    finally:
        # Shutdown the ROS node
        node.destroy_node()
        rclpy.shutdown()

def spin(self):
    try:
        rclpy.spin(self)
    except KeyboardInterrupt:
        # If keyboard interrupt is received, stop the robot
        twist_msg = Twist()
        twist_msg.linear.x = 0.0
        twist_msg.angular.z = 0.0
        self.publisher_.publish(twist_msg)
        print("Keyboard interrupt received. Stopping the robot.")


if __name__ == "__main__":
    main()
