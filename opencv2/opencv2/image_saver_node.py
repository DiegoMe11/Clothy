import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from cv_bridge import CvBridge
import cv2
import os
import threading
import numpy as np

def detect_color(hsv_img, lower, upper, color_name, original_img):
    mask = cv2.inRange(hsv_img, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    total_pixels = np.sum(mask > 0)
    
    max_area = 0
    max_contour = None
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour
    
    if max_contour is not None:
        x, y, w, h = cv2.boundingRect(max_contour)
        cv2.rectangle(original_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(original_img, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    return total_pixels, original_img

class ImageSaver(Node):
    def __init__(self):
        super().__init__('image_saver_node')
        self.bridge = CvBridge()

        qos_profile = QoSProfile(reliability=QoSReliabilityPolicy.BEST_EFFORT, depth=10)

        self.image_sub = self.create_subscription(
            Image,
            '/image',
            self.image_callback,
            qos_profile)

        self.save_dir = os.path.expanduser('~/Desktop')
        self.image_saved = False
        self.latest_image = None
        self.get_logger().info(f'Image saver node started. Images will be saved to {self.save_dir}')

    def image_callback(self, msg):
        if not self.image_saved:
            try:
                cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
                
                lower_blue = np.array([110, 50, 50])
                upper_blue = np.array([130, 255, 255])
                lower_red = np.array([0, 50, 50])
                upper_red = np.array([10, 255, 255])
                lower_yellow = np.array([20, 100, 100])
                upper_yellow = np.array([30, 255, 255])
                lower_green = np.array([30, 50, 50])
                upper_green = np.array([90, 255, 255])
                
                colors = {
                    'Azul': detect_color(hsv, lower_blue, upper_blue, 'Azul', cv_image.copy()),
                    'Rojo': detect_color(hsv, lower_red, upper_red, 'Rojo', cv_image.copy()),
                    'Amarillo': detect_color(hsv, lower_yellow, upper_yellow, 'Amarillo', cv_image.copy()),
                    'Verde': detect_color(hsv, lower_green, upper_green, 'Verde', cv_image.copy()),
                }
                
                max_color = max(colors, key=lambda k: colors[k][0])
                
                save_path = os.path.join(self.save_dir, f'{max_color}_camera_image.jpg')
                cv2.imwrite(save_path, colors[max_color][1])
                self.get_logger().info(f'Saved image to {save_path}')
                self.image_saved = True
                self.image_sub.destroy()
            except Exception as e:
                self.get_logger().error('Error processing image: %s' % str(e))

def main(args=None):
    rclpy.init(args=args)
    image_saver = ImageSaver()
    try:
        while rclpy.ok():
            rclpy.spin_once(image_saver, timeout_sec=0.1)
    except KeyboardInterrupt:
        image_saver.get_logger().info('Shutting down')
    finally:
        image_saver.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

