import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from picamera import PiCamera
import time

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        self.publisher_ = self.create_publisher(Image, 'camera_feed', 10)
        self.bridge = CvBridge()

    def publish_image(self):
        camera = PiCamera()
        camera.resolution = (640, 480)
        time.sleep(2)  # Allow camera to warm up
        while not self.publisher_.get_subscription_count():
            time.sleep(0.1)  # Wait for subscribers
        try:
            while True:
                img_msg = self.bridge.cv2_to_imgmsg(camera.capture(), encoding="bgr8")
                self.publisher_.publish(img_msg)
        finally:
            camera.close()

def main(args=None):
    rclpy.init(args=args)
    camera_publisher = CameraPublisher()
    camera_publisher.publish_image()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
