#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Float32MultiArray
from geometry_msgs.msg import Twist
import math

class LineControllerNode(Node):
    def __init__(self):
        super().__init__("line_controller_node")
        self.subscription = self.create_subscription(
            Float32MultiArray,
            "ir_data",
            self.ir_data_callback,
            10
        )
        self.publisher_ = self.create_publisher(Twist, "cmd_vel", 10)
        self.kp = 0.5  # Proportional gain
        self.linear_speed = 0.2  # Linear speed

    def ir_data_callback(self, msg):
        # Assuming msg.data contains [v1, v2, v3, v4, v5]
        v1, v2, v3, v4, v5 = msg.data 
        twist_msg = Twist()
        twist_msg.linear.x = self.linear_speed

        if (v1==1 and v2==1 and v3==1 and v4==1 and v5==1) or (v1==0 and v2==0 and v3==0 and v4==0 and v5==0) :
            twist_msg.linear.x=0.0
            twist_msg.angular.z=0.0
        # Create Twist message
        elif (v1==1 and v2==0 and v3==0 and v4==0 and v5==0):
            twist_msg.linear.x=0.22
            twist_msg.angular.z=-2
        
        elif (v1==0 and v2==1 and v3==0 and v4==0 and v5==0):
            twist_msg.linear.x=0.22
            twist_msg.angular.z=-1

        elif (v1==0 and v2==0 and v3==1 and v4==0 and v5==0):
            twist_msg.linear.x=0.22
            twist_msg.angular.z=0

        elif (v1==0 and v2==0 and v3==0 and v4==1 and v5==0):
            twist_msg.linear.x=0.22
            twist_msg.angular.z=1

        elif (v1==0 and v2==0 and v3==0 and v4==0 and v5==1):
            twist_msg.linear.x=0.22
            twist_msg.angular.z=2

        






        # Publish Twist message to cmd_vel
        self.publisher_.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    node = LineControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()