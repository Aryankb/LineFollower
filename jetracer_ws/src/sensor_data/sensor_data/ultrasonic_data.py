#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Float32MultiArray
import time
import RPi.GPIO as GPIO
import concurrent.futures

class UltrasonicDataPublisherNode(Node):
    def __init__(self):
        super().__init__("ultrasonic_data_publisher")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(12, GPIO.IN)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(19, GPIO.IN)
        self.publisher_ = self.create_publisher(Float32MultiArray, "us_data", 10)
        self.timer=self.create_timer(0.01,self.publish_gpio_values)
        # self.previous_distance=100
        # self.t=0.1

    # def thr(self,gp):
   


    def publish_gpio_values(self):
        msg = Float32MultiArray()
        # Ensure the trigger pin is low
        GPIO.output(11, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
        time.sleep(0.5)

        # Send 10us pulse to trigger
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(21, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
             # Wait for echo to start
        while GPIO.input(12) == GPIO.LOW:
            pulse_start = time.time()

        # Wait for echo to end
        while GPIO.input(12) == GPIO.HIGH:
            pulse_end = time.time()

        # Calculate pulse duration
        pulse_duration = pulse_end - pulse_start

        # Speed of sound in air is 34300 cm/s
        # Distance = (time taken for pulse to travel to object and back * speed of sound) / 2
        distance = (pulse_duration * 34300) / 2

        # distance=(1-self.t)*self.previous_distance + self.t*(distance)
        # self.previous_distance =distance
        msg.data = [
           distance,
           0.0
        ]
        self.publisher_.publish(msg)
        self.get_logger().info("Published distance: %s" % msg.data)

def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicDataPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()