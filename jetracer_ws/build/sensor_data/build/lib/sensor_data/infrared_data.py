#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Float32MultiArray

import RPi.GPIO as GPIO

class InfraredDataPublisherNode(Node):
    def __init__(self):
        super().__init__("infrared_data_publisher")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(3, GPIO.IN)
        GPIO.setup(5, GPIO.IN)
        GPIO.setup(7, GPIO.IN)
        GPIO.setup(11, GPIO.IN)
        GPIO.setup(13, GPIO.IN)
        self.publisher_ = self.create_publisher(Float32MultiArray, "ir_data", 10)
        self.timer=self.create_timer(0.1,self.publish_gpio_values)

    def publish_gpio_values(self):
        msg = Float32MultiArray()
        msg.data = [
            float(GPIO.input(13)),
            float(GPIO.input(11)),
            float(GPIO.input(7)),
            float(GPIO.input(5)),
            float(GPIO.input(3)),
        ]
        self.publisher_.publish(msg)
        self.get_logger().info("Published GPIO values: %s" % msg.data)

def main(args=None):
    rclpy.init(args=args)
    node = InfraredDataPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()